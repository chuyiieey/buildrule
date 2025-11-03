# src/rule_engine/list_rules/core.py
from typing import List, Any
from ...rule_node import RuleNode


class ListHasElementRule(RuleNode[List[Any]]):
    type_name = "LIST_HAS_ELEMENT"

    def __init__(self, sub_rule: RuleNode):
        self.sub_rule = sub_rule

    def evaluate(self, condition: List[Any]) -> bool:
        return any(self.sub_rule.evaluate(item) for item in condition)


class ListAllElementsRule(RuleNode[List[Any]]):
    type_name = "LIST_ALL_ELEMENTS"

    def __init__(self, sub_rule: RuleNode):
        self.sub_rule = sub_rule

    def evaluate(self, condition: List[Any]) -> bool:
        return all(self.sub_rule.evaluate(item) for item in condition)


class ListIndexRule(RuleNode[List[Any]]):
    type_name = "LIST_INDEX"

    def __init__(self, index: int, sub_rule: RuleNode):
        self.index = index
        self.sub_rule = sub_rule

    def evaluate(self, condition: List[Any]) -> bool:
        try:
            target_element = condition[self.index]
            return self.sub_rule.evaluate(target_element)
        except IndexError:
            return False
