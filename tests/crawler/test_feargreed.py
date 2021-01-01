from dcbot.crawler.feargreed import FearGreedCrawler
from dcbot.dc import WebDriverContainer


def test_feargreed():
    with WebDriverContainer() as web_driver_container:
        crawled = FearGreedCrawler(web_driver_container).crawl()
        assert crawled.summary_title()
        print(crawled.summary_title())
        assert crawled.summary_content()
        print(crawled.summary_content())


def test_extract_from_rawstring():
    assert FearGreedCrawler.extract_from_rawstring("Fear &amp; Greed Now: 51 (Neutral)") == ("Now", 51, "Neutral")
    assert FearGreedCrawler.extract_from_rawstring("Fear &amp; Greed Previous Close: 50 (Neutral)") \
        == ("Previous Close", 50, "Neutral")
    assert FearGreedCrawler.extract_from_rawstring("Fear &amp; Greed 1 Week Ago: 53 (Neutral)") \
        == ("1 Week Ago", 53, "Neutral")
    assert FearGreedCrawler.extract_from_rawstring("Fear &amp; Greed 1 Month Ago: 85 (Extreme Greed)") \
        == ("1 Month Ago", 85, "Extreme Greed")
    assert FearGreedCrawler.extract_from_rawstring("Fear &amp; Greed 1 Year Ago: 93 (Extreme Greed)") \
        == ("1 Year Ago", 93, "Extreme Greed")
