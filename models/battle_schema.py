from pydantic import BaseModel, Field
from typing import Dict, Any
from enum import Enum

class BattleType(str, Enum):
    CASUAL = "CASUAL"
    RANKED = "RANKED"   
    TOURNAMENT = "TOURNAMENT"

class BattleRequest(BaseModel):
    battleType: BattleType = Field(..., description="Loại trận đấu")
    playerDisplayName: str = Field(..., json_schema_extra={"example":"Knight001"})
    playerStats: Dict[str, Any] = Field(..., description="Chỉ số người chơi 1.", json_schema_extra={"example": {
        "hp": 120.0, "atk": 90.0, "def": 30.0, "critPercentage": 5.05, "critDamage": 240.0, "dodge": 10.0, "speed": 24.0
    }})
    enemyDisplayName: str = Field(..., json_schema_extra={"example":"MageX"})
    enemyStats: Dict[str, Any] =  Field(..., description="Chỉ số người chơi 2.", json_schema_extra={"example": {
        "hp": 120.0, "atk": 90.0, "def": 30.0, "critPercentage": 5.05, "critDamage": 240.0, "dodge": 10.0, "speed": 24.0
    }})