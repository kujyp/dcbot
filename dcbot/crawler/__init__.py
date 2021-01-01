import datetime
from typing import Optional, List

from dcbot.dc import WebDriverContainer


class CrawledContent:

    def __init__(self) -> None:
        self.crawled_time: Optional[datetime.datetime] = None
        self.references: List[str] = []

    def set_crawled_time(self, crawled_time: datetime.datetime):
        self.crawled_time = crawled_time

    def append_reference(self, reference_url: str):
        self.references.append(reference_url)

    def summary_content_prefix(self) -> str:
        return f"기준시간: [{self.crawled_time.strftime('%Y-%m-%d %X')}]\n\n"

    def summary_content_postfix(self) -> str:
        ret = "\n"
        if len(self.references) == 1:
            return ret + f"참조사이트: {self.references[0]}"
        for index, reference in enumerate(self.references):
            ret += f"참조사이트{index + 1}: {reference}\n"
        return ret

    def summary_title_prefix(self) -> str:
        return ""

    def summary_title_postfix(self) -> str:
        return ""

    def summary_title(self) -> str:
        return self.summary_title_prefix() + self.summary_child_title() + self.summary_title_postfix()

    def summary_child_title(self) -> str:
        raise NotImplementedError()

    def summary_content(self) -> str:
        return self.summary_content_prefix() + self.summary_child_content() + self.summary_content_postfix()

    def summary_child_content(self) -> str:
        raise NotImplementedError()


class Crawler:
    def __init__(self, web_driver_container: WebDriverContainer) -> None:
        self.web_driver_container = web_driver_container

    def crawl(self) -> CrawledContent:
        raise NotImplementedError()
