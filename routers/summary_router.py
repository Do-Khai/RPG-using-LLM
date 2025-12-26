from fastapi import APIRouter, HTTPException
from models.summary_schema import SummaryRequest
from services.summary_service import prepare_payload_summary
from utils import call_ollama, MODEL_NAME
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

router = APIRouter()


@router.post("/chat/summary", tags=["LLM Generation"])
async def generate_summary(req: SummaryRequest):
    """
    Service nhận input từ backend, gọi đến LLM để sinh nội dung game và trả về JSON hợp lệ.

    **Request Body:**

    - `user_id` (str, **bắt buộc**): ID định danh duy nhất của người chơi.
    - `user_state` (Dict, **bắt buộc**): Dictionary chứa state tổng của người chơi.
    - `recent_messages` (Optional[List[Dict]]): Lịch sử các tin nhắn gần đây giữa user và assistant.
    """

    try:
        payload = prepare_payload_summary(req)
        logging.info(f"Gửi payload summary tới Ollama với user {req.user_id}")

        start_time = time.time()
        response = await call_ollama(payload)
        response_content = response.get("message", {}).get(
            "content", ""
        ) or response.get("response", "")
        end_time = time.time()
        response_time = end_time - start_time
        logging.info(
            f"Thời gian phản hồi của mô hình {MODEL_NAME}: {response_time:.2f}s"
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
