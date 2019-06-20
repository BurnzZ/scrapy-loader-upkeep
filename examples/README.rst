Contains examples of using the ``scrapy-loader-upkeep`` package inside Scrapy.


Simple Example
~~~~~~~~~~~~~~

.. code-block:: bash

   $ scrapy crawl quotestoscrape_simple

This should output in the stats:

.. code-block:: python

   2019-06-16 14:32:32 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
   { ...
     'parser/QuotesItemLoader/author/css/1': 10,
     'parser/QuotesItemLoader/quote/css/1': 10,
     ...
   }

This presents a simple example where 100% of the declared parser rules has been
producing values successfully.


Missing Example
~~~~~~~~~~~~~~

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
