from typing import Any, Optional
import pytest
import re

# 导入规则引擎模块
from buildrule.rule_node import *
from buildrule.rule import *


class TestRuleBuilder:
    """测试RuleBuilder的链式调用、分组逻辑和异常处理"""

    def test_basic_and_combination(self):
        """测试基础AND组合：A AND B"""
        builder = RuleBuilder()
        rule = (
            builder.condition(EqualsRule(5))
            .and_()
            .condition(GreaterOrEqualRule(3))
            .build()
        )
        assert rule.evaluate(5) == True
        assert rule.evaluate(4) == False

    def test_basic_or_combination(self):
        """测试基础OR组合：A OR B"""
        builder = RuleBuilder()
        rule = (
            builder.condition(ContainsRule("error"))
            .or_()
            .condition(IsBlankRule())
            .build()
        )
        assert rule.evaluate("system error") == True
        assert rule.evaluate("   ") == True
        assert rule.evaluate("success") == False

    def test_group_logic(self):
        """测试分组逻辑：(A AND B) OR C"""
        builder = RuleBuilder()
        rule = (
            builder.group()
            .condition(EqualsRule(10))
            .and_()
            .condition(RangeRule(8, 12))
            .end_group()
            .or_()
            .condition(GreaterThanRule(20))
            .build()
        )
        assert rule.evaluate(10) == True
        assert rule.evaluate(25) == True
        assert rule.evaluate(15) == False

    def test_builder_exceptions(self):
        """测试构建器异常场景"""
        builder = RuleBuilder()

        with pytest.raises(
            ValueError, match=re.escape("Call condition() first before and_()")
        ):
            builder.and_()

        builder.condition(EqualsRule(5)).group().condition(GreaterThanRule(3))
        with pytest.raises(
            ValueError,
            match=re.escape("Unclosed groups detected: need 1 more end_group() calls"),
        ):
            builder.build()

        with pytest.raises(
            ValueError,
            match=re.escape("No rules added in the current group (empty group)"),
        ):
            builder.group().end_group()

        with pytest.raises(
            ValueError, match=re.escape("No rules added (empty rule set)")
        ):
            RuleBuilder().build()
