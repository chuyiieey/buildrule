"""
BuildRule: A flexible, extensible rule engine library.

This module provides a general-purpose rule engine for defining,
combining, and evaluating complex business rules with support for
serialization, deserialization, and custom rule creation.
"""

# 导出核心类和模块
from .rule_node import RuleNode, RuleBuilder
from . import rule

# 定义所有导出内容（避免*导入时暴露无关内容）
__all__ = [
    # 核心类
    "RuleNode",
    "RuleBuilder",
    # 规则模块
    "rule",
]
