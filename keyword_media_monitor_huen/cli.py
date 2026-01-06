import asyncio

from keyword_media_monitor_huen.crawler import create_crawler


async def cli(path) -> None:
    crawler = create_crawler()
    await crawler.run(['https://crawlee.dev'])

async def main() -> None:
    pass


if __name__ == "__main__":
    asyncio.run(main())
