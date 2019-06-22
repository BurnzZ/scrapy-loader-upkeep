import pytest
from unittest import mock

from scrapy_loader_upkeep import ItemLoader
from scrapy.utils.python import flatten
from scrapy.http import TextResponse
from scrapy import Item, Field


def test_get_selector_values_with_no_selector():
    """It should raise an error if it's not configured with any Selector."""

    loader = ItemLoader()

    with pytest.raises(RuntimeError) as err:
        loader.get_selector_values("field_name", [], None)


def test_get_selector_values():
    """Selectors must be properly called as well as correctly flatten the data."""

    selector_rules = ["#rule1", "#rule2", "#rule3"]
    field_name = "field"
    parsed_data = ["data1", "data2"]

    mock_selector = mock.Mock()
    mock_selector().getall.return_value = parsed_data
    mock_selector.__name__ = "css"

    loader = ItemLoader(selector=mock_selector)
    loader.write_to_stats = mock.Mock()

    result = loader.get_selector_values(field_name, selector_rules, mock_selector)

    assert result == flatten([parsed_data] * len(selector_rules))

    mock_selector.assert_has_calls(
        [
            mock.call(selector_rules[0]),
            mock.call().getall(),
            mock.call(selector_rules[1]),
            mock.call().getall(),
            mock.call(selector_rules[2]),
            mock.call().getall(),
        ]
    )

    loader.write_to_stats.assert_has_calls(
        [
            mock.call(field_name, parsed_data, 1, "css"),
            mock.call(field_name, parsed_data, 2, "css"),
            mock.call(field_name, parsed_data, 3, "css"),
        ]
    )


def test_write_to_stats_with_uninjected_stat_dependency():
    """It should not call stats when the stat dependency isn't available."""

    loader = ItemLoader()
    loader.stats = mock.MagicMock()
    loader.stats.__bool__.return_value = False  # don't pass the if-condition

    assert loader.write_to_stats("field_name", "parsed_data", 0, "xpath") == None
    assert not loader.stats.inc_value.called


def test_write_to_stats_with_no_parsed_data():
    """It should not call stats when parsing the data returned None."""

    loader = ItemLoader()
    loader.stats = mock.Mock()

    parsed_data = None
    expected_stat_key = "parser/ItemLoader/field_name/css/0/missing"

    assert loader.write_to_stats("field_name", parsed_data, 0, "css") == None
    loader.stats.inc_value.assert_called_once_with(expected_stat_key)


def test_write_to_stats():
    """It should incremenent the correct key in the stat."""

    loader = ItemLoader()
    loader.stats = mock.MagicMock()

    expected_stat_key = "parser/ItemLoader/field_name/css/0"

    # Rules with values
    assert loader.write_to_stats("field_name", "parsed_data", 123, "css") == None

    # Rules that hasn't rendered any values
    assert loader.write_to_stats("field_name", None, 456, "css") == None
    assert loader.write_to_stats("field_name", [], 789, "css") == None

    loader.stats.inc_value.assert_has_calls(
        [
            mock.call("parser/ItemLoader/field_name/css/123"),
            mock.call("parser/ItemLoader/field_name/css/456/missing"),
            mock.call("parser/ItemLoader/field_name/css/789/missing"),
        ]
    )


TEST_HTML_BODY = """
<html>
    <title>This is a title</title>
    <body>
        <article>
            <h2>Product #1</h2>
            <span class='price'>$1.23</span>
        </article>

        <article>
            <div class='product-title'>Product #2</div>
            <span class='price'>$9.99</span>
        </article>
    </body>
</html>
"""
RESPONSE = TextResponse('https://test.com', body=TEST_HTML_BODY, encoding='utf-8')


class TestItem(Item):
    title = Field()


class TestItemLoader(ItemLoader):
    default_item_class = TestItem


@pytest.fixture()
def loader():
    mock_stats = mock.MagicMock()
    loader = TestItemLoader(response=RESPONSE, stats=mock_stats)
    return loader


# NOTES: We'll be using the 'css' methods of ItemLoader below. The 'xpath' 
#   methods are also using the 'get_selector_values()' method underneath, the
#   same with 'css'. So we'll assume that 'xpath' would also pass the test
#   if 'css' passes.

# This assumption will hold true for now, since the current implementation of
# the 'css' and 'xpath' methods are just facades to the 'get_selector_values()'.


def test_add_css_1(loader):
    loader.add_css('title', 'article h2::text')
    loader.stats.inc_value.assert_has_calls(
        [
            mock.call("parser/TestItemLoader/title/css/1"),
        ]
    )
    assert loader.stats.inc_value.call_count == 1


def test_add_css_2(loader):
    loader.add_css('title', [
        'article h2::text',
        'article .product-title::text',
    ])
    loader.stats.inc_value.assert_has_calls(
        [
            mock.call("parser/TestItemLoader/title/css/1"),
            mock.call("parser/TestItemLoader/title/css/2"),
        ]
    )
    assert loader.stats.inc_value.call_count == 2
