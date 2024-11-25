# Scraper

![Supported Python Versions](https://img.shields.io/badge/python-3.8%2B-0D7FBF)
![Ubuntu](https://img.shields.io/badge/linux-compatible-40CA22)
![Windows](https://img.shields.io/badge/windows-compatible-40CA22)


## Overview

Scraper is a feasible web crawling and web scraping that built on top scrapy framework, used to 
efficiently navigates to crawl websites and extract structured data from the selected website. 
It supporting various tasks such as data mining to monitoring and automated testing.


## Capabilities

* **Scraping Dynamic Websites**, scraping items with scraper on dynamic websites that heavily rely on javascript involves using middleware such as selenium to render javascript content before extracting the desired data.
* **Transform Pipelines**, tool that are used to process and manipulate scraped data, such as cleaning, validating, or enriching items, before they are exported or stored.
* **Database Pipelines**, database pipelines on scraper facilitate the storage of scraped data directly into databases like Postgres, MongoDB, or others, by defining custom pipeline classes to handle the insertion of items into the desired database.
* **Multiples Scraping**, soon!
* **Scrapy API Integration**, soon!


## Requirements

* python 3.8+
* pip
* scrapy
* selenium
* python-dotenv
* psycopg[binary]
* fake-useragent

#### Adds-on:

* scrapy-rotating-proxies
* ipython


## Installation

1. From the repository:

		git clone https://github.com/lzarz/scraper.git
		cd scraper
	
2. If you're not using venv,

		python -m venv venv
		. venv/bin/activate (for linux)
		venv\Scripts\activate.bat (for windows)

3. you can skip to install requirements:

		pip install -r requirements.txt


## Getting started

### Quick Running

1. After successfully installing requirements that needed, execute this command to see active spiders that in the scraper:

    	scrapy list

2. Then, choose spider that you want to run. For, examples:

		scrapy crawl toscrape

3. Folder named `data` will be created on *`scraper/data/spider_name`* folder and filled with files formatted like this:

		YYYYmmdd_HMS.csv
		YYYYmmdd_HMS.json
		YYYYmmdd_HMS.xml

> Notes: Y=Year m=Months d=Days H=Hour M=Minutes S=Seconds


### List Active Spiders

| **Spider Name** | **Scraped URL** | **Status** | 
| --- | --- | --- |
| torscrape | `https://books.toscrape.com` | development |
| tokopedia | `https://www.tokopedia.com/p/komputer-laptop/media-penyimpanan-data/ssd` | development |
| shopee | `https://shopee.co.id` | initiated |


### Create New Spider

1. For creating new spider you can execute this command:

		scrapy genspider name_of_your_spider 
	
2.	The spider will be created on *`scraper/scraper/spiders/your_spider_name`*.


###
