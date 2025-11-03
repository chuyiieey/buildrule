from typing import Any, Optional
import pytest
import re
from datetime import datetime, date, timedelta, timezone

# 导入规则引擎模块
from buildrule.rule_node import *
from buildrule.rule import *


class TestRuleNodeBase:
    """测试RuleNode基类的子类注册、序列化/反序列化核心功能"""

    def test_rule_node_type_registry(self):
        """测试子类自动注册到_type_registry，且type_name正确"""
        assert RuleNode._type_registry["EQUAL"] == EqualsRule
        assert RuleNode._type_registry["AND"] == AndNode
        assert RuleNode._type_registry["GREATERTHAN"] == GreaterThanRule
        assert RuleNode._type_registry["REGEX_FULL_MATCH"] == RegexMatchRule

    def test_serialize_basic_rule(self):
        """测试基础规则（无嵌套）的序列化"""
        equal_rule = EqualsRule(target=10.5)
        assert equal_rule.serialize() == "EQUAL(10.5)"

        contains_rule = ContainsRule(substr="test", case_sensitive=False)
        assert contains_rule.serialize() == 'CONTAINS("test",False)'

        true_rule = IsTrueRule()
        assert true_rule.serialize() == "IS_TRUE()"

    def test_serialize_nested_rule(self):
        """测试嵌套规则（逻辑组合+子规则）的序列化"""
        equal_rule = EqualsRule(5)
        contains_rule = ContainsRule("error")
        nested_rule = equal_rule.and_(contains_rule.not_())
        assert nested_rule.serialize() == 'AND(EQUAL(5),NOT(CONTAINS("error",True)))'

    def test_deserialize_basic_rule(self):
        """测试基础规则的反序列化，验证实例属性和功能一致性"""
        serialized = "RANGE(10,20)"
        range_rule = RuleNode.from_serialized(serialized)
        assert isinstance(range_rule, RangeRule)
        assert range_rule.min_val == 10 and range_rule.max_val == 20
        assert range_rule.evaluate(15) is True

        serialized = 'EXACT_MATCH("He said hello",False)'
        exact_rule = RuleNode.from_serialized(serialized)
        assert isinstance(exact_rule, ExactMatchRule)
        assert exact_rule.target == "He said hello"
        assert exact_rule.case_sensitive is False
        assert exact_rule.evaluate("he said HELLO") is True

    def test_deserialize_nested_rule(self):
        """测试嵌套规则的反序列化，验证逻辑正确性"""
        serialized = "OR(AND(EQUAL(3),GREATER_OR_EQUAL(2)),NOT(IS_BLANK()))"
        nested_rule = RuleNode.from_serialized(serialized)

        assert nested_rule.evaluate(3) is True
        assert nested_rule.evaluate(2) is True
        assert nested_rule.evaluate("test") is True
        assert nested_rule.evaluate(None) is False

    def test_deserialize_exceptions(self):
        """测试反序列化异常场景"""
        with pytest.raises(ValueError, match=re.escape("missing '('")):
            RuleNode.from_serialized("EQUAL10.5")

        with pytest.raises(ValueError, match="Unknown rule type: UNKNOWN"):
            RuleNode.from_serialized("UNKNOWN(10)")

        class BadRule(RuleNode[int]):
            type_name = "BAD"

            def __init__(self, param):
                self.missing_param = param

            def evaluate(self, condition):
                return True

        with pytest.raises(AttributeError, match=re.escape("lacks attribute 'param'")):
            BadRule(param=5).serialize()
