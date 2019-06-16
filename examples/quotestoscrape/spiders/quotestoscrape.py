import scrapy

from ..loader import QuotesItemLoader


class QuotesToScrapeSimpleSpider(scrapy.Spider):
    """This is a simple example that should output this in the stats:

        2019-06-16 14:32:32 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
        {...
         'parser/QuotesItemLoader/author/0': 10,
         'parser/QuotesItemLoader/quote/0': 10,
         ...
        }

    This presents an example where the 100% of the declared parser rules have
    been successfully matched.
    """

    name = 'quotestoscrape_simple'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        """Notice that in order for this enhanced ItemLoader package to work,
        we'll need to inject the stats API into it.
        """

        for quote_div in response.css('div.quote'):
            loader = QuotesItemLoader(selector=quote_div, stats=self.crawler.stats)
            loader.add_css('quote', '.quote > span[itemprop="text"]::text')
            loader.add_css('author', '.author::text')
            yield loader.load_item()
