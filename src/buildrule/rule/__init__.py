# 1. 汇总导出所有规则（用户可直接from rule_engine import XXXRule）
from .numeric_rules import (
    EqualsRule,
    GreaterThanRule,
    RangeRule,
    NotEqualsRule,
    GreaterOrEqualRule,
    LessThanRule,
    LessOrEqualRule,
    NonZeroRule,
)
from .string_rules import (
    ContainsRule,
    StartsWithRule,
    LengthRule,
    EndsWithRule,
    ExactMatchRule,
    IsBlankRule,
    NotContainsRule,
)
from .datetime_rules import (
    DateAfterRule,
    DateBeforeRule,
    DateInRangeRule,
    DateTodayRule,
    DateWithinDaysRule,
)
from .set_rules import SetContainsRule, SetNotContainsRule, SetSizeRule
from .list_rules import ListHasElementRule, ListAllElementsRule, ListIndexRule
from .boolean_rules import IsTrueRule, IsFalseRule
from .regex_rules import RegexMatchRule, RegexSearchRule
from .dict_ext_rules import (
    DictKeyExistsRule,
    DictValueRule,
    DictKeyNotExistsRule,
    DictValueNotRule,
)
from .xml_rules import XmlTagExistsRule, XmlAttributeMatchRule

# 2. 导出子包本身（用户可from rule_engine.numeric_rules import XXXRule）
from . import (
    numeric_rules,
    string_rules,
    datetime_rules,
    set_rules,
    list_rules,
    boolean_rules,
    regex_rules,
    dict_ext_rules,
    xml_rules,
)

all = [
    # 子包
    "numeric_rules",
    "string_rules",
    "datetime_rules",
    "set_rules",
    "list_rules",
    "boolean_rules",
    "regex_rules",
    "dict_ext_rules",
    "xml_rules",
    # 数值规则
    "EqualsRule",
    "GreaterThanRule",
    "RangeRule",
    "NotEqualsRule",
    "GreaterOrEqualRule",
    "LessThanRule",
    "LessOrEqualRule",
    "NonZeroRule",
    # 字符串规则
    "ContainsRule",
    "StartsWithRule",
    "LengthRule",
    "EndsWithRule",
    "ExactMatchRule",
    "IsBlankRule",
    "NotContainsRule",
    # 日期时间规则
    "DateAfterRule",
    "DateBeforeRule",
    "DateInRangeRule",
    "DateTodayRule",
    "DateWithinDaysRule",
    # 集合规则
    "SetContainsRule",
    "SetNotContainsRule",
    "SetSizeRule",
    # 列表规则
    "ListHasElementRule",
    "ListAllElementsRule",
    "ListIndexRule",
    # 布尔规则
    "IsTrueRule",
    "IsFalseRule",
    # 正则规则
    "RegexMatchRule",
    "RegexSearchRule",
    # 字典拓展规则
    "DictKeyExistsRule",
    "DictValueRule",
    "DictKeyNotExistsRule",
    "DictValueNotRule",
    # XML规则
    "XmlTagExistsRule",
    "XmlAttributeMatchRule",
]
