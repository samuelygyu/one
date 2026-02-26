from dataclasses import dataclass
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from one.tools.source_fetcher import NewsItem
from one.utils.logger import get_logger
from one.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_MODEL,
    DEEPSEEK_BASE_URL,
)
from one.prompts.writer_prompt import WRITER_SYSTEM_PROMPT

logger = get_logger(__name__)


@dataclass
class WrittenNews:
    title: str
    hook: str
    script: str
    golden_sentence: str


def _build_llm() -> ChatOpenAI | None:
    """构造 DeepSeek LLM 客户端，如果缺少配置则返回 None。"""
    if not DEEPSEEK_API_KEY:
        logger.warning("DEEPSEEK_API_KEY 未配置，回退到本地 mock 文案。")
        return None

    try:
        return ChatOpenAI(
            model=DEEPSEEK_MODEL,
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("初始化 DeepSeek LLM 失败：%s", exc)
        return None


def _build_chain(llm: ChatOpenAI):
    """基于系统 Prompt 构建 LangChain Chain。"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", WRITER_SYSTEM_PROMPT),
            (
                "user",
                "标题：{title}\n\n摘要：{summary}",
            ),
        ]
    )
    parser = JsonOutputParser()
    return prompt | llm | parser


def _mock_written_news(item: NewsItem) -> WrittenNews:
    """在没有 LLM 时的降级逻辑，保留原来的简单口语化拼接。"""
    hook = f"今天跟你聊一条关于「{item.title}」的新闻。"
    script = (
        f"{hook}\n\n"
        f"简单说，这条新闻的核心是：{item.summary}\n\n"
        "如果放到我们日常生活里，其实可以这么理解："
        "科技公司在不断尝试，用新的产品和技术，把原来很难实现的事情变得更丝滑。"
    )
    golden_sentence = f"{item.title}，背后其实是在抢占下一代科技话语权。"

    logger.info("Generated mock script for '%s' (fallback)", item.title)
    return WrittenNews(
        title=item.title,
        hook=hook,
        script=script,
        golden_sentence=golden_sentence,
    )


def _parse_llm_result(item: NewsItem, result: Dict[str, Any]) -> WrittenNews:
    """把 LLM 返回的 JSON 解析成 WrittenNews，缺字段时做容错。"""
    hook = str(result.get("hook") or "").strip()
    script = str(result.get("script") or "").strip()
    golden_sentence = str(result.get("golden_sentence") or "").strip()

    if not hook or not script or not golden_sentence:
        logger.warning("LLM 返回 JSON 字段缺失，回退到 mock 文案，title=%s", item.title)
        return _mock_written_news(item)

    logger.info("Generated script by DeepSeek LLM for '%s'", item.title)
    return WrittenNews(
        title=item.title,
        hook=hook,
        script=script,
        golden_sentence=golden_sentence,
    )


def write_script(item: NewsItem) -> WrittenNews:
    """
    写稿链路：调用 DeepSeek LLM + WRITER_SYSTEM_PROMPT 生成播客脚本。

    当 LLM 不可用时，会自动回退到本地 mock 逻辑，避免整体流程中断。
    """
    llm = _build_llm()
    if llm is None:
        return _mock_written_news(item)

    chain = _build_chain(llm)

    try:
        result = chain.invoke({"title": item.title, "summary": item.summary})
    except Exception as exc:  # noqa: BLE001
        logger.error("调用 DeepSeek LLM 失败，将回退到 mock 文案：%s", exc)
        return _mock_written_news(item)

    if isinstance(result, dict):
        return _parse_llm_result(item, result)

    logger.warning("LLM 返回结果类型异常（%s），回退到 mock 文案。", type(result))
    return _mock_written_news(item)


def batch_write(items: List[NewsItem]) -> List[WrittenNews]:
    return [write_script(i) for i in items]

