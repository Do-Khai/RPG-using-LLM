import json
import logging
import os
from prompt.prompt_summary import PROMPT_SUMMARY
from models.summary_schema import SummaryRequest
from utils import MODEL_NAME
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prepare_payload_summary(req: SummaryRequest) -> dict:
    """
    Chuẩn bị payload chat để gửi đến mô hình.
    """
    system_prompt_content = f"""
    {PROMPT_SUMMARY}
    ---
    ## ⚙️ BỐI CẢNH NGƯỜI CHƠI HIỆN TẠI
    - **UserID**: {req.user_id} (Lưu ý: Không trộn lẫn dữ liệu với người chơi khác)
    - **State hiện tại của người chơi**: {json.dumps(req.user_state, ensure_ascii=False)}
    - **Story cần tóm tắt thêm**: {json.dumps(req.recent_messages, ensure_ascii=False)}
    ---
    """
    messages = [
        {"role": "system", "content": system_prompt_content}
    ]
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
    }
    return payload 