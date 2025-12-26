from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    user_id: str = Field(
        ...,
        description="ID của người chơi",
        json_schema_extra={"example": "b4fcff01-b5ab-4c29-bdef-f3c8119f1cb6"},
    )
    message: str = Field(
        ...,
        description="Lệnh người chơi vừa gửi",
        json_schema_extra={"example": "/choose 1"},
    )
    all_region_data: List[Dict[str, Any]] = Field(
        ...,
        description="Danh sách tất cả các vùng đất trong game và thông tin chi tiết.",
        json_schema_extra={
            "example": [
                {
                    "code": "VALORIA",
                    "name": "Thành Valoria",
                    "description": "Thành phố thánh khởi đầu của hiệp sĩ Ánh Sáng. Valoria phát hiện dấu hiệu Phong Ấn Ánh Sáng bị suy yếu. Các hiệp sĩ điều tra nguyên nhân và phát hiện phe Dark đang tìm cách đánh cắp Tinh Thạch Khởi Nguyên. Người chơi bắt đầu hành trình bằng việc điều tra các đợt quái xâm nhập, cứu dân khỏi bóng ma lạc lối và khám phá thư viện cổ, biết về tiên tri Ma Thần Eclipse sẽ trở lại. Mục tiêu là bảo vệ Tinh Thạch Khởi Nguyên khỏi tay Dark.\nNPC:\n- Kaelen: Hiệp sĩ trưởng Valoria, giao nhiệm vụ chính và hướng dẫn ban đầu.\n- Liora: Linh mục trưởng Valoria, cung cấp thông tin tiên tri về ánh sáng và bóng tối.\n- Darius: Huấn luyện kỹ năng chiến đấu cơ bản. Có thể đưa nhiệm vụ phụ bảo vệ dân làng.\n- Elowen: Người tìm kiếm thông tin về quái vật lạc lối. Hướng dẫn cách sử dụng thẻ nhiệm vụ.\n- Fenric: Cung cấp nhiệm vụ phụ thu thập vật phẩm trong thành.",
                    "levelRequired": 1,
                    "faction": "LIGHT",
                    "connectedRegions": ["CELESTRA"],
                    "isStartingRegion": True,
                }
            ]
        },
    )
    current_stats: Dict[str, Any] = Field(
        ...,
        description="Các chỉ số hiện tại của người chơi.",
        json_schema_extra={
            "example": {
                "hp": 120.0,
                "atk": 90.0,
                "def": 30.0,
                "crit": 5.05,
                "critDamage": 240.0,
                "dodge": 10.0,
                "speed": 24.0,
            }
        },
    )
    next_stats: Dict[str, Any] = Field(
        ...,
        description="Các chỉ số của người chơi khi lên cấp độ tiếp theo.",
        json_schema_extra={
            "example": {
                "hp": 135.0,
                "atk": 98.0,
                "def": 35.0,
                "crit": 5.50,
                "critDamage": 245.0,
                "dodge": 11.0,
                "speed": 25.0,
            }
        },
    )
    user_state: Dict[str, Any] = Field(
        ...,
        description="Trạng thái tổng thể của người chơi trong game.",
        json_schema_extra={
            "example": {
                "level": 5,
                "exp": 1250,
                "currentRegionCode": "VALORIA",
                "faction": "LIGHT",
                "inventory": ["Health Potion", "Sword of Light"],
            }
        },
    )
    recent_messages: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Lịch sử các tin nhắn gần đây giữa người chơi và AI để duy trì ngữ cảnh.",
        json_schema_extra={
            "example": [
                {"role": "user", "content": "Tôi nên đi đâu tiếp theo?"},
                {
                    "role": "assistant",
                    "content": '{"type":"STORY","story":"Bạn thấy một con đường mòn dẫn vào khu rừng tối..."}',
                },
            ]
        },
    )
    last_story: Optional[Dict[str, Any]] = Field(
        None,
        description="Đối tượng JSON của câu chuyện/nhiệm vụ cuối cùng mà AI đã tạo ra.",
        json_schema_extra={
            "example": {
                "type": "STORY",
                "story": "Kaelen, hiệp sĩ trưởng, tiến lại gần bạn và nói: 'Chúng tôi cần sự giúp đỡ của bạn...'",
                "choices": [
                    {"id": 1, "text": "Tôi sẽ giúp."},
                    {"id": 2, "text": "Để tôi suy nghĩ đã."},
                ],
            }
        },
    )
