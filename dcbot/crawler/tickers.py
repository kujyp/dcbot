from typing import Tuple, List

import requests
from dataclasses import dataclass


@dataclass
class Ticker:
    def __init__(self, symbol: str, security_name: str, is_etf: bool) -> None:
        super().__init__()
        self.symbol = symbol
        self.security_name = security_name
        self.is_etf = is_etf


class TickerCrawler:
    @staticmethod
    def crawl():
        ret: List[Ticker] = []
        ret.extend(TickerCrawler.get_nasdaqlisted())
        ret.extend(TickerCrawler.get_otherlisted())
        return ret

    @staticmethod
    def get_nasdaqlisted():
        ret: List[Ticker] = []

        url = "http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
        r = requests.get(url)
        for idx, eachline in enumerate(r.text.splitlines()):
            if eachline.startswith("File Creation Time"):
                continue

            splited = eachline.split("|")
            if idx == 0:
                assert_msg = "Updated. Need to rewrite codes."
                assert splited[0] == "Symbol", assert_msg
                assert splited[1] == "Security Name", assert_msg
                assert splited[2] == "Market Category", assert_msg
                assert splited[3] == "Test Issue", assert_msg
                assert splited[4] == "Financial Status", assert_msg
                assert splited[5] == "Round Lot Size", assert_msg
                assert splited[6] == "ETF", assert_msg
                continue

            splited = eachline.split("|")
            symbol = splited[0].strip()
            security_name = splited[1].strip()
            _market_category = splited[2].strip()
            _test_issue = splited[3]
            _financial_status = splited[4]
            _round_lot_size = splited[5]
            is_etf = splited[6].strip() == "Y"
            ret.append(Ticker(symbol, security_name, is_etf))
        return ret

    @staticmethod
    def get_otherlisted():
        ret: List[Ticker] = []

        url = "http://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
        r = requests.get(url)
        for idx, eachline in enumerate(r.text.splitlines()):
            if eachline.startswith("File Creation Time"):
                continue

            splited = eachline.split("|")
            if idx == 0:
                assert_msg = "Updated. Need to rewrite codes."
                assert splited[0] == "ACT Symbol", assert_msg
                assert splited[1] == "Security Name", assert_msg
                assert splited[2] == "Exchange", assert_msg
                assert splited[3] == "CQS Symbol", assert_msg
                assert splited[4] == "ETF", assert_msg
                assert splited[5] == "Round Lot Size", assert_msg
                assert splited[6] == "Test Issue", assert_msg
                assert splited[7] == "NASDAQ Symbol", assert_msg
                continue

            splited = eachline.split("|")
            act_symbol = splited[0].strip()
            security_name = splited[1].strip()
            _cqs_symbol = splited[3].strip()
            is_etf = splited[4].strip() == "Y"
            _round_lot_size = splited[5]
            _test_issue = splited[6]
            _nasdaq_symbol = splited[7]
            ret.append(Ticker(act_symbol, security_name, is_etf))
        return ret
