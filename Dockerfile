# 1. 빌드 스테이지
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# 시스템 의존성 설치 (ffmpeg 등)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 설치 (캐싱 활용)
# uv.lock이 없는 경우를 대비해 pyproject.toml만 우선 사용
COPY pyproject.toml .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 2. 실행 스테이지 (이미지 경량화)
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/

# 시스템 라이브러리 (실행 시 필요)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# 환경 변수 설정
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV WHISPER_MODEL_PATH=/app/models/whisper-large-v3

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8010"]
