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
    player_stats_dict = req.playerStats
    enemy_stats_dict = req.enemyStats
    system_prompt_content = PROMPT_BATTLE.strip()
    
    user_prompt = f"""
    ---
    ## ⚙️ THÔNG SỐ
    - **Loại trận đấu**: {req.battleType.value}
    - **player**: Tên: {req.playerDisplayName}\n, 
    Chỉ số: {player_stats_dict}\n
    - **enemy**: Tên: {req.enemyDisplayName}\n, 
    Chỉ số: {enemy_stats_dict}
    ---
    """
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt_content},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "max_token": 800
    }
    logging.info(f"Gửi payload tới Ollama với player1: {req.playerDisplayName} và player2: {req.enemyDisplayName}" )
    logging.info(f"Thông số của player:\n {req.playerStats}\n")
    logging.info(f"Thông số của enemy:\n {req.enemyStats}\n")
    return payload 


    