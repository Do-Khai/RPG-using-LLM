import httpx
import os 
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_CLOUD")
MODEL_NAME = os.getenv("MODEL_NAME")
BATTLE_MODEL = os.getenv("BATTLE_MODEL")

@retry(
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TimeoutException)),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5),
    reraise=True 
)
async def call_ollama(payload: dict) -> dict:
    """
    Gửi payload đến Ollama và xử lý response.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            OLLAMA_URL,
            headers={"Authorization": f"Bearer {os.getenv('OLLAMA_KEY')}"},
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        return response.json()