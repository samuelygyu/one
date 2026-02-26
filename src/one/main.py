import asyncio

from one.config import ensure_directories
from one.chains.filter_chain import filter_and_rank
from one.chains.writer_chain import batch_write
from one.tools.audio_engine import batch_synthesize
from one.utils.logger import get_logger
from ingestion_engine import run_ingestion


def main() -> None:
    logger = get_logger(__name__)
    logger.info("News audio automation started.")

    ensure_directories()

    # 1. 抓取新闻（通过 ingestion_engine）
    ingestion_results = asyncio.run(run_ingestion())
    raw_items = [item for r in ingestion_results for item in r.items]
    if not raw_items:
        logger.warning("No news items fetched, exit.")
        return

    # 2. 过滤 + 打分
    scored_items = filter_and_rank(raw_items)
    if not scored_items:
        logger.warning("No items passed filter, exit.")
        return

    kept_items = [item for item, score in scored_items]

    # 3. 生成口语化脚本
    written = batch_write(kept_items)

    # 4. 对各个口播脚本进行编排

    # 5. 生成“音频”（当前为 txt 占位文件）
    audio_paths = batch_synthesize(w.script for w in written)

    for w, p in zip(written, audio_paths):
        logger.info("Generated script for '%s' at %s", w.title, p)

    logger.info("Pipeline finished. Total clips: %d", len(audio_paths))


if __name__ == "__main__":
    main()

