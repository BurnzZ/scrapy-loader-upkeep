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

    # The methods below have been overridden from their parent to pass the
    # 'field_name' variable into `_get_xpathvalues()` and `_get_cssvalues()`

    def add_xpath(self, field_name, xpath, *processors, **kw):
        values = self._get_xpathvalues(field_name, xpath, **kw)
        self.add_value(field_name, values, *processors, **kw)

    def replace_xpath(self, field_name, xpath, *processors, **kw):
        values = self._get_xpathvalues(field_name, xpath, **kw)
        self.replace_value(field_name, values, *processors, **kw)

    def get_xpath(self, xpath, *processors, **kw):
        values = self._get_xpathvalues(field_name, xpath, **kw)
        return self.get_value(values, *processors, **kw)

    def add_css(self, field_name, css, *processors, **kw):
        values = self._get_cssvalues(field_name, css, **kw)
        self.add_value(field_name, values, *processors, **kw)

    def replace_css(self, field_name, css, *processors, **kw):
        values = self._get_cssvalues(field_name, css, **kw)
        self.replace_value(field_name, values, *processors, **kw)

    def get_css(self, css, *processors, **kw):
        values = self._get_cssvalues(field_name, css, **kw)
        return self.get_value(values, *processors, **kw)

    # The methods below are overridden and have been refactored for integration
    # for logging and stats.

    def _get_xpathvalues(self, field_name, xpaths, **kw):
        return self.get_selector_values(
            field_name, xpaths, self.selector.xpath, **kw)

    def _get_cssvalues(self, field_name, csss, **kw):
        return self.get_selector_values(
            field_name, csss, self.selector.css, **kw)

    def get_selector_values(self, field_name, selector_rules, selector, **kw):
        """Provides an abstraction to _get_xpathvalues() and _get_cssvalues()
        since they share the same components.
        """

        self._check_selector_method()

        values = []
        for rule in arg_to_iter(selector_rules):
            data = selector(rule).getall()
            values.append(data)
            self.stat(field_name, rule, data)
        return flatten(values)

    def stat(field_name, rule, data):
        pass
