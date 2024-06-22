"""
Module for defining models for middlewares.This module contains classes that define
spider middleware and downloader middlewares for Scrapy spiders. These middlewares
extend the functionality of Scrapy by providing custom handling of requests and responses
during the scraping process.
"""

import time
import logging
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from fake_useragent import UserAgent

# useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter


class ScraperSpiderMiddleware:
    """
    Middleware for handling spider actions.
    """
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        """
        Initialize the middleware and connect signals.
        """

        instance = cls()
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    def process_spider_input(self, response, spider):
        """
        Process each response before it reaches the spider.
        """
        # Should return None or raise an exception.

        return None

    def process_spider_output(self, response, result, spider):
        """
        Process the results returned from the spider.
        """
        # Must return an iterable of Request, or item objects.

        for item in result:
            yield item

    def process_spider_exception(self, response, exception, spider):
        """
        Handle exceptions raised by the spider or process_spider_input.
        """
        # (from other spider middleware) raises an exception.
        # Should return either None or an iterable of Request or item objects.

    def process_start_requests(self, start_requests, spider):
        """
        Function called with the start requests of the spider, and
        works similarly to the process_spider_output() method, except
        that it doesn’t have a response associated.
        """
        # Must return only requests (not items).

        for request in start_requests:
            yield request

    def spider_opened(self, spider):
        """
        Log when the spider is opened.
        """

        spider.logger.info("Spider opened: " + spider.name)

    def spider_closed(self, spider):
        """
        Log when the spider is closed.
        """

        spider.logger.info(f"Spider closed: {spider.name}")


class ScraperDownloaderMiddleware:
    """
    Middleware for handling downloader actions.
    """
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    logging.getLogger("selenium.webdriver").setLevel(logging.INFO)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

    def __init__(self, crawler):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--user-agent=" + crawler.settings.get('USER_AGENT'))
        self.driver = webdriver.Chrome(options=options)

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware and connect signals."""
        instance = cls(crawler)
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(instance.spider_closed, signal=signals.spider_closed)
        return instance

    def process_request(self, request, spider):
        """
        Process each request through the downloader.
        """
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        self.driver.get(request.url)
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        body = self.driver.page_source
        return HtmlResponse(
            url=self.driver.current_url, body=body, encoding="utf-8", request=request
        )

    def process_response(self, request, response, spider):
        """
        Process the response returned from the downloader.
        """
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        return response

    def process_exception(self, request, exception, spider):
        """
        Handle exceptions raised during request processing.
        """
        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain

        pass

    def spider_opened(self, spider):
        """
        Log when the spider is opened.
        """

        spider.logger.info(f"Spider opened: {spider.name}")

    def spider_closed(self, spider):
        """
        Quit the webdriver when the spider is closed.
        """

        self.driver.quit()
        spider.logger.info(f"Spider closed: {spider.name}")


class FakeUserAgentMiddleware:
    """
    Middleware for setting a random User-Agent for each request.
    """

    def process_request(self, request):
        """
        Set a random User-Agent for each request.
        """

        user_agent = UserAgent().random
        request.headers["User-Agent"] = user_agent
