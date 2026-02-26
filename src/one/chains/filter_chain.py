from typing import List, Tuple

from one.config import MIN_SCORE, MAX_ITEMS
from one.utils.logger import get_logger
from ingestion_engine import ContentItem

logger = get_logger(__name__)


def score_item(item: ContentItem) -> float:
    """
    简化的“打分公式”：这里只是根据标题长度做一个玩具分数。
    真实情况会调用 LLM + FILTER_SYSTEM_PROMPT。
    """
    length = len(item.title)
    return max(0.0, min(1.0, length / 30.0))


def filter_and_rank(items: List[ContentItem]) -> List[Tuple[ContentItem, float]]:
    """对新闻列表打分并过滤出合格项。"""
    scored: List[Tuple[ContentItem, float]] = []
    for item in items:
        s = score_item(item)
        logger.info("Scored news '%s' -> %.3f", item.title, s)
        if s >= MIN_SCORE:
            scored.append((item, s))

    # 按分数从高到低排序，并截断数量
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:MAX_ITEMS]

