# -*- coding: utf-8 -*-
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class AMBot:

    base_url = "https://www.amazon.de/dp/"

    def __init__(self, timeout_sec=60):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout_sec, 1)
    
    def open_product(self, asin: str) -> None:
        product_url = self.base_url + asin
        logger.info(f"opening product page asin={asin}")
        self.driver.get(product_url)
        assert self.driver.title != "Seite wurde nicht gefunden"
    
    def get_title(self) -> str:
        logger.debug(f"extracting product title")
        title_text = self.driver.find_element_by_xpath(
            "//h1[@id='title']/span[@id='productTitle']"
        ).text
        return title_text

    def get_listing_info(self) -> int:
        logger.debug(f"extracting number of listings")
        listing_text = self.driver.find_element_by_xpath(
            "//div[@id='olp_feature_div']"
        ).text
        listing_cnt = re.\
            search('[^\d]*([\d]*).*', listing_text).group(1)
        return int(listing_cnt)

    def get_ranking_info(self) -> dict:
        ranking_pattern = "Nr\.\s*((\d|\.)*)\s*in\s*(\w*).*"
        ranking_dict = dict()
        logger.debug(f"extracting sales rank information")
        ranking_text = self.driver.find_element_by_xpath(
            "//tr[@id='SalesRank']/td[@class='value']"
        ).text
        lines = ranking_text.split("\n")
        
        for l in lines:
            s = re.search(ranking_pattern, l)
            rank_, category = s.group(1).replace('.',''), s.group(3)
            ranking_dict[category] = int(rank_)
        
        return ranking_dict

    def get_product_info(self, asin: str):
        res = dict()
        
        try:
            self.open_product(asin)
        except AssertionError as e:
            logger.info("item not found")
            return None
        
        res['asin'] = asin
        res['title'] = self.get_title()
        
        try:
            res['listings'] = self.get_listing_info()
        except NoSuchElementException as e:
            logger.info("other listings not found")
            res['listings'] = 0
        
        try:
            rankings = self.get_ranking_info()
            res['category_1'], res['category_2'] = \
                rankings.keys()
            res['rank_1'], res['rank_2'] = \
                rankings.values()
        except NoSuchElementException as e:
            logger.info("ranking info not found")
            pass

        res['updated_at'] = datetime.now()
        
        return res


if __name__ == '__main__':
    # sample_asin = "B07GLMY23V"
    # sample_asin = "B07B4DJ2LJ"
    # sample_asin = "B078X52S84"
    # sample_asin = "B01H1WPOFX" # wrong code
    sample_asin = "B01H1WPOF0"

    ab = AMBot()
    sample_info = ab.get_product_info(sample_asin)
    print(sample_info)