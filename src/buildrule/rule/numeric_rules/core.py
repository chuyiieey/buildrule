# src/rule_engine/numeric_rules/core.py
from ...rule_node import RuleNode  # 相对路径导入父包的RuleNode


# 原数值相关规则（完整迁移，代码不变）
class EqualsRule(RuleNode[float]):
    type_name = "EQUAL"

    def __init__(self, target: float):
        self.target = target

    def evaluate(self, condition: float) -> bool:
        return condition == self.target


class GreaterThanRule(RuleNode[float]):
    type_name = "GREATERTHAN"

    def __init__(self, threshold: float):
        self.threshold = threshold

    def evaluate(self, condition: float) -> bool:
        return condition > self.threshold


class RangeRule(RuleNode[float]):
    type_name = "RANGE"

    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val

    def evaluate(self, condition: float) -> bool:
        return self.min_val <= condition <= self.max_val


# 数值拓展规则（全部迁移）
class NotEqualsRule(RuleNode[float]):
    type_name = "NOT_EQUAL"

    def __init__(self, target: float):
        self.target = target

    def evaluate(self, condition: float) -> bool:
        return condition != self.target


class GreaterOrEqualRule(RuleNode[float]):
    type_name = "GREATER_OR_EQUAL"

    def __init__(self, threshold: float):
        self.threshold = threshold

    def evaluate(self, condition: float) -> bool:
        return condition >= self.threshold


class LessThanRule(RuleNode[float]):
    type_name = "LESS_THAN"

    def __init__(self, threshold: float):
        self.threshold = threshold

    def evaluate(self, condition: float) -> bool:
        return condition < self.threshold


class LessOrEqualRule(RuleNode[float]):
    type_name = "LESS_OR_EQUAL"

    def __init__(self, threshold: float):
        self.threshold = threshold

    def evaluate(self, condition: float) -> bool:
        return condition <= self.threshold


class NonZeroRule(RuleNode[float]):
    type_name = "NON_ZERO"

    def __init__(self):
        pass

    def evaluate(self, condition: float) -> bool:
        return condition != 0
