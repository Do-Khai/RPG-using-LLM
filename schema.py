from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    user_id: str
    message: str                     # Lệnh player gửi (/start, /choose 1, /travel ...)
    regions: List[str]
    current_stats: Dict[str, Any]
    next_stats: Dict[str, Any]
    user_state: Dict[str, Any]       # Lưu state tổng: {faction, gender, level, region, quest_progress}
    recent_messages: List[Dict[str, str]]
    last_story: Optional[Dict[str, Any]] = None  # Lưu JSON story/quest gần nhất model sinh ra
