# src/rule_engine/boolean_rules/core.py
from ...rule_node import RuleNode


class IsTrueRule(RuleNode[bool]):
    type_name = "IS_TRUE"

    def __init__(self):
        pass

    def evaluate(self, condition: bool) -> bool:
        return condition is True


class IsFalseRule(RuleNode[bool]):
    type_name = "IS_FALSE"

    def __init__(self):
        pass

    def evaluate(self, condition: bool) -> bool:
        return condition is False
