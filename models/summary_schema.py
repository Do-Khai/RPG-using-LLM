from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union


class SummaryRequest(BaseModel):
    user_id: str = Field(..., description="ID của người chơi", json_schema_extra={"example": "b4fcff01-b5ab-4c29-bdef-f3c8119f1cb6"})
    user_state: Dict[str, Any] = Field(..., description="Trạng thái tổng thể của người chơi trong game.", json_schema_extra={"example": {
        "level": 5, "exp": 1250, "currentRegionCode": "VALORIA", "faction": "LIGHT", "inventory": ["Health Potion", "Sword of Light"]
    }})
    recent_messages: Optional[List[Dict[str, str]]] = Field(None, description="Lịch sử các tin nhắn gần đây giữa người chơi và AI để duy trì ngữ cảnh.", json_schema_extra={"example": [
        {"role": "user", "content": "Tôi nên đi đâu tiếp theo?"},
        {"role": "assistant", "content": "{\"type\":\"STORY\",\"story\":\"Bạn thấy một con đường mòn dẫn vào khu rừng tối...\"}"}
    ]})