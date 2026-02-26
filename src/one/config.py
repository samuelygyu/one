from pathlib import Path
import os

# 项目根目录（保持与原来一致：仓库根）
BASE_DIR = Path(__file__).resolve().parents[2]

# 过滤相关配置
MIN_SCORE: float = 0.5
MAX_ITEMS: int = 3

# TTS / 音频相关配置
AUDIO_OUTPUT_DIR: Path = BASE_DIR / "outputs"
DEFAULT_VOICE: str = "zh-CN-XiaoxiaoNeural"

# LLM / DeepSeek 相关配置
DEEPSEEK_API_KEY: str | None = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")


def ensure_directories() -> None:
    """确保运行所需的目录已创建。"""
    AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

