# BuildRule 中文使用指南

## 📚 目录

- [BuildRule 中文使用指南](#buildrule-中文使用指南)
  - [📚 目录](#-目录)
  - [🚀 快速开始](#-快速开始)
    - [安装](#安装)
    - [基本使用](#基本使用)
  - [🔍 核心概念](#-核心概念)
    - [规则节点](#规则节点)
    - [逻辑组合](#逻辑组合)
    - [规则构建器](#规则构建器)
  - [🛠️ 内置规则详解](#️-内置规则详解)
    - [数值规则](#数值规则)
    - [字符串规则](#字符串规则)
    - [日期时间规则](#日期时间规则)
    - [集合规则](#集合规则)
    - [列表规则](#列表规则)
    - [布尔规则](#布尔规则)
    - [正则规则](#正则规则)
    - [字典规则](#字典规则)
    - [XML规则](#xml规则)
  - [🔧 高级用法](#-高级用法)
    - [序列化与反序列化](#序列化与反序列化)
    - [自定义规则](#自定义规则)
    - [复杂规则构建](#复杂规则构建)
  - [💡 使用场景示例](#-使用场景示例)
    - [数据验证](#数据验证)
    - [业务规则引擎](#业务规则引擎)
    - [配置化工作流](#配置化工作流)
  - [❓ 常见问题](#-常见问题)
  - [📝 版本历史](#-版本历史)

## 🚀 快速开始

### 安装

BuildRule 可以通过 pip 安装：

```bash
pip install buildrule
```

也可以直接从源码安装：

```bash
git clone <repository-url>
cd buildrule
pip install -e .
```

### 基本使用

以下是 BuildRule 的基本使用示例：

```python
from buildrule.rule_node import RuleNode
from buildrule.rule import EqualsRule, ContainsRule, RuleBuilder

# 1. 创建简单规则
age_rule = EqualsRule(18)
text_rule = ContainsRule("error", case_sensitive=False)

# 2. 执行规则判断
is_adult = age_rule.evaluate(18)  # True
has_error = text_rule.evaluate("系统出现Error")  # True

# 3. 组合规则
combined_rule = age_rule.and_(text_rule)
result = combined_rule.evaluate(18)  # True (但text_rule需要字符串输入，这里仅作示例)

# 4. 使用规则构建器
builder = RuleBuilder()
complex_rule = (
    builder.condition(EqualsRule(10))
    .and_()
    .condition(ContainsRule("success"))
    .build()
)
```

## 🔍 核心概念

### 规则节点

规则节点是 BuildRule 的基本构建块，所有规则都继承自 `RuleNode` 基类。每个规则节点负责对输入数据进行特定的判断，并返回布尔结果。

```python
# 规则节点的基本结构
class RuleNode(Generic[ConditionType]):
    def evaluate(self, condition: ConditionType) -> bool: ...  # 核心判断方法
```

规则节点支持泛型，可以指定输入数据的类型，提供类型安全的判断。

### 逻辑组合

BuildRule 支持通过 AND、OR、NOT 操作符组合多个规则节点，形成复杂的逻辑表达式：

```python
# AND 组合：两个规则都必须满足
rule1.and_(rule2)

# OR 组合：满足任一规则即可
rule1.or_(rule2)

# NOT 取反：规则不满足时返回 True
rule1.not_()

# 嵌套组合
rule1.and_(rule2.or_(rule3.not_()))
```

### 规则构建器

对于复杂规则，RuleBuilder 提供了更清晰的链式 API：

```python
builder = RuleBuilder()

# 构建复杂规则：(A AND B) OR (C AND D)
rule = (
    builder.group()
    .condition(A)
    .and_()
    .condition(B)
    .end_group()
    .or_()
    .group()
    .condition(C)
    .and_()
    .condition(D)
    .end_group()
    .build()
)
```

## 🛠️ 内置规则详解

### 数值规则

处理数值类型的判断：

| 规则类名 | 功能描述 | 参数说明 | 示例 |
|---------|---------|---------|------|
| EqualsRule | 判断是否等于目标值 | target: float | `EqualsRule(10.5).evaluate(10.5)` → True |
| NotEqualsRule | 判断是否不等于目标值 | target: float | `NotEqualsRule(10).evaluate(15)` → True |
| GreaterThanRule | 判断是否大于阈值 | threshold: float | `GreaterThanRule(10).evaluate(15)` → True |
| GreaterOrEqualRule | 判断是否大于等于阈值 | threshold: float | `GreaterOrEqualRule(10).evaluate(10)` → True |
| LessThanRule | 判断是否小于阈值 | threshold: float | `LessThanRule(10).evaluate(5)` → True |
| LessOrEqualRule | 判断是否小于等于阈值 | threshold: float | `LessOrEqualRule(10).evaluate(10)` → True |
| RangeRule | 判断是否在指定范围内 | min_val: float, max_val: float | `RangeRule(5, 15).evaluate(10)` → True |
| NonZeroRule | 判断是否非零 | 无 | `NonZeroRule().evaluate(5)` → True |

### 字符串规则

处理字符串类型的判断：

| 规则类名 | 功能描述 | 参数说明 | 示例 |
|---------|---------|---------|------|
| ContainsRule | 判断是否包含子串 | substr: str, case_sensitive: bool=True | `ContainsRule("hello").evaluate("hello world")` → True |
| NotContainsRule | 判断是否不包含子串 | substr: str, case_sensitive: bool=True | `NotContainsRule("error").evaluate("success")` → True |
| StartsWithRule | 判断是否以指定前缀开头 | prefix: str | `StartsWithRule("Hello").evaluate("Hello world")` → True |
| EndsWithRule | 判断是否以指定后缀结尾 | suffix: str | `EndsWithRule(".com").evaluate("example.com")` → True |
| ExactMatchRule | 判断是否完全匹配 | target: str, case_sensitive: bool=True | `ExactMatchRule("test").evaluate("test")` → True |
| LengthRule | 判断字符串长度是否在范围内 | min_len: int, max_len: int | `LengthRule(3, 10).evaluate("hello")` → True |
| IsBlankRule | 判断字符串是否为空或空白 | 无 | `IsBlankRule().evaluate("   ")` → True |

### 日期时间规则

处理日期和时间的判断：

| 规则类名 | 功能描述 | 参数说明 | 示例 |
|---------|---------|---------|------|
| DateAfterRule | 判断日期是否在指定日期之后 | target_date: date/datetime | `DateAfterRule(date(2023, 1, 1)).evaluate(date(2023, 1, 2))` → True |
| DateBeforeRule | 判断日期是否在指定日期之前 | target_date: date/datetime | `DateBeforeRule(date(2023, 1, 1)).evaluate(date(2022, 12, 31))` → True |
| DateInRangeRule | 判断日期是否在指定范围内 | start_date: date/datetime, end_date: date/datetime | `DateInRangeRule(date(2023, 1, 1), date(2023, 12, 31)).evaluate(date(2023, 6, 1))` → True |
| DateTodayRule | 判断日期是否为今天 | 无 | `DateTodayRule().evaluate(date.today())` → True |
| DateWithinDaysRule | 判断日期是否在最近N天内 | days: int | `DateWithinDaysRule(7).evaluate(date.today() - timedelta(days=5))` → True |

### 集合规则

处理集合类型的判断：

| 规则类名 | 功能描述 | 参数说明 | 示例 |
|---------|---------|---------|------|
| SetContainsRule | 判断集合是否包含元素 | element: Any | `SetContainsRule(5).evaluate({1, 2, 3, 4, 5})` → True |
| SetNotContainsRule | 判断集合是否不包含元素 | element: Any | `SetNotContainsRule(6).evaluate({1, 2, 3, 4, 5})` → True |
| SetSizeRule | 判断集合大小是否在范围内 | min_size: int, max_size: int | `SetSizeRule(3, 6).evaluate({1, 2, 3, 4})` → True |

### 列表规则

处理列表类型的判断：

| 规则类名 | 功能描述 | 参数说明 | 示例 |
|---------|---------|---------|------|
| ListHasElementRule | 判断列表是否包含元素 | element: Any | `ListHasElementRule(5).evaluate([1, 2, 3, 4, 5])` → True |
| ListAllElementsRule | 判断列表所有元素是否满足规则 | element_rule: RuleNode | `ListAllElementsRule(GreaterThanRule(0)).evaluate([1, 2, 3])` → True |
| ListIndexRule | 判断列表指定索引位置的元素是否满足规则 | index: int, element_rule: RuleNode | `ListIndexRule(0, EqualsRule("first")).evaluate(["first", "second"])` → True |

### 布尔规则

处理布尔类型的判断：

| 规则类名 | 功能描述 | 参数说明 | 示例 |
|---------|---------|---------|------|
| IsTrueRule | 判断是否为True | 无 | `IsTrueRule().evaluate(True)` → True |
| IsFalseRule | 判断是否为False | 无 | `IsFalseRule().evaluate(False)` → True |

### 正则规则

处理正则表达式匹配：

| 规则类名 | 功能描述 | 参数说明 | 示例 |
|---------|---------|---------|------|
| RegexMatchRule | 判断是否完全匹配正则表达式 | pattern: str | `RegexMatchRule(r"^\d+$").evaluate("12345")` → True |
| RegexSearchRule | 判断是否包含匹配正则表达式的子串 | pattern: str | `RegexSearchRule(r"\d+").evaluate("abc123def")` → True |

### 字典规则

处理字典类型的判断：

| 规则类名 | 功能描述 | 参数说明 | 示例 |
|---------|---------|---------|------|
| DictKeyExistsRule | 判断字典是否包含指定键 | key: Any | `DictKeyExistsRule("name").evaluate({"name": "John"})` → True |
| DictKeyNotExistsRule | 判断字典是否不包含指定键 | key: Any | `DictKeyNotExistsRule("age").evaluate({"name": "John"})` → True |
| DictValueRule | 判断字典指定键的值是否满足规则 | key: Any, value_rule: RuleNode | `DictValueRule("age", GreaterThanRule(18)).evaluate({"age": 25})` → True |
| DictValueNotRule | 判断字典指定键的值是否不满足规则 | key: Any, value_rule: RuleNode | `DictValueNotRule("age", EqualsRule(17)).evaluate({"age": 25})` → True |

### XML规则

处理XML内容的判断：

| 规则类名 | 功能描述 | 参数说明 | 示例 |
|---------|---------|---------|------|
| XmlTagExistsRule | 判断XML是否包含指定标签 | tag_name: str | `XmlTagExistsRule("user").evaluate("<user><name>John</name></user>")` → True |
| XmlAttributeMatchRule | 判断XML标签属性是否匹配 | tag_name: str, attr_name: str, attr_value: str | `XmlAttributeMatchRule("user", "id", "123").evaluate("<user id=\"123\">John</user>")` → True |

## 🔧 高级用法

### 序列化与反序列化

BuildRule 支持规则的序列化和反序列化，便于存储和传输：

```python
# 创建规则
rule = EqualsRule(10).and_(ContainsRule("success"))

# 序列化为字符串
serialized = rule.serialize()
# serialized = "AND(EQUAL(10),CONTAINS(\"success\",True))"

# 反序列化
restored_rule = RuleNode.from_serialized(serialized)

# 验证功能一致性
assert rule.evaluate(10) == restored_rule.evaluate(10)
```

序列化字符串格式为：`TYPE_NAME(param1,param2,...)`，支持嵌套规则。

### 自定义规则

创建自定义规则只需继承 RuleNode 基类并实现 evaluate 方法：

```python
from buildrule.rule_node import RuleNode

class EmailRule(RuleNode[str]):
    """判断字符串是否为有效的电子邮件地址"""
    type_name = "EMAIL_VALID"
    
    def __init__(self):
        import re
        self.pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    
    def evaluate(self, condition: str) -> bool:
        return bool(self.pattern.match(condition))

# 使用自定义规则
email_rule = EmailRule()
print(email_rule.evaluate("user@example.com"))  # True
print(email_rule.evaluate("invalid-email"))  # False

# 支持序列化和反序列化
serialized = email_rule.serialize()  # "EMAIL_VALID()"
restored = RuleNode.from_serialized(serialized)
```

自定义规则会自动注册到系统中，无需额外配置。

### 复杂规则构建

对于非常复杂的规则，可以结合规则构建器和分组逻辑：

```python
from buildrule.rule_node import RuleBuilder
from buildrule.rule import (
    EqualsRule, ContainsRule, GreaterThanRule,
    DateAfterRule, DictValueRule, ListAllElementsRule
)
from datetime import date

builder = RuleBuilder()

# 构建复杂的业务规则
complex_business_rule = (
    builder.group()  # 开始条件组：用户资格
    .condition(DictValueRule("age", GreaterThanRule(18)))  # 年龄大于18
    .and_()
    .condition(DictValueRule("is_verified", EqualsRule(True)))  # 已验证
    .end_group()
    .and_()
    .group()  # 开始条件组：订单条件
    .condition(DictValueRule("order_date", DateAfterRule(date(2023, 1, 1))))  # 2023年后的订单
    .or_()
    .condition(DictValueRule("order_amount", GreaterThanRule(1000)))  # 或订单金额大于1000
    .end_group()
    .build()
)

# 测试规则
user_data = {
    "age": 25,
    "is_verified": True,
    "order_date": date(2023, 6, 15),
    "order_amount": 1200
}

result = complex_business_rule.evaluate(user_data)
print(result)  # True (同时满足用户资格和订单条件)
```

## 💡 使用场景示例

### 数据验证

使用 BuildRule 进行数据输入验证：

```python
from buildrule.rule_node import RuleBuilder
from buildrule.rule import (
    LengthRule, RegexMatchRule, RangeRule,
    DictValueRule, IsTrueRule
)

def validate_user_registration(user_data):
    """验证用户注册数据"""
    builder = RuleBuilder()
    
    validation_rule = (
        builder.group()  # 用户名验证
        .condition(DictValueRule("username", LengthRule(3, 20)))
        .and_()
        .condition(DictValueRule("username", RegexMatchRule(r"^[a-zA-Z0-9_]+$")))
        .end_group()
        .and_()
        .condition(DictValueRule("email", RegexMatchRule(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")))  # 邮箱验证
        .and_()
        .condition(DictValueRule("age", RangeRule(18, 120)))  # 年龄验证
        .and_()
        .condition(DictValueRule("agree_terms", IsTrueRule()))  # 必须同意条款
        .build()
    )
    
    return validation_rule.evaluate(user_data)

# 测试
user1 = {
    "username": "john_doe",
    "email": "john@example.com",
    "age": 25,
    "agree_terms": True
}

user2 = {
    "username": "j",  # 用户名太短
    "email": "invalid-email",
    "age": 16,  # 年龄太小
    "agree_terms": False
}

print(validate_user_registration(user1))  # True
print(validate_user_registration(user2))  # False
```

### 业务规则引擎

实现简单的风控规则引擎：

```python
from buildrule.rule_node import RuleBuilder
from buildrule.rule import (
    GreaterThanRule, ContainsRule, DateAfterRule,
    DictValueRule, ListHasElementRule
)
from datetime import date, timedelta

def create_risk_control_rules():
    """创建风控规则"""
    builder = RuleBuilder()
    
    # 高风险规则：金额大 OR 短时间内多次交易 OR 用户在黑名单中
    high_risk_rule = (
        builder.group()  # 金额风险
        .condition(DictValueRule("transaction_amount", GreaterThanRule(50000)))
        .end_group()
        .or_()
        .group()  # 频率风险
        .condition(DictValueRule("transaction_count_24h", GreaterThanRule(20)))
        .end_group()
        .or_()
        .group()  # 黑名单风险
        .condition(ListHasElementRule("blacklisted_users", DictValueRule("user_id", ContainsRule(""))))  # 简化示例
        .end_group()
        .build()
    )
    
    # 中风险规则：新用户大额交易 OR 异常地点
    medium_risk_rule = (
        builder.group()
        .condition(DictValueRule("account_age_days", GreaterThanRule(-1)))
        .and_()
        .condition(DictValueRule("account_age_days", GreaterThanRule(30)))
        .end_group()
        .build()
    )
    
    return {
        "high_risk": high_risk_rule,
        "medium_risk": medium_risk_rule
    }

def evaluate_risk(transaction_data, rules):
    """评估交易风险"""
    risk_level = "low"
    
    if rules["high_risk"].evaluate(transaction_data):
        risk_level = "high"
    elif rules["medium_risk"].evaluate(transaction_data):
        risk_level = "medium"
    
    return risk_level

# 创建规则
rules = create_risk_control_rules()

# 测试交易
large_transaction = {
    "transaction_amount": 100000,
    "transaction_count_24h": 5,
    "user_id": "user123",
    "account_age_days": 365
}

print(evaluate_risk(large_transaction, rules))  # "high"
```

### 配置化工作流

基于规则配置的工作流判断：

```python
from buildrule.rule_node import RuleNode, RuleBuilder
from buildrule.rule import (
    EqualsRule, GreaterThanRule, ContainsRule,
    DateAfterRule, DictValueRule
)
from datetime import date

def load_workflow_rules(rule_configs):
    """从配置加载工作流规则"""
    rules = {}
    
    for step_name, serialized_rule in rule_configs.items():
        rules[step_name] = RuleNode.from_serialized(serialized_rule)
    
    return rules

def execute_workflow(data, rules):
    """执行工作流判断"""
    results = {}
    
    for step_name, rule in rules.items():
        results[step_name] = rule.evaluate(data)
    
    return results

# 配置化的工作流规则
workflow_config = {
    "step1_approval": "GREATER_THAN(10000)",  # 金额大于10000需审批
    "step2_manager_review": "AND(GREATER_THAN(50000),CONTAINS(\"contract\",True))",  # 大额合同需经理审核
    "step3_finance_check": "OR(GREATER_THAN(100000),DATE_AFTER(2023-12-31))"  # 超大额或跨年度需财务检查
}

# 加载规则
rules = load_workflow_rules(workflow_config)

# 测试数据
project_data = {
    "amount": 75000,
    "has_contract": True,
    "submit_date": date(2023, 11, 15)
}

# 执行工作流
results = execute_workflow(project_data["amount"], rules)
print(results)
# 输出示例: {
#     "step1_approval": True,
#     "step2_manager_review": True,
#     "step3_finance_check": False
# }
```

## ❓ 常见问题

**Q: 如何处理不同数据类型的规则组合？**

A: 当需要组合处理不同数据类型的规则时，可以使用字典规则来访问不同字段：

```python
from buildrule.rule_node import RuleBuilder
from buildrule.rule import DictValueRule, EqualsRule, ContainsRule

builder = RuleBuilder()
rule = (
    builder.condition(DictValueRule("age", EqualsRule(18)))
    .and_()
    .condition(DictValueRule("name", ContainsRule("John")))
    .build()
)

# 输入是一个字典，包含不同类型的字段
user_data = {"age": 18, "name": "John Doe"}
result = rule.evaluate(user_data)  # True
```

**Q: 规则执行性能如何？**

A: BuildRule 的设计注重性能，特别是对于：
- 简单规则的直接执行非常高效
- 逻辑组合使用短路求值优化（如 AND 组合中第一个规则失败则不再执行后续规则）
- 序列化/反序列化机制针对常见场景进行了优化

对于非常复杂的规则表达式或高频调用场景，可以考虑：
- 缓存常用规则实例
- 预编译正则表达式规则
- 避免过于深层次的规则嵌套

**Q: 如何调试规则？**

A: 调试规则的几种方法：

1. 序列化规则查看结构：`print(rule.serialize())`
2. 分步执行并打印中间结果
3. 创建自定义规则时添加日志输出
4. 使用简单的测试数据验证单个规则的行为

**Q: 是否支持异步规则执行？**

A: 当前版本的 BuildRule 主要设计为同步执行模型。对于需要异步执行的场景，可以在应用层面结合 asyncio 使用：

```python
import asyncio
from buildrule.rule import EqualsRule

async def async_evaluate(rule, data):
    # 在单独的线程中执行规则评估
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, rule.evaluate, data)

# 使用示例
rule = EqualsRule(10)
async def main():
    result = await async_evaluate(rule, 10)
    print(result)

asyncio.run(main())
```

## 📝 版本历史

- **0.0.1** - 初始版本
  - 核心规则节点系统
  - 基础逻辑组合（AND/OR/NOT）
  - 规则构建器
  - 序列化/反序列化支持
  - 多种内置规则类型
  - 完整的单元测试