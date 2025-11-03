# src/rule_engine/dict_ext_rules/core.py
from ...rule_node import RuleNode


class DictKeyExistsRule(RuleNode[dict]):
    type_name = "DICTKEYEXISTS"

    def __init__(self, key: str):
        self.key = key

    def evaluate(self, condition: dict) -> bool:
        return self.key in condition


class DictValueRule(RuleNode[dict]):
    type_name = "DICTVALUE"

    def __init__(self, key: str, sub_rule: RuleNode):
        self.key = key
        self.sub_rule = sub_rule

    def evaluate(self, condition: dict) -> bool:
        if self.key not in condition:
            return False
        return self.sub_rule.evaluate(condition[self.key])


class DictKeyNotExistsRule(RuleNode[dict]):
    type_name = "DICT_KEY_NOT_EXISTS"

    def __init__(self, key: str):
        self.key = key

    def evaluate(self, condition: dict) -> bool:
        return self.key not in condition


class DictValueNotRule(RuleNode[dict]):
    type_name = "DICT_VALUE_NOT"

    def __init__(self, key: str, sub_rule: RuleNode):
        self.key = key
        self.sub_rule = sub_rule

    def evaluate(self, condition: dict) -> bool:
        if self.key not in condition:
            return True
        return not self.sub_rule.evaluate(condition[self.key])
