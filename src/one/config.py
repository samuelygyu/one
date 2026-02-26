from pathlib import Path

# 项目根目录（保持与原来一致：仓库根）
BASE_DIR = Path(__file__).resolve().parents[2]

# 过滤相关配置
MIN_SCORE: float = 0.5
MAX_ITEMS: int = 3

# TTS / 音频相关配置
AUDIO_OUTPUT_DIR: Path = BASE_DIR / "outputs"
DEFAULT_VOICE: str = "zh-CN-XiaoxiaoNeural"


def ensure_directories() -> None:
    """确保运行所需的目录已创建。"""
    AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

