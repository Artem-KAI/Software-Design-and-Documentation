from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    id: str
    username: str
    password: str

@dataclass
class Message:
    id: str
    conversation_id: str
    sender_id: str
    sender_name: str  # Додаємо після нашого JOIN
    text: str
    timestamp: str
    status: str = "sent"

@dataclass
class Conversation:
    id: str
    name: str
    participants: List[str]
    is_group: bool = False