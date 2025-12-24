import httpx
import os 
import logging
import time
import threading
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

OLLAMA_URL = os.getenv("OLLAMA_CLOUD")
MODEL_NAME = os.getenv("MODEL_NAME")
BATTLE_MODEL = os.getenv("BATTLE_MODEL")

# API_KEYS = [
#     os.getenv("OLLAMA_KEY_1"),
#     os.getenv("OLLAMA_KEY_2"),
#     os.getenv("OLLAMA_KEY_3"),
# ]

# class KeyManager:
#     def __init__(self, keys: list, cooldown_seconds: int = 3600):
#         if not keys:
#             raise ValueError("Danh sách API key không được rỗng.")
#         self._keys = keys
#         self._cooldown_seconds = cooldown_seconds
#         self._key_status = {key: {"available": True, "cooldown_until": 0} for key in keys}
#         self._lock = threading.Lock()
#         self._current_index = 0

#     def get_next_key(self):
#         with self._lock:
#             for _ in range(len(self._keys)):
#                 key = self._keys[self._current_index]
#                 status = self._key_status[key]
                
#                 # Nếu key đang trong thời gian cooldown, kiểm tra xem đã hết chưa
#                 if not status["available"] and time.time() < status["cooldown_until"]:
#                     self._current_index = (self._current_index + 1) % len(self._keys)
#                     continue
                
#                 status["available"] = True # Reset trạng thái nếu đã hết cooldown
#                 self._current_index = (self._current_index + 1) % len(self._keys)
#                 return key
#             return None # Không có key nào khả dụng

#     def set_key_cooldown(self, key: str):
#         with self._lock:
#             if key in self._key_status:
#                 logging.warning(f"Key ...{key[-4:]} đang được đưa vào trạng thái cooldown trong {self._cooldown_seconds} giây.")
#                 self._key_status[key]["available"] = False
#                 self._key_status[key]["cooldown_until"] = time.time() + self._cooldown_seconds


# valid_keys = [key for key in API_KEYS if key] 
# if not valid_keys:
#     raise ValueError("Không tìm thấy OLLAMA_KEY nào trong file .env.")
# key_manager = KeyManager(valid_keys)


@retry(
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5),
    reraise=True 
)
async def call_ollama(payload: dict) -> dict:
    """
    Gửi payload đến Ollama, sử dụng KeyManager để xoay vòng key một cách tối ưu.
    """
    # for _ in range(len(key_manager._keys)): # Thử tối đa số lượng key đang có
    #     key = key_manager.get_next_key()
    #     if not key:
    #         raise Exception("Tất cả các API key đều đang trong thời gian cooldown.")

    #     logging.info(f"Đang sử dụng key ...{key[-4:]}")
    try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    OLLAMA_URL,
                    # headers={"Authorization": f"Bearer {key}"},
                    json=payload,
                    timeout=300.0
                )
                response.raise_for_status()
                # logging.info(f"Gọi API với key ...{key[-4:]} thành công.")
                return response.json()
    except httpx.HTTPStatusError as e:
            logging.error(f"Ollama API Error: {e.response.status_code} - {e.response.text}")
            raise e

    # raise Exception("Tất cả các API key đều đã thất bại hoặc đang trong thời gian cooldown.")