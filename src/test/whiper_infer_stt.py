import torch
import logging
import json
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os

# 로거 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 설정
    model_path = "/home/pps-nipa/NIQ/fish/whisper/src/resoursces/models/whisper-large-v3"
    audio_path = "/home/pps-nipa/NIQ/fish/whisper/src/test/4번자리_나연.wav"
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    logger.info(f"Using device: {device}")
    logger.info(f"Loading model from: {model_path}")

    try:
        # 모델 및 프로세서 로드
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_path, 
            torch_dtype=torch_dtype, 
            low_cpu_mem_usage=True, 
            use_safetensors=True
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained(model_path)

        # 파이프라인 설정
        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
        )

        logger.info(f"Transcribing audio: {audio_path}")

        # STT 실행 옵션 설정 (Hugging Face 권장 사항 반영)
        # '아 아 아...'와 같은 반복 현상을 방지하기 위해 디코딩 파라미터를 강화합니다.
        generate_kwargs = {
            "language": "korean",
            "max_new_tokens": 448,
            "num_beams": 1,
            "condition_on_prev_tokens": False,
            "compression_ratio_threshold": 1.35,
            "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
            "logprob_threshold": -1.0,
            "no_speech_threshold": 0.6,
        }

        # STT 실행
        # 30초 이상의 긴 음성을 처리하기 위해 return_timestamps=True와 chunk_length_s=30을 유지합니다.
        result = pipe(
            audio_path, 
            chunk_length_s=30, 
            return_timestamps=True,
            generate_kwargs=generate_kwargs
        )

        # 결과 출력
        print("\n" + "="*50)
        print("STT 결과:")
        print(result["text"])
        print("="*50 + "\n")
        
        # JSON 파일로 저장
        output_json_path = audio_path.rsplit(".", 1)[0] + ".json"
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        logger.info(f"STT 결과(타임스탬프 포함)가 저장되었습니다: {output_json_path}")
        logger.info("Transcription completed successfully.")

    except Exception as e:
        logger.exception(f"An error occurred during STT process: {e}")

if __name__ == "__main__":
    main()

