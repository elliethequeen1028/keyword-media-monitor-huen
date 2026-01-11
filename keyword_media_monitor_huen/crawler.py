import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext


def match_keywords(text: str, keywords: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Match text against keywords (case-insensitive). Returns matched keywords by priority."""
    text_lower = text.lower()
    matched = {"primary": [], "secondary": []}

    for kw in keywords["primary"]:
        if kw.lower() in text_lower:
            matched["primary"].append(kw)

    for kw in keywords["secondary"]:
        if kw.lower() in text_lower:
            matched["secondary"].append(kw)

    return matched


def save_result(data: dict, storage_path: Path) -> None:
    """Append a matched result to the JSON Lines file."""
    output_file = storage_path / "results.jsonl"
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def create_crawler(keywords: Dict[str, List[str]], storage_path: Path) -> PlaywrightCrawler:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=50,  # Limit for prototype
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f"Processing {context.request.url} ...")

        # Extract page content
        title = await context.page.title()
        text_content = await context.page.evaluate("() => document.body.innerText")

        # Try to find publish date (common patterns)
        publish_date = None
        date_meta = await context.page.query_selector('meta[property="article:published_time"]')
        if date_meta:
            publish_date = await date_meta.get_attribute("content")
        if not publish_date:
            time_elem = await context.page.query_selector("time[datetime]")
            if time_elem:
                publish_date = await time_elem.get_attribute("datetime")

        # Combine title and content for keyword matching
        full_text = f"{title} {text_content}"
        matched = match_keywords(full_text, keywords)

        # Only store if at least one keyword matched
        if matched["primary"] or matched["secondary"]:
            data = {
                "url": context.request.url,
                "title": title,
                "publish_date": publish_date,
                "matched_keywords": matched,
                "content_snippet": text_content[:500] if text_content else "",
                "collected_at": datetime.now().isoformat(),
            }

            await context.push_data(data)
            save_result(data, storage_path)
            context.log.info(f"Matched keywords: {matched}")

        # Follow links on the page
        await context.enqueue_links()

    return crawler
