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


@app.post("/chat")
async def chat_with_ollama(req: ChatRequest):
    """
    Service nhận input từ backend
    -> Gọi Ollama
    -> Trả lại JSON story/quest/battle hợp lệ
    """
    system_prompt_content = f"""
{PROMPT}

---
## ⚙️ BỐI CẢNH NGƯỜI CHƠI HIỆN TẠI
- **UserID**: {req.user_id} (Lưu ý: Không trộn lẫn dữ liệu với người chơi khác)
- **Các vùng đất trong game**: {json.dumps(req.regions, ensure_ascii=False)}
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
        parsed = json.loads(response_content)
    except Exception:
        raise HTTPException(status_code=500, detail=f"Phản hồi từ model không phải JSON hợp lệ: {response_content}")

    return parsed
