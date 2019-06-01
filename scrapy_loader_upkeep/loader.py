"""Challenges:

- ItemLoaders doesn't have access to the crawler API which contains
  reference to the stats API.

- Could instantiate our own `scrapy.statcollectors.StatsCollector` but there's
  no way of knowning when to dump the stats out since it's not hooked up to the
  'close_spider' signal.
"""

from scrapy.loader import ItemLoader as ItemLoaderOG
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import flatten


class ItemLoader(ItemLoaderOG):

    def get_selector_values(self, selector_rules, selector, **kw):
        self._check_selector_method()

        values = []
        for rule in arg_to_iter(selector_rules):
            data = selector(rule).getall()
            values.append(data)
            self.stat(rule, data)
        return flatten(values)

    def _get_xpathvalues(self, xpaths, **kw):
        """Overridden from parent to add logging to stats."""

        return self.get_selector_values(xpaths, self.selector.xpath, **kw)

    def _get_cssvalues(self, csss, **kw):
        """Overridden from parent to add logging to stats."""

        return self.get_selector_values(csss, self.selector.css, **kw)

    def stat(rule, data):
        pass
