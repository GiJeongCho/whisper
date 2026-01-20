from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
import shutil
import os
import uuid
from .main import get_stt_engine

router_v1 = APIRouter(
    prefix="/v1",
    tags=["whisper"],
)

@router_v1.post("/stt", status_code=status.HTTP_200_OK)
async def speech_to_text(
    file: UploadFile = File(...),
    language: str = Form("korean")
):
    # 파일 확장자 확인
    if not file.filename.endswith((".wav", ".mp3", ".m4a")):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # 임시 파일 저장 경로
    temp_file_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
    
    try:
        # 업로드된 파일을 임시 파일로 저장
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # STT 엔진 실행
        engine = get_stt_engine()
        result = engine.transcribe(temp_file_path, language=language)
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # 처리 완료 후 임시 파일 삭제
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
