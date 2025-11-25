from pydantic import BaseModel, Field
from enum import Enum

class BattleType(str, Enum):
    CASUAL = "CASUAL"
    RANKED = "RANKED"   
    TOURNAMENT = "TOURNAMENT"

class PlayerStats(BaseModel):
    hp: float = Field(..., description="Máu của người chơi", gt=0, json_schema_extra={"example": 120.0})
    atk: float = Field(..., description="Sát thương gây ra", json_schema_extra={"example": 90.0})
    defence: float = Field(..., alias='def', description="Chỉ số phòng thủ", json_schema_extra={"example": 30.0})
    crit: float = Field(..., description="Tỉ lệ chí mạng", ge=0.0, le=100.0, json_schema_extra={"example": 5.05})
    critDamage: float = Field(..., description="Sát thương chí mạng", json_schema_extra={"example": 240.0})
    dodge: float = Field(..., description="Tỉ lệ né đòn", json_schema_extra={"example": 10.0})
    speed: float = Field(..., description="Tốc độ", json_schema_extra={"example": 24.0})
    


class BattleRequest(BaseModel):
    battleType: BattleType = Field(..., description="Loại trận đấu")
    playerDisplayName: str = Field(..., json_schema_extra={"example":"Knight001"})
    playerStats: PlayerStats
    enemyDisplayName: str = Field(..., json_schema_extra={"example":"MageX"})
    enemyStats: PlayerStats