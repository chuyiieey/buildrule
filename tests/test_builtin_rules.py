from typing import Any, Optional
import pytest
import re
from datetime import datetime, date, timedelta, timezone

# 导入规则引擎模块
from buildrule.rule_node import *
from buildrule.rule import *


class TestBuiltinRules:
    """测试所有内置规则的判断逻辑（按类别分组）"""

    # ------------------------------
    # 4.1 数值规则
    # ------------------------------
    @pytest.mark.parametrize(
        "rule, input_val, expected",
        [
            (EqualsRule(5.0), 5.0, True),
            (EqualsRule(5.0), 4.9, False),
            (NotEqualsRule(5.0), 4.9, True),
            (NotEqualsRule(5.0), 5.0, False),
            (GreaterThanRule(10), 11, True),
            (GreaterThanRule(10), 10, False),
            (GreaterOrEqualRule(10), 10, True),
            (GreaterOrEqualRule(10), 9, False),
            (LessThanRule(20), 19, True),
            (LessThanRule(20), 20, False),
            (LessOrEqualRule(20), 20, True),
            (LessOrEqualRule(20), 21, False),
            (NonZeroRule(), 0, False),
            (NonZeroRule(), -1, True),
            (RangeRule(10, 20), 15, True),
            (RangeRule(10, 20), 10, True),
            (RangeRule(10, 20), 20, True),
            (RangeRule(10, 20), 21, False),
        ],
    )
    def test_numeric_rules(self, rule, input_val, expected):
        assert rule.evaluate(input_val) == expected

    # ------------------------------
    # 4.2 字符串规则
    # ------------------------------
    @pytest.mark.parametrize(
        "rule, input_val, expected",
        [
            (ContainsRule("test"), "test123", True),
            (ContainsRule("Test"), "test123", False),
            (ContainsRule("Test", case_sensitive=False), "test123", True),
            (NotContainsRule("error"), "success", True),
            (NotContainsRule("Error", case_sensitive=False), "error", False),
            (StartsWithRule("pre"), "prefix", True),
            (StartsWithRule("pre"), "Pre", False),
            (EndsWithRule("fix"), "prefix", True),
            (EndsWithRule("Fix"), "prefix", False),
            (ExactMatchRule("Hello"), "Hello", True),
            (ExactMatchRule("Hello", False), "hello", True),
            (ExactMatchRule("Hello"), "Hello123", False),
            (IsBlankRule(), "", True),
            (IsBlankRule(), "   ", True),
            (IsBlankRule(), None, True),
            (IsBlankRule(), "test", False),
            (IsBlankRule(), 123, False),
            (IsBlankRule(), True, False),
            (IsBlankRule(), {}, False),
            (LengthRule(3, 5), "123", True),
            (LengthRule(3, 5), "12345", True),
            (LengthRule(3, 5), "12", False),
        ],
    )
    def test_string_rules(self, rule, input_val, expected):
        assert rule.evaluate(input_val) == expected

    # ------------------------------
    # 4.3 日期时间规则
    # ------------------------------
    @pytest.fixture
    def today(self):
        return date.today()

    @pytest.fixture
    def now(self):
        return datetime.now()

    @pytest.mark.parametrize(
        "rule, input_val, expected",
        [
            (DateTodayRule(), date.today(), True),
            (DateTodayRule(), date.today() - timedelta(1), False),
            (DateAfterRule(datetime(2024, 1, 1)), datetime(2024, 1, 2), True),
            (DateAfterRule(datetime(2024, 1, 1)), datetime(2023, 12, 31), False),
            (DateBeforeRule(datetime(2024, 1, 1)), datetime(2023, 12, 31), True),
            (DateBeforeRule(datetime(2024, 1, 1)), datetime(2024, 1, 2), False),
            (
                DateInRangeRule(datetime(2024, 1, 1), datetime(2024, 1, 3)),
                datetime(2024, 1, 2),
                True,
            ),
            (
                DateInRangeRule(datetime(2024, 1, 1), datetime(2024, 1, 3)),
                datetime(2024, 1, 1),
                True,
            ),
            (DateWithinDaysRule(1, 1), datetime.now(), True),
            (DateWithinDaysRule(1, 1), datetime.now() + timedelta(2), False),
            (
                DateWithinDaysRule(1, 1),
                datetime.now(timezone.utc).astimezone().replace(tzinfo=None),
                True,
            ),
        ],
    )
    def test_datetime_rules(self, rule, input_val, expected):
        assert rule.evaluate(input_val) == expected

    # ------------------------------
    # 4.4 集合规则
    # ------------------------------
    @pytest.mark.parametrize(
        "rule, input_val, expected",
        [
            (SetContainsRule(5), {1, 2, 5}, True),
            (SetContainsRule(5), {1, 2, 3}, False),
            (SetNotContainsRule(5), {1, 2, 3}, True),
            (SetNotContainsRule(5), {1, 2, 5}, False),
            (SetSizeRule(2, 4), {1, 2, 3}, True),
            (SetSizeRule(2, 4), {1}, False),
            (SetSizeRule(2, 4), {1, 2, 3, 4}, True),
        ],
    )
    def test_set_rules(self, rule, input_val, expected):
        assert rule.evaluate(input_val) == expected

    # ------------------------------
    # 4.5 列表规则
    # ------------------------------
    @pytest.mark.parametrize(
        "rule, input_val, expected",
        [
            (ListHasElementRule(EqualsRule(5)), [1, 3, 5], True),
            (ListHasElementRule(EqualsRule(5)), [1, 3, 4], False),
            (ListAllElementsRule(GreaterThanRule(0)), [1, 2, 3], True),
            (ListAllElementsRule(GreaterThanRule(0)), [1, -2, 3], False),
            (ListIndexRule(0, EqualsRule(1)), [1, 2, 3], True),
            (ListIndexRule(-1, EqualsRule(3)), [1, 2, 3], True),
            (ListIndexRule(5, EqualsRule(1)), [1, 2, 3], False),
        ],
    )
    def test_list_rules(self, rule, input_val, expected):
        assert rule.evaluate(input_val) == expected

    # ------------------------------
    # 4.6 布尔规则
    # ------------------------------
    @pytest.mark.parametrize(
        "rule, input_val, expected",
        [
            (IsTrueRule(), True, True),
            (IsTrueRule(), False, False),
            (IsFalseRule(), False, True),
            (IsFalseRule(), True, False),
        ],
    )
    def test_boolean_rules(self, rule, input_val, expected):
        assert rule.evaluate(input_val) == expected

    # ------------------------------
    # 4.7 正则规则
    # ------------------------------
    @pytest.mark.parametrize(
        "rule, input_val, expected",
        [
            (RegexMatchRule(r"^\d{3}$"), "123", True),
            (RegexMatchRule(r"^\d{3}$"), "1234", False),
            (RegexMatchRule(r"^[A-Z]+$", re.IGNORECASE), "abc", True),
            (RegexSearchRule(r"\d+"), "abc123def", True),
            (RegexSearchRule(r"\d+"), "abcdef", False),
            (RegexSearchRule(r"error", re.IGNORECASE), "ERROR", True),
        ],
    )
    def test_regex_rules(self, rule, input_val, expected):
        assert rule.evaluate(input_val) == expected

    # ------------------------------
    # 4.8 字典规则
    # ------------------------------
    @pytest.mark.parametrize(
        "rule, input_val, expected",
        [
            (DictKeyExistsRule("name"), {"name": "Alice"}, True),
            (DictKeyExistsRule("age"), {"name": "Alice"}, False),
            (DictKeyNotExistsRule("age"), {"name": "Alice"}, True),
            (DictKeyNotExistsRule("name"), {"name": "Alice"}, False),
            (DictValueRule("age", GreaterThanRule(18)), {"age": 20}, True),
            (DictValueRule("age", GreaterThanRule(18)), {"age": 17}, False),
            (DictValueRule("age", GreaterThanRule(18)), {"name": "Alice"}, False),
            (DictValueNotRule("age", GreaterThanRule(18)), {"age": 17}, True),
            (DictValueNotRule("age", GreaterThanRule(18)), {"age": 20}, False),
            (DictValueNotRule("age", GreaterThanRule(18)), {"name": "Alice"}, True),
        ],
    )
    def test_dict_rules(self, rule, input_val, expected):
        assert rule.evaluate(input_val) == expected

    # ------------------------------
    # 4.9 XML规则
    # ------------------------------
    @pytest.mark.parametrize(
        "rule, input_val, expected",
        [
            (XmlTagExistsRule("user"), "<user><name>Alice</name></user>", True),
            (XmlTagExistsRule("age"), "<user><name>Alice</name></user>", False),
            (XmlTagExistsRule("age"), "<user><age>18</age></user>", True),
            (
                XmlAttributeMatchRule("user", "id", "123"),
                '<user id="123">Alice</user>',
                True,
            ),
            (
                XmlAttributeMatchRule("user", "id", "123"),
                '<user id="456">Alice</user>',
                False,
            ),
            (
                XmlAttributeMatchRule("user", "id", "123"),
                "<user id='123'>Alice</user>",
                True,
            ),
        ],
    )
    def test_xml_rules(self, rule, input_val, expected):
        assert rule.evaluate(input_val) == expected
