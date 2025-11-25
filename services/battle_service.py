from prompt.prompt_battle import PROMPT_BATTLE
import json
import logging
import os
from utils import MODEL_NAME
from models.battle_schema import BattleRequest
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def prepare_payload_battle(req: BattleRequest) -> dict:
    """
    Chuẩn bị payload battle để gửi đến mô hình.
    """
    player_stats_dict = req.playerStats.model_dump(by_alias=True)
    enemy_stats_dict = req.enemyStats.model_dump(by_alias=True)
    system_prompt_content = f"""
    {PROMPT_BATTLE}
    ---
    ## ⚙️ THÔNG SỐ CỦA 2 NGƯỜI CHƠI
    - **Loại trận đấu**: {req.battleType.value}
    - **Người chơi 1**: Tên: {req.playerDisplayName}, Chỉ số: {json.dumps(player_stats_dict, ensure_ascii=False)}
    - **Người chơi 2**: Tên: {req.enemyDisplayName}, Chỉ số: {json.dumps(enemy_stats_dict, ensure_ascii=False)}
    ---
    """
    messages = [{"role": "system", "content": system_prompt_content}]
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "max_token": 1200
    }
    logging.info(f"Gửi payload tới Ollama với player1: {req.playerDisplayName} và player2: {req.enemyDisplayName}" )
    return payload 


    