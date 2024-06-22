"""
Module for defining models for scraped items. This module contains
the item definitions for the web scraping project using Scrapy.
Each item represents a specific type of data entity that can be scraped.
"""

import scrapy


class BookItem(scrapy.Item):
    """
    Class representing a book item.

    Attributes:
        url (scrapy.Field): The URL of the book's webpage.
        title (scrapy.Field): The title of the book.
        product_type (scrapy.Field): The type of product (e.g., book).
        price_excl_tax (scrapy.Field): The price excluding tax.
        price_incl_tax (scrapy.Field): The price including tax.
        tax (scrapy.Field): The tax amount.
        availability (scrapy.Field): The availability status of the book.
        num_reviews (scrapy.Field): The number of reviews.
        stars (scrapy.Field): The star rating of the book.
        category (scrapy.Field): The category of the book.
        description (scrapy.Field): A description of the book.
        price (scrapy.Field): The price of the book.
    """

    url = scrapy.Field()
    title = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()


class ProductItem(scrapy.Item):
    """
    Class representing a product item.

    Attributes:
        product_name (scrapy.Field): The name of the product.
        product_price (scrapy.Field): The price of the product.
        total_review (scrapy.Field): The total number of reviews for the product.
    """

    product_name = scrapy.Field()
    product_price = scrapy.Field()
    total_review = scrapy.Field()
