from typing import Any, Optional
import pytest
import re
from datetime import datetime, date, timedelta, timezone

# 导入规则引擎模块
from buildrule.rule_node import *
from buildrule.rule import *


class TestIntegrationScenarios:
    """测试真实业务场景下的规则组合与判断"""

    def test_user_validation_scenario(self):
        """场景：用户信息校验（年龄18-60岁 AND 姓名非空白 AND (手机号含11位数字 OR 邮箱含@)）"""
        builder = RuleBuilder()
        user_rule = (
            builder.condition(DictValueRule("age", RangeRule(18, 60)))
            .and_()
            .condition(DictValueRule("name", NotNode(IsBlankRule())))
            .and_()
            .group()
            .condition(DictValueRule("phone", RegexMatchRule(r"^\d{11}$")))
            .or_()
            .condition(DictValueRule("email", RegexSearchRule(r"@")))
            .end_group()
            .build()
        )

        valid_user = {"age": 25, "name": "Alice", "phone": "13800138000"}
        invalid_user1 = {"age": 17, "name": "Bob", "email": "bob@test.com"}
        invalid_user2 = {"age": 30, "name": "", "phone": "13800138000"}
        invalid_user3 = {
            "age": 40,
            "name": "Charlie",
            "phone": "12345",
        }
        assert user_rule.evaluate(valid_user) == True
        assert user_rule.evaluate(invalid_user1) == False
        assert user_rule.evaluate(invalid_user2) == False
        assert user_rule.evaluate(invalid_user3) == False

    def test_order_filter_scenario(self):
        """场景：订单筛选（金额>1000元 AND 下单时间在7天内 AND (状态为待发货 OR 包含赠品)）"""
        builder = RuleBuilder()
        order_rule = (
            builder.condition(DictValueRule("amount", GreaterThanRule(1000)))
            .and_()
            .condition(DictValueRule("create_time", DateWithinDaysRule(7, 0)))
            .and_()
            .group()
            .condition(
                DictValueRule("status", ExactMatchRule("待发货", case_sensitive=False))
            )
            .or_()
            .condition(
                DictValueRule("gifts", ListHasElementRule(NotNode(IsBlankRule())))
            )
            .end_group()
            .build()
        )

        valid_order = {
            "amount": 1500,
            "create_time": datetime.now() - timedelta(3),
            "status": "待发货",
            "gifts": ["优惠券"],
        }
        invalid_order = {
            "amount": 800,
            "create_time": datetime.now() - timedelta(10),
            "status": "已发货",
            "gifts": [],
        }
        assert order_rule.evaluate(valid_order) == True
        assert order_rule.evaluate(invalid_order) == False
