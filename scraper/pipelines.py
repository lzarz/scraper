"""
Module for defining item pipelines for web scraping with Scrapy.

Pipelines:
- TransformToscrapeBooksPipeline: Handles data transformation for 'toscrape' spider items.
- LoadPostgresPipeline: Manages loading for general scraped items into PostgreSQL database tables.
"""

import psycopg
from scrapy.exceptions import NotConfigured
from itemadapter import ItemAdapter

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


class TransformToscrapeBooksPipeline:
    """
    Pipeline for transforming toscrape books scraped items.
    """

    def process_item(self, item, spider):
        """
        Perform various formatting operations on the scraped item.
        """

        adapter = ItemAdapter(item)

        # Strip whitespace from all string fields except 'description'
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                if isinstance(value, str):
                    adapter[field_name] = value.strip()

        # Transform specific fields to lowercase
        for field in ["category", "product_type"]:
            value = adapter.get(field)
            if isinstance(value, str):
                adapter[field] = value.lower()

        # Transform price fields to float
        for price_field in ["price", "price_excl_tax", "price_incl_tax", "tax"]:
            value = adapter.get(price_field)
            if value:
                adapter[price_field] = float(value.replace("£", ""))

        # Extract number from availability string
        availability = adapter.get("availability", "")
        if "(" in availability:
            availability = availability.split("(")[1].split(" ")[0]
            adapter["availability"] = int(availability)
        else:
            adapter["availability"] = 0

        # Transform num_reviews to integer
        num_reviews = adapter.get("num_reviews", "0")
        adapter["num_reviews"] = int(num_reviews)

        # Transform stars text to integer
        stars_string = adapter.get("stars")
        split_stars_array = stars_string.split(" ")
        stars_text_value = split_stars_array[1].strip().lower()
        stars_mapping = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5
        }
        adapter["stars"] = stars_mapping.get(stars_text_value, 0)

        return item


class LoadPostgresPipeline:
    """
    Pipeline for load scraped items into a PostgreSQL database.
    """

    def __init__(self, host, port, user, password, database):
        # Connection Details
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        host = settings.get('DATABASE_HOST')
        port = settings.get('DATABASE_PORT')
        user = settings.get('DATABASE_USER')
        password = settings.get('DATABASE_PASSWORD')
        database = settings.get('DATABASE_NAME')

        if not all([host, port, user, password, database]):
            raise NotConfigured("Database settings are not properly configured")

        return cls(host, port, user, password, database)

    def open_spider(self, spider):
        """
        Initialize database connection and cursor when the spider opens.
        """

        # Connect to database
        self.connection = psycopg.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.database
        )

        # Connect cursor, used to execute commands
        self.cursor = self.connection.cursor()

        if spider.name == "toscrape":
            self._create_books_table()
        elif spider.name == "tokopedia":
            self._create_products_table()

    def _create_books_table(self):
        """
        Create the books table if it doesn't exist.
        """

        create_table_query = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255),
            title TEXT,
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description TEXT
        );
        """
        self._execute_query(create_table_query)

    def _create_products_table(self):
        """
        Create the products table if it doesn't exist.
        """

        create_table_query = """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(100),
            product_price VARCHAR(25),
            total_review INTEGER
        );
        """
        self._execute_query(create_table_query)

    def _execute_query(self, query, data=None):
        """
        Helper method to execute a database query.
        """

        try:
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
        except psycopg.Error as e:
            print(f"Database error: {e}")

    def process_item(self, item, spider):
        """
        Insert items into the database.
        """

        if spider.name == "toscrape":
            self._insert_book(item)
        elif spider.name == "tokopedia":
            self._insert_product(item)

        self.connection.commit()
        return item

    def _insert_book(self, item):
        """
        Insert book items into the books table.
        """

        insert_query = """
        INSERT INTO books (
            url, title, product_type, price_excl_tax, price_incl_tax, tax, price,
            availability, num_reviews, stars, category, description
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        data = (
            item["url"], item["title"], item["product_type"], item["price_excl_tax"],
            item["price_incl_tax"], item["tax"], item["price"], item["availability"],
            item["num_reviews"], item["stars"], item["category"], item["description"]
        )
        self._execute_query(insert_query, data)

    def _insert_product(self, item):
        """
        Insert a product item into the products table.
        """

        insert_query = """
        INSERT INTO products (
            product_name, product_price, total_review
        ) VALUES (%s, %s, %s);
        """
        data = (item["product_name"], item["product_price"], item["total_review"])
        self._execute_query(insert_query, data)

    def close_spider(self, spider):
        """
        Close database connection and cursor when the spider closes.
        """

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
