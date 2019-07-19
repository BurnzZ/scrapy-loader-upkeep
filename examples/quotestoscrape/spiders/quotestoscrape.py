import scrapy

from ..loader import QuotesItemLoader


class BaseExampleSpider(scrapy.Spider):

    start_urls = ["http://quotes.toscrape.com/"]


class QuotesToScrapeSimpleSpider(BaseExampleSpider):
    """This is a simple example that should output this in the stats:

        2019-06-16 14:32:32 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
        { ...
          'parser/QuotesItemLoader/author/css/1': 10,
          'parser/QuotesItemLoader/quote/css/1': 10,
          ...
        }

    This presents an example where the 100% of the declared parser rules have
    been successfully matched.
    """

    name = "quotestoscrape_simple"

    def parse(self, response):
        """Notice that in order for this enhanced ItemLoader package to work,
        we'll need to inject the stats API into it.
        """

        for quote_div in response.css("div.quote"):
            loader = QuotesItemLoader(selector=quote_div, stats=self.crawler.stats)
            loader.add_css("quote", '.quote > span[itemprop="text"]::text')
            loader.add_css("author", ".author::text")
            yield loader.load_item()


class QuotesToScrapeHasMissingSpider(BaseExampleSpider):
    """Similar to the example above but some fallback parsers are added with
    purposefully "not-working" rules to demonstrate obsolete rules.

        2019-06-16 14:32:32 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
        { ...
          'parser/QuotesItemLoader/author/css/1': 10,
          'parser/QuotesItemLoader/quote/css/1/missing': 10,
          'parser/QuotesItemLoader/quote/css/2': 10
          ...
        }
    """

    name = "quotestoscrape_has_missing"

    def parse(self, response):
        """Notice that in order for this enhanced ItemLoader package to work,
        we'll need to inject the stats API into it.
        """

        for quote_div in response.css("div.quote"):
            loader = QuotesItemLoader(selector=quote_div, stats=self.crawler.stats)
            loader.add_css(
                "quote",
                [
                    # This first parser rule doesn't exist at all.
                    ".this-quote-does-not-exist span::text",
                    '.quote > span[itemprop="text"]::text',
                ],
            )
            loader.add_css("author", ".author::text")
            yield loader.load_item()


class QuotesToScrapeUseName(BaseExampleSpider):
    """Demonstrates the new feature of naming the parsers using the 'name' param.

        2019-06-16 14:32:32 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
        { ...
          'parser/QuotesItemLoader/author/css/1/basic author class': 10,
          'parser/QuotesItemLoader/quote/css/1/Quotes inside the box/missing': 10,
          'parser/QuotesItemLoader/quote/css/2/Quotes inside the box': 10,
          'parser/QuotesItemLoader/tags/css/1/underneath the author text': 10,
          ...
        }
    """

    name = "quotestoscrape_use_name"

    def parse(self, response):
        """Notice that in order for this enhanced ItemLoader package to work,
        we'll need to inject the stats API into it.
        """

        for quote_div in response.css("div.quote"):
            loader = QuotesItemLoader(selector=quote_div, stats=self.crawler.stats)
            loader.add_css(
                "quote",
                [
                    # This first parser rule doesn't exist at all.
                    ".this-quote-does-not-exist span::text",
                    '.quote > span[itemprop="text"]::text',
                ],
                name="Quotes inside the box",
            )
            loader.add_css("author", ".author::text", name="basic author class")
            loader.add_css("tags", ".tag::text", name="underneath the author text")
            yield loader.load_item()
