# Whisper STT API

OpenAI의 `whisper-large-v3` 모델을 사용하여 음성 파일을 텍스트로 변환해주는 FastAPI 기반 API 서버입니다. `uv`를 사용하여 의존성 관리와 빌드 속도를 최적화했습니다.

## 주요 기능
- **STT 추론**: WAV, MP3 등의 음성 파일을 텍스트로 변환 (타임스탬프 포함)
- **고성능 디코딩**: 반복 환각(Hallucination) 방지 및 안정적인 파라미터 적용
- **Docker/Podman 지원**: 컨테이너화를 통한 간편한 배포 및 GPU 가속 지원

## 실행 방법

### 1. 로컬 환경 실행 (uv 사용)
가상환경 활성화 없이 `uv` 명령어로 즉시 실행 가능합니다.
```bash
# 의존성 설치 및 동기화
uv sync

# 서버 실행 (자동으로 가상환경 내 패키지 사용)
uv run uvicorn src.api:app --host 0.0.0.0 --port 8010 --reload
```

### 2. 컨테이너 환경 실행 (Podman)
GPU 가속을 위해 NVIDIA 컨테이너 툴킷이 설치되어 있어야 합니다.

#### 이미지 빌드
```bash
podman build -t whisper-stt-api .
```

#### 컨테이너 실행
호스트의 모델 폴더를 컨테이너 내부(`/app/models/whisper-large-v3`)로 마운트합니다.
```bash
podman run -d \
  --name whisper-api \
  --device nvidia.com/gpu=all \
  -p 8010:8010 \
  -v /home/pps-nipa/NIQ/fish/whisper/src/resoursces/models/whisper-large-v3:/app/models/whisper-large-v3:Z \
  whisper-stt-api
```

## API 사용법

### STT 변환 (`POST /v1/stt`)
음성 파일을 업로드하여 텍스트 결과를 JSON으로 반환받습니다.

- **Endpoint**: `http://localhost:8010/v1/stt`
- **Parameters**:
  - `file`: 음성 파일 (wav, mp3, m4a 등)
  - `language`: 언어 설정 (기본값: `korean`)

**cURL 테스트:**
```bash
curl -X 'POST' \
  'http://localhost:8010/v1/stt' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@sample.wav' \
  -F 'language=korean'
```

## API 문서 및 모니터링
- **Swagger UI**: [http://localhost:8010/docs](http://localhost:8010/docs)
- **Health Check**: [http://localhost:8010/health](http://localhost:8010/health)
