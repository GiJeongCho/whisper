# Whisper STT API

OpenAI의 `whisper-large-v3` 모델을 사용하여 음성 파일을 텍스트로 변환해주는 FastAPI 기반 API 서버입니다.

## 주요 기능
- **STT 추론**: WAV, MP3 등의 음성 파일을 텍스트로 변환 (타임스탬프 포함)
- **언어 선택**: `language` 파라미터를 통해 전사할 언어 지정 가능
- **Docker 지원**: Podman/Docker를 통해 간편하게 컨테이너화 가능

## 실행 방법

### 1. 로컬 환경 실행 (uv 사용 시)
```bash
# 의존성 설치 및 가상환경 구축
uv sync

# API 실행
uv run src/api.py
```

### 2. 컨테이너 환경 실행 (Podman)
`uv`를 사용하여 빌드 속도가 최적화되었습니다. 모델 파일은 호스트 시스템의 경로를 컨테이너 내부(`/app/models/whisper-large-v3`)로 마운트하여 사용합니다.

```bash
# 이미지 빌드
podman build -t whisper-stt-api .

# 컨테이너 실행
podman run -d \
  --name whisper-api \
  --device nvidia.com/gpu=all \
  -p 8010:8010 \
  -v /home/pps-nipa/NIQ/fish/whisper/src/resoursces/models/whisper-large-v3:/app/models/whisper-large-v3:Z \
  whisper-stt-api
```

## API 사용법

### STT 변환 (`POST /v1/stt`)
음성 파일을 업로드하여 텍스트 결과를 가져옵니다.

- **URL**: `http://localhost:8010/v1/stt`
- **Method**: `POST`
- **Payload**:
  - `file`: 음성 파일 (wav, mp3 등)
  - `language`: 언어 코드 (기본값: `korean`)

**예시 (cURL):**
```bash
curl -X 'POST' \
  'http://localhost:8010/v1/stt' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@audio_file.wav' \
  -F 'language=korean'
```

## API 문서
서버가 실행 중일 때 아래 주소에서 Swagger UI를 확인할 수 있습니다.
- `http://localhost:8010/docs`

