# BuildRule

[![PyPI version](https://badge.fury.io/py/buildrule.svg)](https://badge.fury.io/py/buildrule)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/buildrule.svg)](https://pypi.org/project/buildrule/)

## 📖 项目简介

BuildRule 是一个功能强大、易于扩展的通用规则引擎库，专为构建和执行复杂业务规则而设计。它提供了灵活的规则定义、组合和执行功能，适用于各种需要动态规则处理的场景，如数据验证、业务规则引擎、风控系统等。

## ✨ 核心特性

- **类型安全**：基于泛型的规则定义，提供编译时类型检查
- **丰富的内置规则**：涵盖数值、字符串、日期时间、集合、列表、布尔值、正则表达式、字典和XML等多种数据类型的判断
- **灵活的逻辑组合**：支持AND、OR、NOT等逻辑操作，以及规则分组和优先级管理
- **简洁的链式API**：通过RuleBuilder提供流畅的规则构建体验
- **序列化支持**：规则表达式可自动序列化和反序列化，便于存储和传输
- **高度可扩展**：简单的接口设计，易于创建自定义规则
- **无外部依赖**：轻量级设计，不依赖第三方库

## 📦 安装

使用 pip 安装 BuildRule：

```bash
pip install buildrule
```

或者从源码安装：

```bash
git clone <repository-url>
cd buildrule
pip install -e .
```

## 🚀 快速开始

### 基本使用

```python
from buildrule.rule_node import RuleNode, RuleBuilder
from buildrule.rule import EqualsRule, ContainsRule, GreaterThanRule

# 创建简单规则
age_rule = EqualsRule(18)
text_rule = ContainsRule("success", case_sensitive=False)

# 执行规则判断
is_adult = age_rule.evaluate(18)  # True
has_success = text_rule.evaluate("Operation was SUCCESSful")  # True

# 组合规则
combined_rule = age_rule.and_(text_rule)

# 使用规则构建器创建复杂规则
builder = RuleBuilder()
complex_rule = (
    builder.condition(GreaterThanRule(10))
    .and_()
    .condition(ContainsRule("valid"))
    .build()
)

# 序列化和反序列化
serialized = complex_rule.serialize()
restored_rule = RuleNode.from_serialized(serialized)
```

## 🔧 使用示例

### 数据验证

```python
from buildrule.rule_node import RuleBuilder
from buildrule.rule import LengthRule, RegexMatchRule, DictValueRule, IsTrueRule

def validate_user_registration(user_data):
    builder = RuleBuilder()
    
    validation_rule = (
        builder.group()  # 用户名验证
        .condition(DictValueRule("username", LengthRule(3, 20)))
        .and_()
        .condition(DictValueRule("username", RegexMatchRule(r"^[a-zA-Z0-9_]+$")))
        .end_group()
        .and_()
        .condition(DictValueRule("email", RegexMatchRule(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")))
        .and_()
        .condition(DictValueRule("agree_terms", IsTrueRule()))
        .build()
    )
    
    return validation_rule.evaluate(user_data)
```

### 业务规则引擎

```python
from buildrule.rule_node import RuleBuilder
from buildrule.rule import GreaterThanRule, DateAfterRule, DictValueRule
from datetime import date

def create_promotion_rules():
    builder = RuleBuilder()
    
    # VIP客户折扣规则
    vip_discount_rule = (
        builder.group()
        .condition(DictValueRule("is_vip", IsTrueRule()))
        .and_()
        .condition(DictValueRule("order_amount", GreaterThanRule(1000)))
        .end_group()
        .build()
    )
    
    # 季节性促销规则
    seasonal_rule = (
        builder.condition(DictValueRule("purchase_date", DateAfterRule(date(2023, 12, 1))))
        .build()
    )
    
    return {"vip_discount": vip_discount_rule, "seasonal_promotion": seasonal_rule}
```

## 🔍 文档

完整文档请参阅以下内容：

- **中文项目说明**: [docs/cn_project_specification.md](docs/cn_project_specification.md)
- **英文项目说明**: [docs/en_project_specification.md](docs/en_project_specification.md)
- **中文使用指南**: [docs/cn_user_guide.md](docs/cn_user_guide.md)
- **英文使用指南**: [docs/en_user_guide.md](docs/en_user_guide.md)

## 🛠️ 开发与贡献

### 开发环境设置

1. 克隆仓库：
   ```bash
   git clone <repository-url>
   cd buildrule
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate  # Windows
   ```

3. 安装开发依赖：
   ```bash
   pip install -e "[dev]"
   ```

### 运行测试

```bash
pytest
```

### 代码风格检查

```bash
# 运行 mypy 进行类型检查
mypy src/

# 使用 black 格式化代码
black src/ tests/
```

## 🤝 贡献指南

我们欢迎社区贡献！如果您想参与项目开发，请遵循以下步骤：

1. Fork 项目仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 📄 许可证

BuildRule 采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件。

## 📧 联系我们

如有任何问题或建议，请通过以下方式联系我们：

- 电子邮件: chuyiieey@outlook.com
- GitHub Issues: [项目 Issues 页面](https://github.com/yourusername/buildrule/issues)

## 📊 项目状态

BuildRule 目前处于活跃开发阶段。我们正在不断改进和扩展库的功能。欢迎反馈和建议！