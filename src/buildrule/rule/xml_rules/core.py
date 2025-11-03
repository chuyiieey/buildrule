# src/rule_engine/xml_rules/core.py
import re
from typing import Pattern
from ...rule_node import RuleNode


class XmlTagExistsRule(RuleNode[str]):
    type_name = "XML_TAG_EXISTS"

    def __init__(self, tag_name: str):
        self.open_tag = f"<{tag_name}"
        self.close_tag = f"</{tag_name}>"

    def evaluate(self, condition: str) -> bool:
        return self.open_tag in condition or self.close_tag in condition


class XmlAttributeMatchRule(RuleNode[str]):
    type_name = "XML_ATTR_MATCH"

    def __init__(self, tag_name: str, attr_name: str, attr_value: str):
        pattern = (
            rf"<{tag_name}\s+.*{attr_name}\s*=\s*['\"]{re.escape(attr_value)}['\"]"
        )
        self.pattern: Pattern[str] = re.compile(pattern, re.IGNORECASE)

    def evaluate(self, condition: str) -> bool:
        return self.pattern.search(condition) is not None
