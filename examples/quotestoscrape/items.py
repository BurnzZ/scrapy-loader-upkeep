import scrapy

class QuotesToScrapeItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
