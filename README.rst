scrapy-loader-upkeep 
====================

.. image:: https://img.shields.io/pypi/pyversions/scrapy-loader-upkeep.svg
    :target: https://pypi.python.org/pypi/scrapy-loader-upkeep

.. image:: https://img.shields.io/pypi/v/scrapy-loader-upkeep.svg
    :target: https://pypi.python.org/pypi/scrapy-loader-upkeep

.. image:: https://travis-ci.org/BurnzZ/scrapy-loader-upkeep.svg?branch=master
    :target: https://travis-ci.org/BurnzZ/scrapy-loader-upkeep

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

Spider Example
~~~~~~~~~~~~~~
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

Requirements
~~~~~~~~~~~~
Python 3.6+
