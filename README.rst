scrapy-loader-upkeep 
====================

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

Installation
~~~~~~~~~~~~
.. code-block:: bash

	$ pipenv install scrapy-loader-upkeep

Usage
~~~~~
Simply replace the import of:

.. code-block:: python

	from scrapy.loader import ItemLoader

	class SiteItemLoader(ItemLoader):
	    pass

into

.. code-block:: python

	from scrapy_loader_upkeep import ItemLoader

	class SiteItemLoader(ItemLoader):
	    pass

and it will take care of the rest.

Requirements
~~~~~~~~~~~~
Python 2.7 or Python 3.4+ (*should be the same with Scrapy*)