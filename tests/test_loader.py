import mock
import pytest

from scrapy_loader_upkeep import ItemLoader

def test_get_selector_values_with_no_selector():
    """It should raise an error if it's not configured with any Selector."""

    loader = ItemLoader()

    mock_selector = mock.Mock()

    with pytest.raises(RuntimeError) as err:
        loader.get_selector_values([], mock_selector)
