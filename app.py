import os
from fastapi import FastAPI
from routers import chat_router, battle_router, summary_router
from dotenv import load_dotenv

load_dotenv()

required_env_vars = ["OLLAMA_CLOUD", "MODEL_NAME", "BATTLE_MODEL"]
for var in required_env_vars:
    if not os.getenv(var):
        raise RuntimeError(f"Thiếu biến môi trường: {var}")

app = FastAPI(title="RPG Quest Proxy Service")

app.include_router(chat_router.router, prefix="/api/v1")
app.include_router(battle_router.router, prefix="/api/v1")
app.include_router(summary_router.router, prefix="/api/v1")


@app.get("/health", include_in_schema=False)
@app.head("/health", include_in_schema=False)
async def health_check():
    return {"ok": True}
