"""
This module contains spider for scraping shopee.com
"""

import scrapy


class ShopeeSpider(scrapy.Spider):
    """Class representing shopee spider."""

    name = "shopee"
    allowed_domains = ["shopee.co.id"]
    start_urls = ["https://shopee.co.id"]

    def parse(self, response, **kwargs):
        pass
