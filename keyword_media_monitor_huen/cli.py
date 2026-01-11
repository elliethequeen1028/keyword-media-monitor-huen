import argparse
import asyncio
from pathlib import Path

from keyword_media_monitor_huen.configuration import parse
from keyword_media_monitor_huen.crawler import create_crawler


async def run_monitor(config_path: Path) -> None:
    """Load configuration and run the crawler."""
    config_text = config_path.read_text()
    config = parse(config_text)

    # Extract target URLs from configuration
    urls = [target["base_url"].text for target in config["targets"]]

    # Extract keywords for matching
    keywords = {
        "primary": [kw.text for kw in config["keywords"]["primary"]],
        "secondary": [kw.text for kw in config["keywords"]["secondary"]],
    }

    # Storage settings
    storage_path = Path(config["storage"]["path"].text)
    storage_path.mkdir(parents=True, exist_ok=True)

    print(f"Starting monitor with {len(urls)} target(s)")
    print(f"Keywords: {keywords}")
    print(f"Storage path: {storage_path}")

    crawler = create_crawler(keywords, storage_path)
    await crawler.run(urls)

    print("Crawl completed!")


def cli(path: str) -> None:
    """Entry point for poe task."""
    asyncio.run(run_monitor(Path(path)))


def main() -> None:
    """CLI entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        prog="keyword-media-monitor",
        description="A lightweight keyword-based web content monitoring tool"
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to the YAML configuration file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse config and show what would be crawled without actually crawling"
    )

    args = parser.parse_args()

    if not args.config.exists():
        parser.error(f"Configuration file not found: {args.config}")

    if args.dry_run:
        config_text = args.config.read_text()
        config = parse(config_text)
        print("Configuration loaded successfully!")
        print(f"Targets: {[t['name'].text for t in config['targets']]}")
        print(f"Primary keywords: {[k.text for k in config['keywords']['primary']]}")
        print(f"Secondary keywords: {[k.text for k in config['keywords']['secondary']]}")
        return

    asyncio.run(run_monitor(args.config))


if __name__ == "__main__":
    main()
