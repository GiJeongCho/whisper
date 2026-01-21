# 베이스 이미지 설정 (CUDA 및 PyTorch 지원)
FROM docker.io/pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uv/bin/
ENV PATH="/uv/bin:$PATH"

# 시스템 의존성 설치 (ffmpeg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 설치 (uv가 관리하는 가상환경 생성)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# 소스 코드 복사
COPY src/ ./src/

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV WHISPER_MODEL_PATH=/app/models/whisper-large-v3

# API 실행 (uv run을 사용하여 안전하게 실행)
CMD ["uv", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8010"]
