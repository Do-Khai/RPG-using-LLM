import json
import logging
import os
from prompt.prompt_chat import PROMPT_CHAT
from models.chat_schema import ChatRequest
from utils import MODEL_NAME
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prepare_payload_chat(req: ChatRequest) -> dict:
    """
    Chuẩn bị payload chat để gửi đến mô hình.
    """
    system_prompt_content = f"""
    {PROMPT_CHAT}
    ---
    ## ⚙️ BỐI CẢNH NGƯỜI CHƠI HIỆN TẠI
    - **UserID**: {req.user_id} (Lưu ý: Không trộn lẫn dữ liệu với người chơi khác)
    - **Các vùng đất và các thông tin chi tiết của các vùng đất đó trong game**: {json.dumps(req.all_region_data, ensure_ascii=False)}
    - **Chỉ số hiện tại**: {json.dumps(req.current_stats, ensure_ascii=False)}
    - **Chỉ số khi lên cấp**: {json.dumps(req.next_stats, ensure_ascii=False)}
    - **State hiện tại của người chơi**: {json.dumps(req.user_state, ensure_ascii=False)}
    ---
    """
    messages = [
        {"role": "system", "content": system_prompt_content}
    ]
    messages.extend(req.recent_messages)
    messages.append(
        {"role": "user", "content": req.message}
    )
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
    }
    return payload 