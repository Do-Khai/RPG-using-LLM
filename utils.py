import httpx
import os 
import logging
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

OLLAMA_URL = os.getenv("OLLAMA_CLOUD")
MODEL_NAME = os.getenv("MODEL_NAME")
BATTLE_MODEL = os.getenv("BATTLE_MODEL")

API_KEYS = [
    os.getenv("OLLAMA_KEY_1"),
    os.getenv("OLLAMA_KEY_2"),
    os.getenv("OLLAMA_KEY_3"),
]
API_KEYS = [key for key in API_KEYS if key] 

if not API_KEYS:
    raise ValueError("Không tìm thấy OLLAMA_KEY nào trong file .env.")

@retry(
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5),
    reraise=True 
)
async def call_ollama(payload: dict) -> dict:
    """
    Gửi payload đến Ollama
    """
    last_exception = None
    for i, key in enumerate(API_KEYS):
        logging.info(f"Đang thử gọi API với key #{i+1}...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    OLLAMA_URL,
                    headers={"Authorization": f"Bearer {key}"},
                    json=payload,
                    timeout=300
                )
                response.raise_for_status()
                logging.info(f"Gọi API với key #{i+1} thành công.")
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [429, 403, 401]:
                logging.warning(f"Key #{i+1} gặp lỗi {e.response.status_code}. Đang chuyển sang key tiếp theo...")
                last_exception = e
                continue 
            else:
                raise e
    logging.error("Tất cả các API key đều đã thất bại.")
    if last_exception:
        raise last_exception
    raise Exception("Không thể kết nối đến Ollama sau khi đã thử tất cả các key.")