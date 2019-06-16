from scrapy_loader_upkeep import ItemLoader

from quotestoscrape.items import QuotesToScrapeItem


class QuotesItemLoader(ItemLoader):
    default_item_class = QuotesToScrapeItem
