"""Update lesson YouTube videos.

Revision ID: update_lesson_videos
Revises: remove_achievements
"""

from alembic import op


revision = "update_lesson_videos"
down_revision = "remove_achievements"
branch_labels = None
depends_on = None


LESSON_VIDEOS = {
    "Introduction to Quantum Computing": "https://www.youtube.com/watch?v=s2tGe7FSChE",
    "Classical vs Quantum Computing": "https://www.youtube.com/watch?v=NZD9APb7ZtY",
    "Bits vs Qubits": "https://www.youtube.com/watch?v=s2tGe7FSChE",
    "Superposition": "https://www.youtube.com/watch?v=WjjUfEpej-0",
    "Quantum Measurement": "https://www.youtube.com/watch?v=XxHxL5dPNyU",
    "Quantum States": "https://www.youtube.com/watch?v=s2tGe7FSChE",
    "The Bloch Sphere": "https://www.youtube.com/watch?v=WjjUfEpej-0",
    "Pauli-X Gate (Quantum NOT)": "https://www.youtube.com/watch?v=uNrPJ3_Mttc",
    "Pauli-Y Gate": "https://www.youtube.com/watch?v=uNrPJ3_Mttc",
    "Pauli-Z Gate": "https://www.youtube.com/watch?v=uNrPJ3_Mttc",
    "Hadamard Gate": "https://www.youtube.com/watch?v=WjjUfEpej-0",
    "Phase (S) Gate": "https://www.youtube.com/watch?v=ZvUD_KPjzLo",
    "T Gate": "https://www.youtube.com/watch?v=ZvUD_KPjzLo",
    "Rotation Gates (RX, RY, RZ)": "https://www.youtube.com/watch?v=qrNxFzLsqro",
    "Multiple Qubits": "https://www.youtube.com/watch?v=BiDJFkOFWvE",
    "CNOT Gate": "https://www.youtube.com/watch?v=YNLr6uIPHYA",
    "Controlled Gates": "https://www.youtube.com/watch?v=YNLr6uIPHYA",
    "Quantum Entanglement": "https://www.youtube.com/watch?v=pS69lqCMdy8",
    "Bell States": "https://www.youtube.com/watch?v=pS69lqCMdy8",
    "Deutsch-Jozsa Algorithm": "https://www.youtube.com/watch?v=QcK0GK7DUh8",
    "Grover's Search Algorithm": "https://www.youtube.com/watch?v=RDGUpC7bc7s",
    "Quantum Fourier Transform": "https://www.youtube.com/watch?v=0tmdEEl_Z2k",
    "Shor's Algorithm (Overview)": "https://www.youtube.com/watch?v=505AJguv7pM",
    "Quantum Teleportation": "https://www.youtube.com/watch?v=jBeFu8PHjgY",
    "Superdense Coding": "https://www.youtube.com/watch?v=XxHxL5dPNyU",
}


def upgrade():
    for title, youtube_url in LESSON_VIDEOS.items():
        op.execute(
            f"""
            UPDATE lessons
            SET youtube_url = '{youtube_url}'
            WHERE title = '{title.replace("'", "''")}'
            """
        )


def downgrade():
    for title in LESSON_VIDEOS:
        op.execute(
            f"""
            UPDATE lessons
            SET youtube_url = NULL
            WHERE title = '{title.replace("'", "''")}'
            """
        )
