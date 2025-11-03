# BuildRule English User Guide

## 📚 Table of Contents

- [BuildRule English User Guide](#buildrule-english-user-guide)
  - [📚 Table of Contents](#-table-of-contents)
  - [🚀 Quick Start](#-quick-start)
    - [Installation](#installation)
    - [Basic Usage](#basic-usage)
  - [🔍 Core Concepts](#-core-concepts)
    - [Rule Nodes](#rule-nodes)
    - [Logical Combinations](#logical-combinations)
    - [Rule Builder](#rule-builder)
  - [🛠️ Built-in Rules](#️-built-in-rules)
    - [Numeric Rules](#numeric-rules)
    - [String Rules](#string-rules)
    - [DateTime Rules](#datetime-rules)
    - [Set Rules](#set-rules)
    - [List Rules](#list-rules)
    - [Boolean Rules](#boolean-rules)
    - [Regex Rules](#regex-rules)
    - [Dictionary Rules](#dictionary-rules)
    - [XML Rules](#xml-rules)
  - [🔧 Advanced Usage](#-advanced-usage)
    - [Serialization and Deserialization](#serialization-and-deserialization)
    - [Custom Rules](#custom-rules)
    - [Complex Rule Construction](#complex-rule-construction)
  - [💡 Use Case Examples](#-use-case-examples)
    - [Data Validation](#data-validation)
    - [Business Rule Engine](#business-rule-engine)
    - [Configurable Workflow](#configurable-workflow)
  - [❓ Frequently Asked Questions](#-frequently-asked-questions)
  - [📝 Version History](#-version-history)

## 🚀 Quick Start

### Installation

BuildRule can be installed via pip:

```bash
pip install buildrule
```

Or directly from source:

```bash
git clone <repository-url>
cd buildrule
pip install -e .
```

### Basic Usage

Here's a basic example of using BuildRule:

```python
from buildrule.rule_node import RuleNode
from buildrule.rule import EqualsRule, ContainsRule, RuleBuilder

# 1. Create simple rules
age_rule = EqualsRule(18)
text_rule = ContainsRule("error", case_sensitive=False)

# 2. Execute rule evaluation
is_adult = age_rule.evaluate(18)  # True
has_error = text_rule.evaluate("System Error occurred")  # True

# 3. Combine rules
combined_rule = age_rule.and_(text_rule)
result = combined_rule.evaluate(18)  # True (note: text_rule would need string input in real usage)

# 4. Use rule builder
builder = RuleBuilder()
complex_rule = (
    builder.condition(EqualsRule(10))
    .and_()
    .condition(ContainsRule("success"))
    .build()
)
```

## 🔍 Core Concepts

### Rule Nodes

Rule nodes are the basic building blocks of BuildRule. All rules inherit from the `RuleNode` base class. Each rule node is responsible for making a specific judgment on input data and returning a boolean result.

```python
# Basic structure of a rule node
class RuleNode(Generic[ConditionType]):
    def evaluate(self, condition: ConditionType) -> bool: ...  # Core evaluation method
```

Rule nodes support generics, allowing you to specify the type of input data for type-safe evaluation.

### Logical Combinations

BuildRule supports combining multiple rule nodes through AND, OR, and NOT operators to form complex logical expressions:

```python
# AND combination: both rules must be satisfied
rule1.and_(rule2)

# OR combination: either rule must be satisfied
rule1.or_(rule2)

# NOT negation: returns True when the rule is not satisfied
rule1.not_()

# Nested combinations
rule1.and_(rule2.or_(rule3.not_()))
```

### Rule Builder

For complex rules, the RuleBuilder provides a clearer chained API:

```python
builder = RuleBuilder()

# Build complex rule: (A AND B) OR (C AND D)
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

## 🛠️ Built-in Rules

### Numeric Rules

Handle numeric type judgments:

| Rule Class | Description | Parameters | Example |
|------------|-------------|------------|--------|
| EqualsRule | Checks if equals target value | target: float | `EqualsRule(10.5).evaluate(10.5)` → True |
| NotEqualsRule | Checks if not equals target value | target: float | `NotEqualsRule(10).evaluate(15)` → True |
| GreaterThanRule | Checks if greater than threshold | threshold: float | `GreaterThanRule(10).evaluate(15)` → True |
| GreaterOrEqualRule | Checks if greater than or equal to threshold | threshold: float | `GreaterOrEqualRule(10).evaluate(10)` → True |
| LessThanRule | Checks if less than threshold | threshold: float | `LessThanRule(10).evaluate(5)` → True |
| LessOrEqualRule | Checks if less than or equal to threshold | threshold: float | `LessOrEqualRule(10).evaluate(10)` → True |
| RangeRule | Checks if in specified range | min_val: float, max_val: float | `RangeRule(5, 15).evaluate(10)` → True |
| NonZeroRule | Checks if non-zero | None | `NonZeroRule().evaluate(5)` → True |

### String Rules

Handle string type judgments:

| Rule Class | Description | Parameters | Example |
|------------|-------------|------------|--------|
| ContainsRule | Checks if contains substring | substr: str, case_sensitive: bool=True | `ContainsRule("hello").evaluate("hello world")` → True |
| NotContainsRule | Checks if does not contain substring | substr: str, case_sensitive: bool=True | `NotContainsRule("error").evaluate("success")` → True |
| StartsWithRule | Checks if starts with prefix | prefix: str | `StartsWithRule("Hello").evaluate("Hello world")` → True |
| EndsWithRule | Checks if ends with suffix | suffix: str | `EndsWithRule(".com").evaluate("example.com")` → True |
| ExactMatchRule | Checks if exact match | target: str, case_sensitive: bool=True | `ExactMatchRule("test").evaluate("test")` → True |
| LengthRule | Checks if string length is in range | min_len: int, max_len: int | `LengthRule(3, 10).evaluate("hello")` → True |
| IsBlankRule | Checks if string is empty or whitespace | None | `IsBlankRule().evaluate("   ")` → True |

### DateTime Rules

Handle date and time judgments:

| Rule Class | Description | Parameters | Example |
|------------|-------------|------------|--------|
| DateAfterRule | Checks if date is after specified date | target_date: date/datetime | `DateAfterRule(date(2023, 1, 1)).evaluate(date(2023, 1, 2))` → True |
| DateBeforeRule | Checks if date is before specified date | target_date: date/datetime | `DateBeforeRule(date(2023, 1, 1)).evaluate(date(2022, 12, 31))` → True |
| DateInRangeRule | Checks if date is in specified range | start_date: date/datetime, end_date: date/datetime | `DateInRangeRule(date(2023, 1, 1), date(2023, 12, 31)).evaluate(date(2023, 6, 1))` → True |
| DateTodayRule | Checks if date is today | None | `DateTodayRule().evaluate(date.today())` → True |
| DateWithinDaysRule | Checks if date is within recent N days | days: int | `DateWithinDaysRule(7).evaluate(date.today() - timedelta(days=5))` → True |

### Set Rules

Handle set type judgments:

| Rule Class | Description | Parameters | Example |
|------------|-------------|------------|--------|
| SetContainsRule | Checks if set contains element | element: Any | `SetContainsRule(5).evaluate({1, 2, 3, 4, 5})` → True |
| SetNotContainsRule | Checks if set does not contain element | element: Any | `SetNotContainsRule(6).evaluate({1, 2, 3, 4, 5})` → True |
| SetSizeRule | Checks if set size is in range | min_size: int, max_size: int | `SetSizeRule(3, 6).evaluate({1, 2, 3, 4})` → True |

### List Rules

Handle list type judgments:

| Rule Class | Description | Parameters | Example |
|------------|-------------|------------|--------|
| ListHasElementRule | Checks if list contains element | element: Any | `ListHasElementRule(5).evaluate([1, 2, 3, 4, 5])` → True |
| ListAllElementsRule | Checks if all list elements satisfy rule | element_rule: RuleNode | `ListAllElementsRule(GreaterThanRule(0)).evaluate([1, 2, 3])` → True |
| ListIndexRule | Checks if element at index satisfies rule | index: int, element_rule: RuleNode | `ListIndexRule(0, EqualsRule("first")).evaluate(["first", "second"])` → True |

### Boolean Rules

Handle boolean type judgments:

| Rule Class | Description | Parameters | Example |
|------------|-------------|------------|--------|
| IsTrueRule | Checks if value is True | None | `IsTrueRule().evaluate(True)` → True |
| IsFalseRule | Checks if value is False | None | `IsFalseRule().evaluate(False)` → True |

### Regex Rules

Handle regular expression matching:

| Rule Class | Description | Parameters | Example |
|------------|-------------|------------|--------|
| RegexMatchRule | Checks if completely matches regex | pattern: str | `RegexMatchRule(r"^\d+$").evaluate("12345")` → True |
| RegexSearchRule | Checks if contains regex match | pattern: str | `RegexSearchRule(r"\d+").evaluate("abc123def")` → True |

### Dictionary Rules

Handle dictionary type judgments:

| Rule Class | Description | Parameters | Example |
|------------|-------------|------------|--------|
| DictKeyExistsRule | Checks if dictionary contains key | key: Any | `DictKeyExistsRule("name").evaluate({"name": "John"})` → True |
| DictKeyNotExistsRule | Checks if dictionary does not contain key | key: Any | `DictKeyNotExistsRule("age").evaluate({"name": "John"})` → True |
| DictValueRule | Checks if dictionary value satisfies rule | key: Any, value_rule: RuleNode | `DictValueRule("age", GreaterThanRule(18)).evaluate({"age": 25})` → True |
| DictValueNotRule | Checks if dictionary value does not satisfy rule | key: Any, value_rule: RuleNode | `DictValueNotRule("age", EqualsRule(17)).evaluate({"age": 25})` → True |

### XML Rules

Handle XML content judgments:

| Rule Class | Description | Parameters | Example |
|------------|-------------|------------|--------|
| XmlTagExistsRule | Checks if XML contains tag | tag_name: str | `XmlTagExistsRule("user").evaluate("<user><name>John</name></user>")` → True |
| XmlAttributeMatchRule | Checks if XML tag attribute matches | tag_name: str, attr_name: str, attr_value: str | `XmlAttributeMatchRule("user", "id", "123").evaluate("<user id=\"123\">John</user>")` → True |

## 🔧 Advanced Usage

### Serialization and Deserialization

BuildRule supports rule serialization and deserialization for easy storage and transmission:

```python
# Create rule
rule = EqualsRule(10).and_(ContainsRule("success"))

# Serialize to string
serialized = rule.serialize()
# serialized = "AND(EQUAL(10),CONTAINS(\"success\",True))"

# Deserialize
restored_rule = RuleNode.from_serialized(serialized)

# Verify functional consistency
assert rule.evaluate(10) == restored_rule.evaluate(10)
```

The serialization string format is: `TYPE_NAME(param1,param2,...)`, with support for nested rules.

### Custom Rules

Creating custom rules simply requires inheriting from the RuleNode base class and implementing the evaluate method:

```python
from buildrule.rule_node import RuleNode

class EmailRule(RuleNode[str]):
    """Checks if string is a valid email address"""
    type_name = "EMAIL_VALID"
    
    def __init__(self):
        import re
        self.pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    
    def evaluate(self, condition: str) -> bool:
        return bool(self.pattern.match(condition))

# Use custom rule
email_rule = EmailRule()
print(email_rule.evaluate("user@example.com"))  # True
print(email_rule.evaluate("invalid-email"))  # False

# Supports serialization and deserialization
serialized = email_rule.serialize()  # "EMAIL_VALID()"
restored = RuleNode.from_serialized(serialized)
```

Custom rules are automatically registered in the system without additional configuration.

### Complex Rule Construction

For very complex rules, you can combine the rule builder with grouping logic:

```python
from buildrule.rule_node import RuleBuilder
from buildrule.rule import (
    EqualsRule, ContainsRule, GreaterThanRule,
    DateAfterRule, DictValueRule, ListAllElementsRule
)
from datetime import date

builder = RuleBuilder()

# Build complex business rule
complex_business_rule = (
    builder.group()  # Start condition group: user eligibility
    .condition(DictValueRule("age", GreaterThanRule(18)))  # Age > 18
    .and_()
    .condition(DictValueRule("is_verified", EqualsRule(True)))  # Verified
    .end_group()
    .and_()
    .group()  # Start condition group: order conditions
    .condition(DictValueRule("order_date", DateAfterRule(date(2023, 1, 1))))  # Orders after 2023
    .or_()
    .condition(DictValueRule("order_amount", GreaterThanRule(1000)))  # Or order amount > 1000
    .end_group()
    .build()
)

# Test rule
user_data = {
    "age": 25,
    "is_verified": True,
    "order_date": date(2023, 6, 15),
    "order_amount": 1200
}

result = complex_business_rule.evaluate(user_data)
print(result)  # True (satisfies both user eligibility and order conditions)
```

## 💡 Use Case Examples

### Data Validation

Using BuildRule for data input validation:

```python
from buildrule.rule_node import RuleBuilder
from buildrule.rule import (
    LengthRule, RegexMatchRule, RangeRule,
    DictValueRule, IsTrueRule
)

def validate_user_registration(user_data):
    """Validate user registration data"""
    builder = RuleBuilder()
    
    validation_rule = (
        builder.group()  # Username validation
        .condition(DictValueRule("username", LengthRule(3, 20)))
        .and_()
        .condition(DictValueRule("username", RegexMatchRule(r"^[a-zA-Z0-9_]+$")))
        .end_group()
        .and_()
        .condition(DictValueRule("email", RegexMatchRule(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")))  # Email validation
        .and_()
        .condition(DictValueRule("age", RangeRule(18, 120)))  # Age validation
        .and_()
        .condition(DictValueRule("agree_terms", IsTrueRule()))  # Must agree to terms
        .build()
    )
    
    return validation_rule.evaluate(user_data)

# Test
user1 = {
    "username": "john_doe",
    "email": "john@example.com",
    "age": 25,
    "agree_terms": True
}

user2 = {
    "username": "j",  # Username too short
    "email": "invalid-email",
    "age": 16,  # Age too young
    "agree_terms": False
}

print(validate_user_registration(user1))  # True
print(validate_user_registration(user2))  # False
```

### Business Rule Engine

Implementing a simple risk control rule engine:

```python
from buildrule.rule_node import RuleBuilder
from buildrule.rule import (
    GreaterThanRule, ContainsRule, DateAfterRule,
    DictValueRule, ListHasElementRule
)
from datetime import date, timedelta

def create_risk_control_rules():
    """Create risk control rules"""
    builder = RuleBuilder()
    
    # High risk rule: large amount OR multiple transactions in short time OR user in blacklist
    high_risk_rule = (
        builder.group()  # Amount risk
        .condition(DictValueRule("transaction_amount", GreaterThanRule(50000)))
        .end_group()
        .or_()
        .group()  # Frequency risk
        .condition(DictValueRule("transaction_count_24h", GreaterThanRule(20)))
        .end_group()
        .or_()
        .group()  # Blacklist risk
        .condition(ListHasElementRule("blacklisted_users", DictValueRule("user_id", ContainsRule(""))))  # Simplified example
        .end_group()
        .build()
    )
    
    # Medium risk rule: new user large transaction OR unusual location
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
    """Evaluate transaction risk"""
    risk_level = "low"
    
    if rules["high_risk"].evaluate(transaction_data):
        risk_level = "high"
    elif rules["medium_risk"].evaluate(transaction_data):
        risk_level = "medium"
    
    return risk_level

# Create rules
rules = create_risk_control_rules()

# Test transaction
large_transaction = {
    "transaction_amount": 100000,
    "transaction_count_24h": 5,
    "user_id": "user123",
    "account_age_days": 365
}

print(evaluate_risk(large_transaction, rules))  # "high"
```

### Configurable Workflow

Config-based workflow judgment:

```python
from buildrule.rule_node import RuleNode, RuleBuilder
from buildrule.rule import (
    EqualsRule, GreaterThanRule, ContainsRule,
    DateAfterRule, DictValueRule
)
from datetime import date

def load_workflow_rules(rule_configs):
    """Load workflow rules from configuration"""
    rules = {}
    
    for step_name, serialized_rule in rule_configs.items():
        rules[step_name] = RuleNode.from_serialized(serialized_rule)
    
    return rules

def execute_workflow(data, rules):
    """Execute workflow judgment"""
    results = {}
    
    for step_name, rule in rules.items():
        results[step_name] = rule.evaluate(data)
    
    return results

# Configurable workflow rules
workflow_config = {
    "step1_approval": "GREATER_THAN(10000)",  # Amount > 10000 needs approval
    "step2_manager_review": "AND(GREATER_THAN(50000),CONTAINS(\"contract\",True))",  # Large contracts need manager review
    "step3_finance_check": "OR(GREATER_THAN(100000),DATE_AFTER(2023-12-31))"  # Very large amounts or cross-year need finance check
}

# Load rules
rules = load_workflow_rules(workflow_config)

# Test data
project_data = {
    "amount": 75000,
    "has_contract": True,
    "submit_date": date(2023, 11, 15)
}

# Execute workflow
results = execute_workflow(project_data["amount"], rules)
print(results)
# Sample output: {
#     "step1_approval": True,
#     "step2_manager_review": True,
#     "step3_finance_check": False
# }
```

## ❓ Frequently Asked Questions

**Q: How to handle rules with different data types?**

A: When combining rules that handle different data types, you can use dictionary rules to access different fields:

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

# Input is a dictionary containing fields of different types
user_data = {"age": 18, "name": "John Doe"}
result = rule.evaluate(user_data)  # True
```

**Q: How is the rule execution performance?**

A: BuildRule is designed with performance in mind, especially for:
- Direct execution of simple rules is very efficient
- Logical combinations use short-circuit evaluation optimization (e.g., in AND combinations, if the first rule fails, subsequent rules are not executed)
- Serialization/deserialization mechanisms are optimized for common scenarios

For very complex rule expressions or high-frequency calling scenarios, consider:
- Caching common rule instances
- Precompiling regex rules
- Avoiding overly deep rule nesting

**Q: How to debug rules?**

A: Several methods for debugging rules:

1. Serialize rules to view structure: `print(rule.serialize())`
2. Execute step by step and print intermediate results
3. Add logging output when creating custom rules
4. Validate individual rule behavior with simple test data

**Q: Does it support asynchronous rule execution?**

A: The current version of BuildRule is primarily designed as a synchronous execution model. For scenarios requiring asynchronous execution, you can use it with asyncio at the application level:

```python
import asyncio
from buildrule.rule import EqualsRule

async def async_evaluate(rule, data):
    # Execute rule evaluation in a separate thread
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, rule.evaluate, data)

# Example usage
rule = EqualsRule(10)
async def main():
    result = await async_evaluate(rule, 10)
    print(result)

asyncio.run(main())
```

## 📝 Version History

- **0.0.1** - Initial release
  - Core rule node system
  - Basic logical combinations (AND/OR/NOT)
  - Rule builder
  - Serialization/deserialization support
  - Multiple built-in rule types
  - Comprehensive unit tests