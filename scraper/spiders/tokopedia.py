"""
This module contains a Scrapy spider for scraping SSD product data from Tokopedia.
The spider is designed to navigate through the SSD product listings on Tokopedia's
website, extract relevant product details, and yield them as `ProductItem` instances.
"""

import scrapy
from scraper.items import ProductItem


class TokopediaSpider(scrapy.Spider):
    """
    Spider for scraping SSD products from tokopedia.com
    """

    name = "tokopedia"
    allowed_domains = ["tokopedia.com"]
    start_urls = [
        "https://www.tokopedia.com/p/komputer-laptop/media-penyimpanan-data/ssd"
    ]

    @classmethod
    def update_settings(cls, settings):
        """
        Update Scrapy Global settings for the tokopedia spider.

        Sets the following settings:
            - DOWNLOAD_DELAY: Sets a delay of 1 second between consecutive requests.
            - ITEM_PIPELINES: Configures the pipeline to use 'LoadPostgresPipeline' with priority 301.
        """

        settings.set("DOWNLOAD_DELAY", 1)
        settings.set("ITEM_PIPELINES", {
            "scraper.pipelines.LoadPostgresPipeline": 301
        })

    def __init__(self, **kwargs):
        """
        Initialize the spider with configurable parameters.
        """

        super().__init__(**kwargs)
        self.item_count = 0
        self.page = 1
        self.max_items = 60
        self.max_pages = 1
        self.base_url = self.start_urls[0] + "?ob=5&page={}"
        self.request_url = self.base_url.format(self.page)

    def start_requests(self):
        """
        Generate initial requests to the start URLs.
        """

        yield scrapy.Request(url=self.request_url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        Parse the response and extract product data.
        """

        if self.page > self.max_pages or self.item_count >= self.max_items:
            return

        products = response.css(".css-bk6tzz.e1nlzfl2")
        for product in products:
            if product.css(".css-1f8sh1y").get() is not None:
                continue

            product_item = ProductItem()
            product_item["product_name"] = product.css(".css-20kt3o::text").get()
            product_item["product_price"] = product.css(".css-o5uqvq::text").get()
            total_review = product.css(".css-1riykrk div span::text").re_first(r"\d+")
            product_item["total_review"] = total_review

            self.item_count += 1
            yield product_item

        if self.item_count < self.max_items:
            self.page += 1
            next_page_url = self.base_url.format(self.page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
