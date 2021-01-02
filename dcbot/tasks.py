from dcbot.crawler.feargreed import FearGreedCrawler
from dcbot.dc import WebDriverContainer, post_with


def fear_greed(dc_nickname: str, dc_article_password: str, gall_id: str, headless: bool):
    with WebDriverContainer(headless) as web_driver_container:
        crawled = FearGreedCrawler(web_driver_container).crawl()
        title = crawled.summary_title()
        content = crawled.summary_content()
        post_with(web_driver_container, dc_nickname, dc_article_password, gall_id, title, content)
