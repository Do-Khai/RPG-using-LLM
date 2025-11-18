from fastapi import FastAPI, HTTPException
import json
from prompt import PROMPT
from schema import ChatRequest
from dotenv import load_dotenv
import httpx
import time 
import os
import logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

app = FastAPI(title="RPG Quest Proxy Service")
@app.get("/health", include_in_schema=False)
@app.head("/health", include_in_schema=False)
async def health_check():
    return {"ok": True}


@app.post("/api/v1/chat", tags=["LLM Generate"])
async def chat_with_ollama(req: ChatRequest):
    """
    Service nhận input từ backend, gọi đến LLM để sinh nội dung game và trả về JSON hợp lệ.

    **Request Body:**

    - `user_id` (str, **bắt buộc**): ID định danh duy nhất của người chơi.
    - `message` (str, **bắt buộc**): Lệnh hoặc tin nhắn người chơi vừa gửi (ví dụ: "/start", "/choose 1").
    - `all_region_data` (List[Dict], **bắt buộc**): Danh sách các đối tượng JSON chứa dữ liệu chi tiết của tất cả các vùng.
    - `current_stats` (Dict, **bắt buộc**): Dictionary chứa các chỉ số hiện tại của người chơi (level, hp, atk...).
    - `next_stats` (Dict, **bắt buộc**): Dictionary chứa các chỉ số của người chơi ở level tiếp theo.
    - `user_state` (Dict, **bắt buộc**): Dictionary chứa state tổng của người chơi (faction, gender,...).
    - `recent_messages` (Optional[List[Dict]]): Lịch sử các tin nhắn gần đây giữa user và assistant.
    - `last_story` (Optional[Dict]): JSON của story/quest gần nhất mà model đã sinh ra.
    """
    system_prompt_content = f"""
{PROMPT}

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
    logging.info(f"Gửi payload tới Ollama với user {req.user_id}")

    try:
        async with httpx.AsyncClient() as client:
            start_time = time.time()
            response = await client.post(os.getenv("OLLAMA_CLOUD"), 
                                         headers={"Authorization": f"Bearer {os.getenv('OLLAMA_KEY')}"}, 
                                         json=payload, 
                                         timeout=300)
            response.raise_for_status()
            
            data = response.json()
            response_content = data.get("message", {}).get("content", "") or data.get("response", "")
            end_time = time.time()
            response_time = end_time - start_time
            logging.info(f"Thời gian phản hồi của mô hình {MODEL_NAME}: {response_time:.2f}s")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama request thất bại: {e}")

    if not response_content:
        raise HTTPException(status_code=500, detail="Ollama trả về response rỗng. Kiểm tra lại model được load và chạy đúng chưa.")

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
