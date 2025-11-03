# src/rule_engine/string_rules/core.py
from typing import Optional
from ...rule_node import RuleNode


# 原字符串相关规则
class ContainsRule(RuleNode[str]):
    type_name = "CONTAINS"

    def __init__(self, substr: str, case_sensitive: bool = True):
        self.substr = substr
        self.case_sensitive = case_sensitive

    def evaluate(self, condition: str) -> bool:
        if not self.case_sensitive:
            return self.substr.lower() in condition.lower()
        return self.substr in condition


class StartsWithRule(RuleNode[str]):
    type_name = "STARTWITH"

    def __init__(self, prefix: str):
        self.prefix = prefix

    def evaluate(self, condition: str) -> bool:
        return condition.startswith(self.prefix)


class LengthRule(RuleNode[str]):
    type_name = "LENGTH"

    def __init__(self, min_len: int, max_len: int):
        self.min_len = min_len
        self.max_len = max_len

    def evaluate(self, condition: str) -> bool:
        return self.min_len <= len(condition) <= self.max_len


# 字符串拓展规则
class EndsWithRule(RuleNode[str]):
    type_name = "ENDS_WITH"

    def __init__(self, suffix: str):
        self.suffix = suffix

    def evaluate(self, condition: str) -> bool:
        return condition.endswith(self.suffix)


class ExactMatchRule(RuleNode[str]):
    type_name = "EXACT_MATCH"

    def __init__(self, target: str, case_sensitive: bool = True):
        self.target = target
        self.case_sensitive = case_sensitive

    def evaluate(self, condition: str) -> bool:
        if self.case_sensitive:
            return condition == self.target
        return condition.lower() == self.target.lower()


class IsBlankRule(RuleNode[str]):
    type_name = "IS_BLANK"

    def __init__(self):
        pass

    def evaluate(self, condition: Optional[str]) -> bool:
        if not isinstance(condition, str) and condition is not None:
            return False
        return condition is None or condition.strip() == ""


class NotContainsRule(RuleNode[str]):
    type_name = "NOT_CONTAINS"

    def __init__(self, substr: str, case_sensitive: bool = True):
        self.substr = substr
        self.case_sensitive = case_sensitive

    def evaluate(self, condition: str) -> bool:
        if not self.case_sensitive:
            return self.substr.lower() not in condition.lower()
        return self.substr not in condition
