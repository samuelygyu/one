from dataclasses import dataclass
from typing import List

from one.tools.source_fetcher import NewsItem
from one.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class WrittenNews:
    title: str
    hook: str
    script: str
    golden_sentence: str


def write_script(item: NewsItem) -> WrittenNews:
    """
    简化版“写稿链路”：只根据标题和摘要拼接一段口语化文案。
    真实情况会调用 LLM + WRITER_SYSTEM_PROMPT。
    """
    hook = f"今天跟你聊一条关于「{item.title}」的新闻。"
    script = (
        f"{hook}\n\n"
        f"简单说，这条新闻的核心是：{item.summary}\n\n"
        "如果放到我们日常生活里，其实可以这么理解："
        "科技公司在不断尝试，用新的产品和技术，把原来很难实现的事情变得更丝滑。"
    )
    golden_sentence = f"{item.title}，背后其实是在抢占下一代科技话语权。"

    logger.info("Generated mock script for '%s'", item.title)
    return WrittenNews(
        title=item.title,
        hook=hook,
        script=script,
        golden_sentence=golden_sentence,
    )


def batch_write(items: List[NewsItem]) -> List[WrittenNews]:
    return [write_script(i) for i in items]

