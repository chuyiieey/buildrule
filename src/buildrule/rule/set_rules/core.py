# src/rule_engine/set_rules/core.py
from typing import Set, Any
from ...rule_node import RuleNode


class SetContainsRule(RuleNode[Set[Any]]):
    type_name = "SET_CONTAINS"

    def __init__(self, element: Any):
        self.element = element

    def evaluate(self, condition: Set[Any]) -> bool:
        return self.element in condition


class SetNotContainsRule(RuleNode[Set[Any]]):
    type_name = "SET_NOT_CONTAINS"

    def __init__(self, element: Any):
        self.element = element

    def evaluate(self, condition: Set[Any]) -> bool:
        return self.element not in condition


class SetSizeRule(RuleNode[Set[Any]]):
    type_name = "SET_SIZE"

    def __init__(self, min_size: int, max_size: int):
        self.min_size = min_size
        self.max_size = max_size

    def evaluate(self, condition: Set[Any]) -> bool:
        return self.min_size <= len(condition) <= self.max_size
