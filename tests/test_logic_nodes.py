from typing import Any, Optional
import pytest

# 导入规则引擎模块
from buildrule.rule_node import *
from buildrule.rule import *


class TestLogicNodes:
    """测试逻辑组合节点的判断逻辑"""

    @pytest.fixture
    def true_rule(self):
        """返回始终为True的规则"""

        class TrueRule(RuleNode[Any]):
            type_name = "TRUE"

            def evaluate(self, condition):
                return True

        return TrueRule()

    @pytest.fixture
    def false_rule(self):
        """返回始终为False的规则"""

        class FalseRule(RuleNode[Any]):
            type_name = "FALSE"

            def evaluate(self, condition):
                return False

        return FalseRule()

    @pytest.mark.parametrize(
        "left_res, right_res, expected",
        [
            (True, True, True),
            (True, False, False),
            (False, True, False),
            (False, False, False),
        ],
    )
    def test_and_node_evaluation(
        self, true_rule, false_rule, left_res, right_res, expected
    ):
        left = true_rule if left_res else false_rule
        right = true_rule if right_res else false_rule
        and_node = AndNode(left, right)
        assert and_node.evaluate(None) == expected

    @pytest.mark.parametrize(
        "left_res, right_res, expected",
        [
            (True, True, True),
            (True, False, True),
            (False, True, True),
            (False, False, False),
        ],
    )
    def test_or_node_evaluation(
        self, true_rule, false_rule, left_res, right_res, expected
    ):
        left = true_rule if left_res else false_rule
        right = true_rule if right_res else false_rule
        or_node = OrNode(left, right)
        assert or_node.evaluate(None) == expected

    @pytest.mark.parametrize("origin_res, expected", [(True, False), (False, True)])
    def test_not_node_evaluation(self, true_rule, false_rule, origin_res, expected):
        origin = true_rule if origin_res else false_rule
        not_node = NotNode(origin)
        assert not_node.evaluate(None) == expected

    def test_nested_logic(self, true_rule, false_rule):
        """测试 (True AND NOT(False)) OR False → 真"""
        nested = AndNode(true_rule, NotNode(false_rule)).or_(false_rule)
        assert nested.evaluate(None) == True
