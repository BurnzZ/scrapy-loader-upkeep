scrapy-loader-upkeep 
====================

.. image:: https://img.shields.io/pypi/pyversions/scrapy-loader-upkeep.svg
    :target: https://pypi.python.org/pypi/scrapy-loader-upkeep

.. image:: https://img.shields.io/pypi/v/scrapy-loader-upkeep.svg
    :target: https://pypi.python.org/pypi/scrapy-loader-upkeep

.. image:: https://travis-ci.org/BurnzZ/scrapy-loader-upkeep.svg?branch=master
    :target: https://travis-ci.org/BurnzZ/scrapy-loader-upkeep

.. image:: https://codecov.io/gh/BurnzZ/scrapy-loader-upkeep/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/BurnzZ/scrapy-loader-upkeep

Overview
~~~~~~~~
This improves over the built-in `ItemLoader` of **Scrapy** by adding features
that focuses on the **maintainability** of the spider over time.

This allows developers to keep track of how often parsers are being used on a
crawl, allowing to safely remove obsolete css/xpath fallback rules.

Motivation
~~~~~~~~~~
Scrapy supports adding multiple css/xpath rules in its ``ItemLoader`` by default
in order to provide a convenient way for developers to keep up with site changes.

However, some sites change layouts more often than others, while some perform
A/B tests for weeks/months where developers need to accommodate those changes.

These fallback css/xpath rules gets obsolete quickly and fills up the project
with potentially dead code, posing a threat to the spiders' long term maintenance.

Original idea proposal: https://github.com/scrapy/scrapy/issues/3795

Usage
~~~~~
.. code-block:: python

    from scrapy_loader_upkeep import ItemLoader

    class SiteItemLoader(ItemLoader):
        pass

Using it inside a spider callback would look like:

.. code-block:: python

    def parse(self, response):
        loader = SiteItemLoader(response=response, stats=self.crawler.stats)

Nothing would change in the usage of this ``ItemLoader`` except for the part on
injecting stat dependency to it, which is necessary to keep track of the usage
of the parser rules.

This only works for the following ``ItemLoader`` methods:

- ``add_css()``
- ``replace_css()``
- ``add_xpath()``
- ``replace_xpath()``

Basic Spider Example
~~~~~~~~~~~~~~~~~~~~
This is taken from the `examples/ 
<https://github.com/BurnzZ/scrapy-loader-upkeep/tree/master/examples>`_
directory.

.. code-block:: bash

   $ scrapy crawl quotestoscrape_simple_has_missing

This should output in the stats:

.. code-block:: python

   2019-06-16 14:32:32 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
   { ...
     'parser/QuotesItemLoader/author/css/1': 10,
     'parser/QuotesItemLoader/quote/css/1/missing': 10,
     'parser/QuotesItemLoader/quote/css/2': 10
     ...
   }

In this example, we could see that the **1st css** rule for the ``quote`` field
has had instances of not being matched at all during the scrape.

New Feature
~~~~~~~~~~~

As with the example above, we're limited only to the positional context of when
the ``add_css()``, ``add_xpath()``, etc were called during the execution.

There will be cases where developers will be maintaining a large spider with a
lot of different parsers to handle varying layouts in the site. It would make
sense to have a better context to what a parser does or is for.

A new optional ``name`` parameter is supported to provide more context around a
given parser. This supports the two (2) main types of creating fallback parsers:

1. **multiple calls**

.. code-block:: python

   loader.add_css('NAME', 'h1::text', name='Name from h1')
   loader.add_css('NAME', 'meta[value="title"]::attr(content)', name="Name from meta tag")

would result in something like:

.. code-block:: python

   { ...
     'parser/QuotesItemLoader/NAME/css/1/Name from h1': 8,
     'parser/QuotesItemLoader/NAME/css/1/Name from h1/missing': 2,
     'parser/QuotesItemLoader/NAME/css/2/Name from meta tag': 7,
     'parser/QuotesItemLoader/NAME/css/2/Name from meta tag/missing': 3,
     ...
   }

2. **grouped parsers in a single call**

.. code-block:: python

   loader.add_css(
       'NAME',
       [
           'h1::text',
           'meta[value="title"]::attr(content)',
       ],
       name='NAMEs at the main content')
   loader.add_css(
       'NAME',
       [
           'footer .name::text',
           'div.page-end span.name::text',
       ],
       name='NAMEs at the bottom of the page')

would result in something like:

.. code-block:: python

   { ...
     'parser/QuotesItemLoader/NAME/css/1/NAMEs at the main content': 8,
     'parser/QuotesItemLoader/NAME/css/1/NAMEs at the main content/missing': 2,
     'parser/QuotesItemLoader/NAME/css/2/NAMEs at the main content': 7,
     'parser/QuotesItemLoader/NAME/css/2/NAMEs at the main content/missing': 3,
     'parser/QuotesItemLoader/NAME/css/3/NAMEs at the bottom of the page': 8,
     'parser/QuotesItemLoader/NAME/css/3/NAMEs at the bottom of the page/missing': 2,
     'parser/QuotesItemLoader/NAME/css/4/NAMEs at the bottom of the page': 7,
     'parser/QuotesItemLoader/NAME/css/4/NAMEs at the bottom of the page/missing': 3,
     ...
   }

The latter is useful in grouping fallback parsers together if they are quite
related in terms of layout/arrangement in the page.


Requirements
~~~~~~~~~~~~
Python 3.6+
