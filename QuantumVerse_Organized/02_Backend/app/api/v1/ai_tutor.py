import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.ai import AIConversation, AIMessage
from app.ai.provider import get_ai_response

router = APIRouter(prefix="/ai", tags=["ai_tutor"])


def _parse_uuid(value: str, field_name: str) -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise HTTPException(400, f"Invalid {field_name}") from exc


@router.post("/conversations", status_code=201)
async def create_conversation(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    conv = AIConversation(user_id=user.id, title="New Conversation")
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return {"id": str(conv.id), "title": conv.title}


@router.get("/conversations")
async def list_conversations(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(
        select(AIConversation).where(AIConversation.user_id == user.id).order_by(desc(AIConversation.updated_at)).limit(20)
    )
    return {"conversations": [{"id": str(c.id), "title": c.title, "updated_at": c.updated_at.isoformat()} for c in rows.scalars().all()]}


class ChatBody(BaseModel):
    message: str
    difficulty: str = "beginner"
    context: dict[str, Any] | None = None


@router.post("/conversations/{conv_id}/chat")
async def chat(
    conv_id: str, body: ChatBody,
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    conv_uuid = _parse_uuid(conv_id, "conv_id")
    conv = (await db.execute(select(AIConversation).where(AIConversation.id == conv_uuid, AIConversation.user_id == user.id))).scalar_one_or_none()
    if not conv:
        raise HTTPException(404, "Conversation not found")

    # Get last 10 messages for context
    history_rows = await db.execute(
        select(AIMessage).where(AIMessage.conversation_id == conv_uuid).order_by(AIMessage.created_at).limit(10)
    )
    history = [{"role": m.role, "content": m.content} for m in history_rows.scalars().all()]

    # Save user message
    user_msg = AIMessage(conversation_id=conv_uuid, role="user", content=body.message)
    db.add(user_msg)

    # Get AI response
    ai_text = await get_ai_response(body.message, history, body.difficulty, body.context)

    # Save AI response
    ai_msg = AIMessage(conversation_id=conv_uuid, role="assistant", content=ai_text)
    db.add(ai_msg)

    # Update conversation title from first message
    if not history:
        conv.title = body.message[:60] + ("..." if len(body.message) > 60 else "")

    await db.commit()
    return {"response": ai_text, "conversation_id": conv_id}


class ExplainBody(BaseModel):
    circuit_data: dict[str, Any]
    difficulty: str = "beginner"


@router.post("/explain-circuit")
async def explain_circuit(body: ExplainBody, user: User = Depends(get_current_user)):
    ops = body.circuit_data.get("operations", [])
    gates = [op.get("gate") for op in ops]
    prompt = f"Explain this quantum circuit step by step for a {body.difficulty} student. Gates used: {', '.join(gates)}. Total gates: {len(ops)}."
    explanation = await get_ai_response(prompt, [], body.difficulty)
    return {"explanation": explanation, "gate_count": len(ops), "gates": list(set(gates))}
