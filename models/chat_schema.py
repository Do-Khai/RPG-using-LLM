from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    user_id: str
    message: str                     
    all_region_data: List[Dict[str, Any]]
    current_stats: Dict[str, Any]
    next_stats: Dict[str, Any]
    user_state: Dict[str, Any]       
    recent_messages: Optional[List[Dict[str, str]]]
    last_story: Optional[Dict[str, Any]] = None  