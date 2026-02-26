from pathlib import Path
from typing import Iterable, List

from one.config import AUDIO_OUTPUT_DIR
from one.utils.logger import get_logger

logger = get_logger(__name__)


def synthesize_to_file(text: str, filename: str) -> Path:
    """
    简化版 TTS：真实情况会调用 Edge-TTS / 其他 TTS 服务。
    当前实现只把文本写入 .txt 作为“占位音频文件”，方便打通流程。
    """
    AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = AUDIO_OUTPUT_DIR / filename
    output_path.write_text(text, encoding="utf-8")
    logger.info("Mock synthesized audio to %s", output_path)
    return output_path


def batch_synthesize(scripts: Iterable[str]) -> List[Path]:
    paths: List[Path] = []
    for idx, script in enumerate(scripts, start=1):
        path = synthesize_to_file(script, f"news_{idx}.txt")
        paths.append(path)
    return paths

