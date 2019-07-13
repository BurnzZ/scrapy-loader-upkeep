from collections import defaultdict
from scrapy.loader import ItemLoader as ItemLoaderOG
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import flatten


class ItemLoader(ItemLoaderOG):
    def __init__(
        self,
        item=None,
        selector=None,
        response=None,
        parent=None,
        stats=None,
        **context,
    ):
        """Adds an additional `stats` dependency to keep track of the fallback
        parser usage.
        """

        super(ItemLoader, self).__init__(
            item=item, selector=selector, response=response, parent=parent, **context
        )

        # This is the new injected dependency that we'll be using as the main
        # functionality of this tool.
        self.stats = stats

        # This keeps track of the position of the 'field' name that is being
        # loaded for a more accurate logging in the stats.
        self.field_tracker = defaultdict(int)

    # The methods below have been overridden from their parent to pass the
    # 'field_name' variable into `_get_xpathvalues()` and `_get_cssvalues()`

    def add_xpath(self, field_name, xpath, *processors, **kw):
        self.field_tracker[f'{field_name}_xpath'] += 1
        values = self._get_xpathvalues(field_name, xpath, **kw)
        self.add_value(field_name, values, *processors, **kw)

    def replace_xpath(self, field_name, xpath, *processors, **kw):
        values = self._get_xpathvalues(field_name, xpath, **kw)
        self.replace_value(field_name, values, *processors, **kw)

    def get_xpath(self, xpath, *processors, **kw):
        values = self._get_xpathvalues(None, xpath, **kw)
        return self.get_value(values, *processors, **kw)

    def add_css(self, field_name, css, *processors, **kw):
        self.field_tracker[f'{field_name}_css'] += 1
        values = self._get_cssvalues(field_name, css, **kw)
        self.add_value(field_name, values, *processors, **kw)

    def replace_css(self, field_name, css, *processors, **kw):
        values = self._get_cssvalues(field_name, css, **kw)
        self.replace_value(field_name, values, *processors, **kw)

    def get_css(self, css, *processors, **kw):
        values = self._get_cssvalues(None, css, **kw)
        return self.get_value(values, *processors, **kw)

    # The methods below are overridden and have been refactored for integration
    # of stat logging.

    def _get_xpathvalues(self, field_name, xpaths, **kw):
        return self.get_selector_values(field_name, xpaths, self.selector.xpath, **kw)

    def _get_cssvalues(self, field_name, csss, **kw):
        return self.get_selector_values(field_name, csss, self.selector.css, **kw)

    # The methods below are unique to this class and are not present in the parent.

    def get_selector_values(self, field_name, selector_rules, selector, **kw):
        """Provides an abstraction to _get_xpathvalues() and _get_cssvalues()
        since they share the same components.
        """

        self._check_selector_method()

        selector_type = selector.__name__  # either 'css' or 'xpath'

        # For every call of `add_css()` and `add_xpath()` this is incremented.
        # We'll use it as the base index of the position of the logged stats.
        index = self.field_tracker[f'{field_name}_{selector_type}']

        values = []
        for position, rule in enumerate(arg_to_iter(selector_rules), index):
            parsed_data = selector(rule).getall()
            values.append(parsed_data)
            self.write_to_stats(field_name, parsed_data, position, selector_type)
        return flatten(values)

    def write_to_stats(self, field_name, parsed_data, position, selector_type):
        """Responsible for logging the parser rules usage.

        NOTES: It's hard to easily denote which parser rule hasn't produced any
          data for the entire crawl, since ItemLoaders essentially don't know
          when the spider is going to be closed, as well as it has many
          instantiations all throughout the code.

        The implementation below where each missing parsed_data is being logged
        to the stat is clunky, but necessary. With this, we can only surmise
        that it's safe to remove parser fallback parser if it's all just
        '*/missing' in the stats.
        """

        if not self.stats or not field_name:
            return

        parser_label = (
            f"parser/{self.loader_name}/{field_name}/{selector_type}/{position}"
        )

        if parsed_data in (None, []):
            parser_label += "/missing"

        self.stats.inc_value(parser_label)

    @property
    def loader_name(self):
        return self.__class__.__name__
