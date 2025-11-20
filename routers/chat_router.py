from fastapi import APIRouter, HTTPException
from models.chat_schema import ChatRequest
from services.chat_service import prepare_payload_chat
from utils import call_ollama, MODEL_NAME
import json
import os
import logging
import httpx
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



router = APIRouter()

@router.post("/chat", tags=["LLM Generation"])
async def generate_chat(req: ChatRequest):
    """
    Service nhận input từ backend, gọi đến LLM để sinh nội dung game và trả về JSON hợp lệ.

    **Request Body:**

    - `user_id` (str, **bắt buộc**): ID định danh duy nhất của người chơi.
    - `message` (str, **bắt buộc**): Lệnh hoặc tin nhắn người chơi vừa gửi.
    - `all_region_data` (List[Dict], **bắt buộc**): Danh sách các đối tượng JSON chứa dữ liệu chi tiết của tất cả các vùng.
    - `current_stats` (Dict, **bắt buộc**): Dictionary chứa các chỉ số hiện tại của người chơi.
    - `next_stats` (Dict, **bắt buộc**): Dictionary chứa các chỉ số của người chơi ở level tiếp theo.
    - `user_state` (Dict, **bắt buộc**): Dictionary chứa state tổng của người chơi.
    - `recent_messages` (Optional[List[Dict]]): Lịch sử các tin nhắn gần đây giữa user và assistant.
    - `last_story` (Optional[Dict]): JSON của story/quest gần nhất mà model đã sinh ra.
    """

    try:
        payload = prepare_payload_chat(req)
        logging.info(f"Gửi payload tới Ollama với user {req.user_id}")

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