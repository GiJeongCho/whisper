# whisper_download.py
from huggingface_hub import snapshot_download
import os

# 다운로드할 모델 ID
model_id = "openai/whisper-large-v3"

# 저장할 로컬 경로 (현재 폴더 내의 whisper-large-v3 폴더)
local_dir = "./models/whisper-large-v3"

print(f"'{model_id}' 모델 다운로드를 시작합니다...")

# 모델 다운로드 실행
snapshot_download(
    repo_id=model_id,
    local_dir=local_dir,
    local_dir_use_symlinks=False, # 심볼릭 링크 대신 실제 파일로 다운로드
    ignore_patterns=["*.msgpack", "*.h5", "*.tflite"] # 불필요한 파일 제외 (선택 사항)
)

print(f"다운로드 완료! 모델이 '{os.path.abspath(local_dir)}'에 저장되었습니다.")