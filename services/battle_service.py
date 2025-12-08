#services/battle_service.py
from prompt.prompt_battle import PROMPT_BATTLE
import json
import logging
import random
from utils import BATTLE_MODEL
from models.battle_schema import BattleRequest, PlayerStats
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Character:
    """Lớp nội bộ để mô phỏng nhân vật trong trận đấu."""
    def __init__(self, name: str, stats: PlayerStats):
        self.name = name
        self.hp = stats.hp
        self.atk = stats.atk
        self.defence = stats.defence
        self.crit_percentage = stats.critPercentage
        self.crit_damage = stats.critDamage
        self.dodge = stats.dodge
        self.speed = stats.speed

def _simulate_battle_in_code(player_name: str, player_stats: PlayerStats, enemy_name: str, enemy_stats: PlayerStats) -> dict:
    """
    Mô phỏng toàn bộ trận đấu bằng code và trả về một "nhật ký trận đấu" (battle log).
    LLM sẽ chỉ làm nhiệm vụ điền mô tả vào nhật ký này.
    """
    player = Character(player_name, player_stats)
    enemy = Character(enemy_name, enemy_stats)

    hp_start_player = player.hp
    hp_start_enemy = enemy.hp

    actors = [player, enemy] if player.speed >= enemy.speed else [enemy, player]
    turns_log = []
    winner = ""
    max_turns = 12 

    for i in range(max_turns):
        attacker = actors[i % 2]
        defender = actors[(i + 1) % 2]

        damage = 0
        damage_blocked = 0

        # Mô phỏng một lượt tấn công
        if random.uniform(0, 100) >= defender.dodge:
            damage = attacker.atk
            if random.uniform(0, 100) < attacker.crit_percentage:
                damage = attacker.atk * (attacker.crit_damage / 100)

            if random.uniform(0, 100) < 10:
                damage_blocked = int(damage * (defender.defence / 100))

            final_damage = damage - damage_blocked
            if final_damage > 0:
                defender.hp = max(0, defender.hp - final_damage)

        # Ghi lại log của lượt đấu
        actor_role = 'player' if attacker is player else 'enemy'
        turn_data = {
            "turn": i + 1,
            "actor": actor_role,
            "description": "...",
            "damage": round(damage),
            "damageBlocked": round(damage_blocked),
            "playerHp": round(player.hp),
            "enemyHp": round(enemy.hp)
        }
        turns_log.append(turn_data)

        if defender.hp <= 0:
            # Gán 'player' hoặc 'enemy' cho người chiến thắng
            winner = 'player' if attacker is player else 'enemy'
            break
    
    # Nếu không ai thắng sau max_turns, kết quả là hòa
    if not winner:
        winner = ""

    # Xây dựng cấu trúc battle log hoàn chỉnh
    battle_log = {
        "type": "battle",
        "description": f"Trận đấu giữa {player_name} và {enemy_name}",
        "status": "DONE",
        "combat": {
            "player": {"name": player_name, "hpStart": hp_start_player, "hpEnd": round(player.hp)},
            "enemy": {"name": enemy_name, "hpStart": hp_start_enemy, "hpEnd": round(enemy.hp)},
            "turns": turns_log,
            "winner": winner
        }
    }
    return battle_log

def prepare_payload_battle(req: BattleRequest) -> dict:
    """
    Bước 1: Mô phỏng trận đấu bằng code để tạo battle log.
    Bước 2: Chuẩn bị payload với battle log để LLM tường thuật.
    """
    logging.info(f"Bắt đầu mô phỏng trận đấu giữa {req.playerDisplayName} và {req.enemyDisplayName} bằng code.")
    battle_log = _simulate_battle_in_code(
        req.playerDisplayName, req.playerStats, 
        req.enemyDisplayName, req.enemyStats   
    )
    battle_log_json_str = json.dumps(battle_log, separators=(',', ':'))

    # Bước 2: Chuẩn bị payload cho LLM
    system_prompt_content = PROMPT_BATTLE

    payload = {
        "model": BATTLE_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt_content},
            {"role": "user", "content": battle_log_json_str}
        ],
        "stream": False
    }
    logging.info(f"Đã tạo xong battle log. Chuẩn bị gửi tới LLM để tường thuật.")
    logging.info(f"Thông số của player:\n {req.playerStats}\n")
    logging.info(f"Thông số của enemy:\n {req.enemyStats}\n")
    return payload 