# BuildRule 项目说明文档

## 1. 项目概述

BuildRule是一个通用规则引擎库，提供灵活的规则定义、组合和执行功能。该库支持自定义规则节点、复杂逻辑组合（AND/OR/NOT）、自动序列化/反序列化，可用于数值判断、字符串匹配、XML验证、字典对象校验等多种场景，具备高度可扩展性。

主要特点：
- 基于泛型的类型安全规则定义
- 支持复杂逻辑组合和分组优先级
- 内置丰富的常用规则类型
- 自动序列化和反序列化机制
- 简洁直观的链式API设计
- 易于扩展的自定义规则体系

## 2. 技术架构

### 2.1 核心架构

BuildRule采用面向对象的设计模式，以RuleNode基类为核心，通过继承机制实现各种规则类型。项目整体架构如下：

- **RuleNode**：所有规则的基类，提供基础框架和序列化/反序列化功能
- **逻辑组合节点**：AndNode、OrNode、NotNode用于实现规则组合
- **RuleBuilder**：用于通过链式调用构建复杂规则表达式
- **专用规则实现**：按数据类型分类的各种具体规则实现

### 2.2 模块结构

```
buildrule/
├── __init__.py       # 包导出定义
├── rule_node.py      # 核心节点类和构建器
└── rule/             # 规则实现目录
    ├── __init__.py   # 规则导出定义
    ├── numeric_rules/     # 数值相关规则
    ├── string_rules/      # 字符串相关规则
    ├── datetime_rules/    # 日期时间相关规则
    ├── set_rules/         # 集合相关规则
    ├── list_rules/        # 列表相关规则
    ├── boolean_rules/     # 布尔相关规则
    ├── regex_rules/       # 正则表达式相关规则
    ├── dict_ext_rules/    # 字典扩展相关规则
    └── xml_rules/         # XML相关规则
```

### 2.3 设计模式

1. **策略模式**：不同规则实现了相同的evaluate接口，但具有不同的判断逻辑
2. **组合模式**：通过AndNode、OrNode、NotNode组合简单规则形成复杂规则
3. **构建者模式**：RuleBuilder提供流畅的API构建复杂规则表达式
4. **注册表模式**：通过_type_registry实现规则类型的自动注册和发现
5. **工厂模式**：通过from_serialized方法实现规则实例的动态创建

## 3. 核心功能

### 3.1 规则节点系统

RuleNode是整个库的核心抽象，所有具体规则都继承自这个基类。它提供了：

- 自动子类注册机制
- 序列化和反序列化功能
- 逻辑组合方法（and_、or_、not_）

```python
# 规则节点核心接口
class RuleNode(Generic[ConditionType]):
    def evaluate(self, condition: ConditionType) -> bool: ...
    def serialize(self) -> str: ...
    @classmethod
    def from_serialized(cls, data: str) -> "RuleNode": ...
```

### 3.2 逻辑组合功能

支持通过AND、OR、NOT操作符组合多个规则，形成复杂的逻辑表达式：

```python
# 逻辑组合示例
rule = equals_rule.and_(contains_rule.not_())
# 等同于：(condition == target) AND (not condition.contains(substr))
```

### 3.3 规则构建器

RuleBuilder提供了链式调用API，用于构建复杂的规则表达式，支持分组逻辑：

```python
# 构建复杂规则：(A AND B) OR C
rule = builder.group()
    .condition(A)
    .and_()
    .condition(B)
    .end_group()
    .or_()
    .condition(C)
    .build()
```

### 3.4 内置规则类型

库提供了丰富的内置规则类型，涵盖多种数据类型的常见判断场景：

- **数值规则**：等于、大于、小于、范围判断等
- **字符串规则**：包含、开始于、结束于、精确匹配等
- **日期时间规则**：日期比较、范围内判断等
- **集合规则**：包含元素、大小判断等
- **列表规则**：元素存在性、全元素检查等
- **布尔规则**：True/False判断
- **正则规则**：正则匹配
- **字典规则**：键存在性、值判断等
- **XML规则**：标签存在性、属性匹配等

### 3.5 序列化与反序列化

支持规则表达式的自动序列化和反序列化，便于存储和传输：

```python
# 序列化
serialized = rule.serialize()  # 例如: "AND(EQUAL(5),NOT(CONTAINS(\"error\",True)))"

# 反序列化
rule = RuleNode.from_serialized(serialized)
```

## 4. 关键API

### 4.1 RuleNode 基类

- **evaluate(condition)**: 执行规则判断，返回布尔结果
- **serialize()**: 将规则序列化为字符串
- **from_serialized(data)**: 从字符串反序列化规则
- **and_(other)**: 与另一规则进行AND组合
- **or_(other)**: 与另一规则进行OR组合
- **not_()**: 对规则结果取反

### 4.2 RuleBuilder 类

- **condition(node)**: 添加基础规则节点
- **and_()**: 声明后续规则使用AND逻辑
- **or_()**: 声明后续规则使用OR逻辑
- **group()**: 开始规则分组
- **end_group()**: 结束规则分组
- **build()**: 完成构建并返回根规则节点

### 4.3 常用规则类

- **EqualsRule(target)**: 判断是否等于目标值
- **RangeRule(min_val, max_val)**: 判断是否在范围内
- **ContainsRule(substr, case_sensitive=True)**: 判断是否包含子串
- **RegexMatchRule(pattern)**: 判断是否匹配正则表达式
- **DictKeyExistsRule(key)**: 判断字典是否包含指定键

## 5. 技术栈与依赖

- **Python版本**: >= 3.8
- **主要依赖**: 无外部运行时依赖
- **开发依赖**:
  - pytest: 单元测试框架
  - mypy: 类型检查
  - black: 代码格式化
  - sphinx: 文档生成

## 6. 使用场景

### 6.1 业务规则引擎

适用于需要灵活配置业务规则的场景，如风控系统、审批流程、定价策略等。

### 6.2 数据验证

可用于数据输入验证、配置文件校验、API参数验证等场景。

### 6.3 动态条件执行

支持根据运行时条件动态决定执行路径，适用于工作流系统、自动化脚本等。

### 6.4 配置化逻辑

允许通过配置文件定义业务逻辑，无需修改代码即可调整规则。

## 7. 扩展指南

要创建自定义规则，只需继承RuleNode基类并实现evaluate方法：

```python
class MyCustomRule(RuleNode[MyType]):
    type_name = "CUSTOM_RULE"  # 可选，自定义类型名
    
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
    
    def evaluate(self, condition: MyType) -> bool:
        # 实现自定义判断逻辑
        return condition.some_property == self.param1
```

自定义规则会自动注册到系统中，可通过from_serialized方法反序列化使用。

## 8. 总结

BuildRule提供了一个灵活、可扩展的规则引擎框架，通过简洁的API和丰富的内置规则，使开发者能够轻松实现复杂的业务规则逻辑。其设计注重类型安全、易用性和可扩展性，适用于各种需要规则判断和逻辑组合的应用场景。