# src/rule_engine/regex_rules/core.py
import re
from typing import Pattern
from ...rule_node import RuleNode


class RegexMatchRule(RuleNode[str]):
    type_name = "REGEX_FULL_MATCH"

    def __init__(self, pattern: str, flags: int = 0):
        self.pattern: Pattern[str] = re.compile(pattern, flags)

    def evaluate(self, condition: str) -> bool:
        return self.pattern.fullmatch(condition) is not None


class RegexSearchRule(RuleNode[str]):
    type_name = "REGEX_SEARCH"

    def __init__(self, pattern: str, flags: int = 0):
        self.pattern: Pattern[str] = re.compile(pattern, flags)

    def evaluate(self, condition: str) -> bool:
        return self.pattern.search(condition) is not None
