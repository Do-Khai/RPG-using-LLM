#services/battle_service.py
from prompt.prompt_battle import PROMPT_BATTLE
import json
import logging
import os
from utils import BATTLE_MODEL
from models.battle_schema import BattleRequest
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def prepare_payload_battle(req: BattleRequest) -> dict:
    """
    Chuẩn bị payload battle để gửi đến mô hình.
    """
    system_prompt_content = PROMPT_BATTLE.strip()
    
    user_prompt = f"""
    ---
    ## THÔNG SỐ
    - **Loại trận đấu**: {req.battleType.value}
    - **player**: Tên: {req.playerDisplayName}\n, 
    Chỉ số: {req.playerStats}\n
    - **enemy**: Tên: {req.enemyDisplayName}\n, 
    Chỉ số: {req.enemyStats}
    ---
    """
    payload = {
        "model": BATTLE_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt_content},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "max_token": 800,
        "top_p": 0.8,  
    }
    logging.info(f"Gửi payload tới Ollama với player1: {req.playerDisplayName} và player2: {req.enemyDisplayName}" )
    logging.info(f"Thông số của player:\n {req.playerStats}\n")
    logging.info(f"Thông số của enemy:\n {req.enemyStats}\n")
    return payload 


    