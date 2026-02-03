from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class Metadata(BaseModel):
    channel: str
    language: str
    locale: str

class InputFormat(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Metadata

class OutputFormat(BaseModel):
    status: str
    reply: Optional[str] = None
    action: Optional[str] = None
