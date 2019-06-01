import mock
import pytest

from scrapy_loader_upkeep import ItemLoader
from scrapy.utils.python import flatten


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
            mock.call(field_name, selector_rules[0], parsed_data, 0),
            mock.call(field_name, selector_rules[1], parsed_data, 1),
            mock.call(field_name, selector_rules[2], parsed_data, 2),
        ]
    )


def test_write_to_stats_with_uninjected_stat_dependency():
    """It should not call stats when the stat dependency isn't available."""

    loader = ItemLoader()
    loader.stats = mock.MagicMock()
    loader.stats.__nonzero__.return_value = False  # don't pass the if-condition

    assert loader.write_to_stats("field_name", [], "parsed_data", 0) == None
    assert not loader.stats.inc_value.called


def test_write_to_stats_with_no_parsed_data():
    """It should not call stats when parsing the data returned None."""

    loader = ItemLoader()
    loader.stats = mock.Mock()

    parsed_data = None

    assert loader.write_to_stats("field_name", [], parsed_data, 0) == None
    assert not loader.stats.inc_value.called


def test_write_to_stats():
    """It should incremenent the correct key in the stat."""

    loader = ItemLoader()
    loader.stats = mock.MagicMock()

    assert loader.write_to_stats("field_name", [], "parsed_data", 0) == None
    loader.stats.inc_value.assert_called_once_with("parser/ItemLoader/field_name/0")
