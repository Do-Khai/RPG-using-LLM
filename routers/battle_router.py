# routers/battle_router.py
from fastapi import APIRouter, HTTPException
from models.battle_schema import BattleRequest
from services.battle_service import prepare_payload_battle
from utils import call_ollama, BATTLE_MODEL
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


router = APIRouter()


@router.post("/player-battle", tags=["LLM Generation"])
async def generate_battle(req: BattleRequest):
    """
    Service nhận input từ backend, gọi đến LLM để sinh combat và trả về JSON hợp lệ.

    **Request Body:**
    - `battleType` (str, **bắt buộc**): Loại trận đấu. Các giá trị hợp lệ: "CASUAL"
    - `playerDisplayName` (str, **bắt buộc**): Tên hiển thị của người chơi thứ nhất.
    - `playerStats` (Dict, **bắt buộc**): Dictionary chứa các chỉ số của người chơi thứ nhất.
        - `hp` (float): Máu.
        - `atk` (float): Sức tấn công.
        - `def` (float): Phòng thủ.
        - `critPercentage` (float): Tỉ lệ chí mạng (0-100).
        - `critDamage` (float): Sát thương chí mạng.
        - `dodge` (float): Tỉ lệ né đòn (0-100).
        - `speed` (float): Tốc độ.
    - `enemyDisplayName` (str, **bắt buộc**): Tên hiển thị của người chơi thứ hai.
    - `enemyStats` (Dict, **bắt buộc**): Dictionary chứa các chỉ số của người chơi thứ hai (cấu trúc tương tự `playerStats`).
    """
    try:
        payload = prepare_payload_battle(req)
        start_time = time.time()
        response = await call_ollama(payload)
        response_content = response.get("message", {}).get(
            "content", ""
        ) or response.get("response", "")
        end_time = time.time()
        response_time = end_time - start_time
        logging.info(
            f"Thời gian phản hồi của mô hình {BATTLE_MODEL}: {response_time:.2f}s"
        )

        if not response_content:
            raise HTTPException(
                status_code=500,
                detail="Ollama trả về response rỗng. Kiểm tra lại model được load và chạy đúng chưa.",
            )

        # Parse JSON từ response
        try:
            start_index = response_content.find("{")
            end_index = response_content.rfind("}")
            if start_index != -1 and end_index != -1 and start_index < end_index:
                json_str = response_content[start_index : end_index + 1]
                parsed = json.loads(json_str)
            else:
                raise ValueError("Không tìm thấy đối tượng JSON hợp lệ trong phản hồi.")
        except (json.JSONDecodeError, ValueError):
            raise HTTPException(
                status_code=500,
                detail=f"Phản hồi từ model không phải JSON hợp lệ: {response_content}",
            )

        return parsed

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Lỗi không mong muốn: {e}")
        raise HTTPException(status_code=500, detail=f"Ollama request thất bại: {e}")
