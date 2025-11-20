import httpx
import os 
from dotenv import load_dotenv
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_CLOUD")
MODEL_NAME = os.getenv("MODEL_NAME")

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