Contains examples of using the ``scrapy-loader-upkeep`` package inside Scrapy.

A symlink has been included in the example project dir in order to read the
source code. Run the following in order to test these out:

.. code-block:: bash

   $ python3 -m scrapy crawl <spider_name>


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


Example using 'name' feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ scrapy crawl quotestoscrape_use_name

This should output in the stats:

.. code-block:: python

   2019-06-16 14:32:32 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
   { ...
     'parser/QuotesItemLoader/author/css/1/basic author class': 10,
     'parser/QuotesItemLoader/quote/css/1/Quotes inside the box/missing': 10,
     'parser/QuotesItemLoader/quote/css/2/Quotes inside the box': 10,
     'parser/QuotesItemLoader/tags/css/1/underneath the author text': 10,
     ...
   }
