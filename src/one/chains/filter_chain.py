from typing import List, Tuple
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from one.config import MIN_SCORE, MAX_ITEMS
from one.utils.logger import get_logger
from ingestion_engine import ContentItem

logger = get_logger(__name__)
CN_TZ = ZoneInfo("Asia/Shanghai")


def score_item(item: ContentItem) -> float:
    """
    简化的“打分公式”：这里只是根据标题长度做一个玩具分数。
    真实情况会调用 LLM + FILTER_SYSTEM_PROMPT。
    """
    length = len(item.title)
    return max(0.0, min(1.0, length / 30.0))


def filter_today(items: List[ContentItem]) -> List[ContentItem]:
    """
    根据 published_at 过滤出“时间为昨天 00:00:00 ~ 23:59:59”的内容。
    """
    if not items:
        return []

    now_cn = datetime.now(CN_TZ)
    # yesterday_date = now_cn.date() - timedelta(days=1)
    yesterday_date = now_cn #TODO 暂时使用今日
    start_cn = datetime.combine(yesterday_date, time(0, 0, 0), tzinfo=CN_TZ)
    end_cn = datetime.combine(yesterday_date, time(23, 59, 59), tzinfo=CN_TZ)

    kept: List[ContentItem] = []
    for item in items:
        pub = item.published_at
        if pub is None:
            continue

        if start_cn <= pub <= end_cn:
            kept.append(item)

    logger.info(
        "Filter_today kept %d/%d items for date %s (CN time)",
        len(kept),
        len(items),
        yesterday_date.isoformat(),
    )
    return kept


def filter_and_rank(items: List[ContentItem]) -> List[Tuple[ContentItem, float]]:
    items = filter_today(items)
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

