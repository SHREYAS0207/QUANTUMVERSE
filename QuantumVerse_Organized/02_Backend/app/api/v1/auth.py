from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.security import create_access_token, verify_password, hash_password
from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User, Profile, UserStatistics, UserStatistics
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).options(selectinload(User.profile), selectinload(User.statistics)).where(User.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=body.name,
        email=body.email,
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    await db.flush()

    profile = Profile(
        id=user.id,
        learning_level=body.learning_level,
    )
    db.add(profile)

    statistics = UserStatistics(user_id=user.id)
    db.add(statistics)

    await db.commit()
    await db.refresh(user)
    await db.refresh(profile)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token, token_type="bearer",
        user_id=str(user.id), name=user.name, email=user.email,
        learning_level=profile.learning_level.value,
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).options(selectinload(User.profile), selectinload(User.statistics)).where(User.email == body.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    profile = user.profile
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token, token_type="bearer",
        user_id=str(user.id), name=user.name, email=user.email,
        learning_level=profile.learning_level.value if profile else "beginner",
    )


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed = {"name", "learning_level"}
    for key, val in body.items():
        if key in allowed:
            setattr(current_user, key, val)
    await db.commit()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)
