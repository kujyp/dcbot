import datetime
from typing import Tuple, Optional, Dict, Any

from dcbot.crawler import Crawler, CrawledContent


class FearGreedCrawledContent(CrawledContent):
    TIME_NOW = "Now"
    TIME_PREV_CLOSE = "Previous Close"
    TIME_WEEK_AGO = "1 Week Ago"
    TIME_MONTH_AGO = "1 Month Ago"
    TIME_YEAR_AGO = "1 Year Ago"
    TIMES = [TIME_NOW, TIME_PREV_CLOSE, TIME_WEEK_AGO, TIME_MONTH_AGO, TIME_YEAR_AGO]

    def __init__(self) -> None:
        super().__init__()
        self.content: Dict[str, Dict[str, Any]] = {}

    def append_value(self, time_value: str, feargreed_value: int, feargreed_readable_value: str):
        assert time_value in self.TIMES
        assert time_value not in self.content
        self.content[time_value] = {
            "value": feargreed_value,
            "readable": feargreed_readable_value,
        }

    def summary_child_title(self) -> str:
        assert self.TIME_NOW in self.content
        return f"현재 공포지수 {self.content[self.TIME_NOW]['value']} / {self.content[self.TIME_NOW]['readable']}"

    def summary_child_content(self) -> str:
        ret = ""
        for each_time in self.TIMES:
            if each_time not in self.content:
                continue
            ret += f"Fear & Greed {each_time}: {self.content[each_time]['value']} ({self.content[each_time]['readable']})\n"
        return ret


class FearGreedCrawler(Crawler):
    def crawl(self) -> FearGreedCrawledContent:
        ret = FearGreedCrawledContent()

        url = "https://money.cnn.com/data/fear-and-greed/"
        self.web_driver_container.get(url)
        ret.append_reference(url)
        ret.set_crawled_time(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=9))))

        needle_div = self.web_driver_container.find_element_by_id("needleChart")
        for each in needle_div.find_elements_by_xpath("ul/li"):
            time_value, feargreed_value, feargreed_readable_value = self.extract_from_rawstring(each.get_attribute("innerHTML"))
            ret.append_value(time_value, feargreed_value, feargreed_readable_value)
        return ret

    @staticmethod
    def extract_from_rawstring(raw_string: str) -> Tuple[str, int, str]:
        processed = raw_string
        assert processed.startswith("Fear &amp; Greed ")
        processed = processed[len("Fear &amp; Greed "):]
        splited = processed.split(":")
        time_value = splited[0]
        splited2 = splited[1].split("(")
        feargreed_value = int(splited2[0].strip())
        feargreed_readable_value = splited2[1].strip(")")
        return time_value, feargreed_value, feargreed_readable_value
