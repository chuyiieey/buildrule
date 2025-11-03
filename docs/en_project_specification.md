# BuildRule Project Specification Document

## 1. Project Overview

BuildRule is a general-purpose rule engine library that provides flexible rule definition, composition, and execution capabilities. The library supports custom rule nodes, complex logical compositions (AND/OR/NOT), automatic serialization/deserialization, and can be used for various scenarios such as numeric judgment, string matching, XML validation, dictionary object verification, etc., with high extensibility.

Key features:
- Type-safe rule definitions based on generics
- Support for complex logic composition and grouping priorities
- Rich built-in rule types
- Automatic serialization and deserialization mechanisms
- Clean and intuitive chain API design
- Easily extensible custom rule system

## 2. Technical Architecture

### 2.1 Core Architecture

BuildRule adopts an object-oriented design pattern, with RuleNode as the core base class, implementing various rule types through inheritance. The overall architecture is as follows:

- **RuleNode**: Base class for all rules, providing the basic framework and serialization/deserialization functionality
- **Logical combination nodes**: AndNode, OrNode, NotNode for implementing rule composition
- **RuleBuilder**: For building complex rule expressions through method chaining
- **Specialized rule implementations**: Various specific rule implementations categorized by data type

### 2.2 Module Structure

```
buildrule/
├── __init__.py       # Package export definitions
├── rule_node.py      # Core node classes and builder
└── rule/             # Rule implementations directory
    ├── __init__.py   # Rule export definitions
    ├── numeric_rules/     # Numeric-related rules
    ├── string_rules/      # String-related rules
    ├── datetime_rules/    # DateTime-related rules
    ├── set_rules/         # Set-related rules
    ├── list_rules/        # List-related rules
    ├── boolean_rules/     # Boolean-related rules
    ├── regex_rules/       # Regular expression rules
    ├── dict_ext_rules/    # Dictionary extension rules
    └── xml_rules/         # XML-related rules
```

### 2.3 Design Patterns

1. **Strategy Pattern**: Different rules implement the same evaluate interface but with different judgment logic
2. **Composite Pattern**: Combining simple rules into complex rules through AndNode, OrNode, NotNode
3. **Builder Pattern**: RuleBuilder provides a fluent API for building complex rule expressions
4. **Registry Pattern**: Automatic registration and discovery of rule types through _type_registry
5. **Factory Pattern**: Dynamic creation of rule instances through from_serialized method

## 3. Core Features

### 3.1 Rule Node System

RuleNode is the core abstraction of the entire library, with all concrete rules inheriting from this base class. It provides:

- Automatic subclass registration mechanism
- Serialization and deserialization functionality
- Logical composition methods (and_, or_, not_)

```python
# Core rule node interface
class RuleNode(Generic[ConditionType]):
    def evaluate(self, condition: ConditionType) -> bool: ...
    def serialize(self) -> str: ...
    @classmethod
    def from_serialized(cls, data: str) -> "RuleNode": ...
```

### 3.2 Logical Composition

Supports combining multiple rules through AND, OR, NOT operators to form complex logical expressions:

```python
# Logical combination example
rule = equals_rule.and_(contains_rule.not_())
# Equivalent to: (condition == target) AND (not condition.contains(substr))
```

### 3.3 Rule Builder

RuleBuilder provides a chained API for building complex rule expressions with support for grouped logic:

```python
# Building complex rule: (A AND B) OR C
rule = builder.group()
    .condition(A)
    .and_()
    .condition(B)
    .end_group()
    .or_()
    .condition(C)
    .build()
```

### 3.4 Built-in Rule Types

The library provides a rich set of built-in rule types covering common judgment scenarios for various data types:

- **Numeric rules**: Equals, greater than, less than, range checking, etc.
- **String rules**: Contains, starts with, ends with, exact match, etc.
- **DateTime rules**: Date comparison, range checking, etc.
- **Set rules**: Element containment, size checking, etc.
- **List rules**: Element existence, all elements check, etc.
- **Boolean rules**: True/False checking
- **Regex rules**: Regular expression matching
- **Dictionary rules**: Key existence, value checking, etc.
- **XML rules**: Tag existence, attribute matching, etc.

### 3.5 Serialization and Deserialization

Supports automatic serialization and deserialization of rule expressions for easy storage and transmission:

```python
# Serialization
serialized = rule.serialize()  # e.g.: "AND(EQUAL(5),NOT(CONTAINS(\"error\",True)))"

# Deserialization
rule = RuleNode.from_serialized(serialized)
```

## 4. Key API

### 4.1 RuleNode Base Class

- **evaluate(condition)**: Executes rule evaluation and returns boolean result
- **serialize()**: Serializes the rule to a string
- **from_serialized(data)**: Deserializes rule from a string
- **and_(other)**: Performs AND combination with another rule
- **or_(other)**: Performs OR combination with another rule
- **not_()**: Inverts the rule result

### 4.2 RuleBuilder Class

- **condition(node)**: Adds a basic rule node
- **and_()**: Declares subsequent rules use AND logic
- **or_()**: Declares subsequent rules use OR logic
- **group()**: Starts a rule group
- **end_group()**: Ends a rule group
- **build()**: Completes building and returns the root rule node

### 4.3 Common Rule Classes

- **EqualsRule(target)**: Checks if equals to target value
- **RangeRule(min_val, max_val)**: Checks if in range
- **ContainsRule(substr, case_sensitive=True)**: Checks if contains substring
- **RegexMatchRule(pattern)**: Checks if matches regular expression
- **DictKeyExistsRule(key)**: Checks if dictionary contains specified key

## 5. Technology Stack and Dependencies

- **Python version**: >= 3.8
- **Main dependencies**: No external runtime dependencies
- **Development dependencies**:
  - pytest: Unit testing framework
  - mypy: Type checking
  - black: Code formatting
  - sphinx: Documentation generation

## 6. Use Cases

### 6.1 Business Rule Engine

Suitable for scenarios requiring flexible configuration of business rules, such as risk control systems, approval processes, pricing strategies, etc.

### 6.2 Data Validation

Can be used for data input validation, configuration file verification, API parameter validation, etc.

### 6.3 Dynamic Condition Execution

Supports dynamically determining execution paths based on runtime conditions, suitable for workflow systems, automation scripts, etc.

### 6.4 Configurable Logic

Allows defining business logic through configuration files, enabling rule adjustment without code modification.

## 7. Extension Guide

To create a custom rule, simply inherit from the RuleNode base class and implement the evaluate method:

```python
class MyCustomRule(RuleNode[MyType]):
    type_name = "CUSTOM_RULE"  # Optional, custom type name
    
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
    
    def evaluate(self, condition: MyType) -> bool:
        # Implement custom judgment logic
        return condition.some_property == self.param1
```

Custom rules are automatically registered in the system and can be used through deserialization with the from_serialized method.

## 8. Summary

BuildRule provides a flexible, extensible rule engine framework with a clean API and rich built-in rules, enabling developers to easily implement complex business rule logic. Its design focuses on type safety, usability, and extensibility, making it suitable for various application scenarios requiring rule judgment and logical composition.