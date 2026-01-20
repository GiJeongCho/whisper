import torch
import logging
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os

logger = logging.getLogger(__name__)

class WhisperSTT:
    def __init__(self, model_path: str):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        logger.info(f"Loading Whisper model from {model_path} on {self.device}")
        
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_path,
            torch_dtype=self.torch_dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True
        )
        self.model.to(self.device)
        self.processor = AutoProcessor.from_pretrained(model_path)
        
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )

    def transcribe(self, audio_path: str, language: str = "korean"):
        generate_kwargs = {
            "language": language,
            "max_new_tokens": 445,
            "num_beams": 1,
            "condition_on_prev_tokens": False,
            "compression_ratio_threshold": 1.35,
            "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
            "logprob_threshold": -1.0,
            "no_speech_threshold": 0.6,
        }
        
        result = self.pipe(
            audio_path,
            chunk_length_s=30,
            return_timestamps=True,
            generate_kwargs=generate_kwargs
        )
        return result

# 모델 인스턴스 싱글톤 관리 (서버 시작 시 로드)
# 현재 파일 위치를 기준으로 상대 경로 설정
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "resoursces", "models", "whisper-large-v3"))

MODEL_PATH = os.getenv("WHISPER_MODEL_PATH", DEFAULT_MODEL_PATH)
stt_engine = None

def get_stt_engine():
    global stt_engine
    if stt_engine is None:
        stt_engine = WhisperSTT(MODEL_PATH)
    return stt_engine

