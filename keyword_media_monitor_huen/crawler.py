from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext


def create_crawler() -> PlaywrightCrawler:
    crawler = PlaywrightCrawler()

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url} ...')
        data = {
            'url': context.request.url,
            'title': await context.page.title(),
        }

        await context.push_data(data)
        await context.enqueue_links()

    return crawler
