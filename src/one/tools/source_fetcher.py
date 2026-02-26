from dataclasses import dataclass
from typing import List

from one.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class NewsItem:
    title: str
    summary: str
    link: str


def fetch_latest_news(limit: int = 5) -> List[NewsItem]:
    """
    一个假的 RSS 抓取器：真实项目中这里会请求 RSS 源。
    现在先返回几条模拟数据，方便打通流程。
    """
    logger.info("Fetching latest news from mock RSS feed...")

    items = [
        NewsItem(
            title="OpenAI 发布全新语音模型",
            summary="新模型在实时语音对话和情感表达上有显著提升。",
            link="https://example.com/openai-voice",
        ),
        NewsItem(
            title="特斯拉推出下一代自动驾驶系统",
            summary="FSD 新版本在城市道路表现更稳定，计划逐步推送。",
            link="https://example.com/tesla-fsd",
        ),
        NewsItem(
            title="苹果考虑在 iPhone 中集成本地 AI 芯片",
            summary="消息称新芯片将大幅提升端侧推理能力，保护隐私。",
            link="https://example.com/apple-ai-chip",
        ),
    ]

    return items[:limit]

