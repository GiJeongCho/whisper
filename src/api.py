from fastapi import FastAPI
import uvicorn
import logging
from src.v1.router import router_v1

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(
    title="Whisper STT API",
    description="OpenAI Whisper Large-v3를 이용한 STT 서비스",
    version="1.0.0"
)

# 라우터 등록
app.include_router(router_v1)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8010, reload=True)

