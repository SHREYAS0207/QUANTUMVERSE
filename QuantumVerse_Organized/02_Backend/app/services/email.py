"""Email service using SMTP (works with Gmail / SendGrid / Mailgun)."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

log = logging.getLogger(__name__)


EMAIL_TEMPLATES = {
    "welcome": {
        "subject": "Welcome to QuantumVerse AI 🔬",
        "body": """
        <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#080812;color:#fff;padding:32px;border-radius:16px">
          <div style="text-align:center;margin-bottom:32px">
            <h1 style="color:#00d4ff;font-size:28px;margin:0">QuantumVerse AI</h1>
            <p style="color:#6b6b80;margin:4px 0">Quantum Computing Mastery Platform</p>
          </div>
          <h2 style="color:#fff">Welcome, {name}! 🎉</h2>
          <p style="color:#a0a0b0;line-height:1.6">You're now part of the QuantumVerse community. Your quantum journey starts here.</p>
          <div style="background:#0d0d1a;border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:20px;margin:24px 0">
            <p style="color:#fff;margin:0 0 12px 0;font-weight:600">Get started:</p>
            <ul style="color:#a0a0b0;line-height:2;padding-left:20px">
              <li>Build your first quantum circuit in the <b style="color:#00d4ff">Quantum Lab</b></li>
              <li>Chat with <b style="color:#00d4ff">QubitAI</b> — your AI tutor</li>
              <li>Explore <b style="color:#00d4ff">Grover's Algorithm</b> in the Algorithm Explorer</li>
            </ul>
          </div>
          <div style="text-align:center">
            <a href="{app_url}" style="display:inline-block;background:#00d4ff;color:#080812;font-weight:700;padding:12px 32px;border-radius:8px;text-decoration:none">Open QuantumVerse</a>
          </div>
          <p style="color:#4a4a5a;font-size:12px;margin-top:32px;text-align:center">You're receiving this because you signed up at quantumverse.ai</p>
        </div>
        """,
    },
    "streak_reminder": {
        "subject": "Don't break your streak! 🔥 {streak} days strong",
        "body": """
        <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#080812;color:#fff;padding:32px;border-radius:16px">
          <h2 style="color:#f97316">🔥 {name}, keep your {streak}-day streak alive!</h2>
          <p style="color:#a0a0b0">You've been on a roll. Complete just one lesson or quiz today to keep going!</p>
          <div style="text-align:center;margin-top:24px">
            <a href="{app_url}/learn" style="display:inline-block;background:#f97316;color:#fff;font-weight:700;padding:12px 32px;border-radius:8px;text-decoration:none">Continue Learning</a>
          </div>
        </div>
        """,
    },
    "level_up": {
        "subject": "🎉 Congratulations! You reached Level {level} on QuantumVerse",
        "body": """
        <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#080812;color:#fff;padding:32px;border-radius:16px">
          <div style="text-align:center;margin-bottom:24px">
            <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#a855f7);display:inline-flex;align-items:center;justify-content:center;font-size:36px;font-weight:900;color:#080812">{level}</div>
          </div>
          <h2 style="color:#00d4ff;text-align:center">Level {level} Unlocked!</h2>
          <p style="color:#a0a0b0;text-align:center">{name}, you've reached Level {level} with {xp} XP. Keep pushing!</p>
          <div style="text-align:center;margin-top:24px">
            <a href="{app_url}/profile" style="display:inline-block;background:#00d4ff;color:#080812;font-weight:700;padding:12px 32px;border-radius:8px;text-decoration:none">View Profile</a>
          </div>
        </div>
        """,
    },
}


async def send_email(to: str, template: str, variables: dict) -> bool:
    """Send a templated HTML email."""
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        log.info(f"Email skipped (SMTP not configured): {template} -> {to}")
        return False
    tpl = EMAIL_TEMPLATES.get(template)
    if not tpl:
        return False
    app_url = getattr(settings, "APP_URL", "https://quantumverse.ai")
    body = tpl["body"].format(app_url=app_url, **variables)
    subject = tpl["subject"].format(**variables)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = settings.SMTP_FROM
    msg["To"]      = to
    msg.attach(MIMEText(body, "html"))
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
            s.starttls()
            s.login(settings.SMTP_USER, settings.SMTP_PASS)
            s.sendmail(settings.SMTP_FROM, [to], msg.as_string())
        return True
    except Exception as exc:
        log.error(f"Email send failed: {exc}")
        return False


async def send_welcome(email: str, name: str) -> bool:
    return await send_email(email, "welcome", {"name": name})

async def send_level_up(email: str, name: str, level: int, xp: int) -> bool:
    return await send_email(email, "level_up", {"name": name, "level": level, "xp": xp})

async def send_streak_reminder(email: str, name: str, streak: int) -> bool:
    return await send_email(email, "streak_reminder", {"name": name, "streak": streak})
