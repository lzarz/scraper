"""
This module contains a Scrapy spider that crawls through the books.toscrape.com
website, extracting information about books listed there. The spider starts from
the main page and follows links to individual book pages to gather detailed data
such as title, price, availability, reviews, etc.
"""

import datetime
import scrapy
from scraper.items import BookItem


class ToscrapeSpider(scrapy.Spider):
    """
    Spider for scraping book data from books.toscrape.com.
    """

    name = "toscrape"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    @classmethod
    def update_settings(cls, settings):
        """
        Update Scrapy Global settings for the toscrape spider.

        Sets the following settings:
            - ITEM_PIPELINES: Configures the pipeline to use 'TransformToscrapeBooksPipeline' with priority 300.
            - FEEDS: Configures output feeds in CSV, JSON, and XML formats with current timestamped filenames.
        """

        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        settings.set("ITEM_PIPELINES", {
            "scraper.pipelines.TransformToscrapeBooksPipeline": 300
        })
        settings.set("FEEDS", {
            "data/%(name)s/" + current_time + ".csv": {
                "format": "csv",
                "encoding": "utf-8-sig",
                "fields": [
                    "url", "title", "product_type", "price_excl_tax", "price_incl_tax",
                    "tax", "price", "availability", "num_reviews", "stars", "category",
                    "description"
                ],
            },
            "data/%(name)s/" + current_time + ".json": {
                "format": "json",
                "encoding": "utf-8",
            },
            "data/%(name)s/" + current_time + ".xml": {
                "format": "xml"
            }
        })

    def parse(self, response, **kwargs):
        """
        Parse the main page listing books and follow links to individual book pages.
        """

        books = response.css("article.product_pod")
        for book in books:
            relative_url = book.css("h3 a::attr(href)").get()
            if "catalogue/" not in relative_url:
                relative_url = "catalogue/" + relative_url.lstrip('/')
            yield response.follow(relative_url, callback=self.parse_book_page)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book_page(self, response):
        """
        Parse individual book page and extract relevant information.
        """

        book_item = BookItem()

        book_item["url"] = response.url
        book_item["title"] = response.css(".product_main h1::text").get()
        book_item["product_type"] = response.css("th:contains('Product Type') + td::text").get()
        book_item["price_excl_tax"] = response.css("th:contains('Price (excl. tax)') + td::text").get()
        book_item["price_incl_tax"] = response.css("th:contains('Price (incl. tax)') + td::text").get()
        book_item["tax"] = response.css("th:contains('Tax') + td::text").get()
        book_item["availability"] = response.css("th:contains('Availability') + td::text").get()
        book_item["num_reviews"] = response.css("th:contains('Number of reviews') + td::text").get()
        book_item["stars"] = response.css("p.star-rating::attr(class)").get()
        book_item["category"] = response.css("ul.breadcrumb li:nth-last-child(2) a::text").get()
        book_item["description"] = response.css("#product_description ~ p::text").get()
        book_item["price"] = response.css("p.price_color::text").get()

        yield book_item
