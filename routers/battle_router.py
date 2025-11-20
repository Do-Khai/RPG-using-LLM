from fastapi import APIRouter, HTTPException
from models.battle_schema import BattleRequest
from services.battle_service import prepare_payload_battle
from utils import call_ollama, MODEL_NAME
import json
import os
import logging
import httpx
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



router = APIRouter()

@router.post("/player-battle", tags=["LLM Generate for Combat between 2 players"])
async def generate_battle(req: BattleRequest):
    """
    Service nhận input từ backend, gọi đến LLM để sinh combat và trả về JSON hợp lệ.

    **Request Body:**
    - `battleType` (str, **bắt buộc**): Loại trận đấu. Các giá trị hợp lệ: "CASUAL"
    - `firstUserDisplayName` (str, **bắt buộc**): Tên hiển thị của người chơi thứ nhất.
    - `firstUserStats` (Dict, **bắt buộc**): Dictionary chứa các chỉ số của người chơi thứ nhất.
        - `hp` (float): Máu.
        - `atk` (float): Sức tấn công.
        - `def` (float): Phòng thủ.
        - `crit` (float): Tỉ lệ chí mạng (0-100).
        - `critDamage` (float): Sát thương chí mạng.
        - `dodge` (float): Tỉ lệ né đòn (0-100).
        - `speed` (float): Tốc độ.
    - `secondUserDisplayName` (str, **bắt buộc**): Tên hiển thị của người chơi thứ hai.
    - `secondUserStats` (Dict, **bắt buộc**): Dictionary chứa các chỉ số của người chơi thứ hai (cấu trúc tương tự `firstUserStats`).
    """
    try:
        payload = prepare_payload_battle(req)
        start_time = time.time()
        response = await call_ollama(payload)
        response_content = response.get("message", {}).get("content", "") or response.get("response", "")
        end_time = time.time()
        response_time = end_time - start_time
        logging.info(f"Thời gian phản hồi của mô hình {MODEL_NAME}: {response_time:.2f}s")
        
        if not response_content:
            raise HTTPException(status_code=500, detail="Ollama trả về response rỗng. Kiểm tra lại model được load và chạy đúng chưa.")
        
         # Parse JSON từ response
        try:
            cleaned_content = response_content.strip()
            if cleaned_content.startswith("```json"):
                start_index = cleaned_content.find('{')
                end_index = cleaned_content.rfind('}')
                if start_index != -1 and end_index != -1:
                    cleaned_content = cleaned_content[start_index:end_index+1]
            parsed = json.loads(cleaned_content)
        except Exception:
            raise HTTPException(status_code=500, detail=f"Phản hồi từ model không phải JSON hợp lệ: {response_content}")

        return parsed

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            logging.warning(f"Ollama API rate limit exceeded cho user {req.user_id}.")
            raise HTTPException(status_code=429, detail="Quá nhiều yêu cầu đến dịch vụ LLM, vui lòng thử lại sau.")
        logging.error(f"Lỗi HTTP từ Ollama: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Lỗi HTTP từ Ollama: {e.response.status_code}")
    except Exception as e:
        logging.error(f"Lỗi không mong muốn: {e}")
        raise HTTPException(status_code=500, detail=f"Ollama request thất bại: {e}")
