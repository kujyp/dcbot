from dcbot.crawler.tickers import TickerCrawler, Ticker


def test_ticker():
    crawled = TickerCrawler.crawl()
    assert len(crawled) > 0
    assert Ticker("AAPL", "Apple Inc. - Common Stock", False) in crawled
    assert Ticker("QQQ", "Invesco QQQ Trust, Series 1", True) in crawled
    assert Ticker("NRGU", "MicroSectors U.S. Big Oil Index 3X Leveraged ETN", False) in crawled
