# RuleEngine: 通用规则引擎库
# General Rule Engine Library

"""
通用规则引擎，支持自定义规则节点、复杂逻辑组合（AND/OR/NOT）、自动序列化/反序列化，
可用于数值判断、字符串匹配、XML验证、字典对象校验等场景，具备高扩展性。

A general-purpose rule engine that supports custom rule nodes, complex logic combinations (AND/OR/NOT),
automatic serialization/deserialization. It can be used for numeric judgment, string matching, XML validation,
dictionary object verification and other scenarios with high extensibility.
"""

import inspect
from enum import Enum
from typing import Generic, Optional, TypeVar, Dict, ClassVar, Any, List, Tuple, Type


# 自定义异常定义
# Custom Exception Definition
class InvalidXMLError(Exception):
    """
    当传入的XML字符串不符合语法规范时抛出的异常。
    Exception raised when the input XML string does not conform to syntax specifications.
    """

    pass


# 类型变量定义（泛型支持）
# Type Variable Definition (Generic Support)
ConditionType = TypeVar("ConditionType")  # 规则判断的输入数据类型
RuleNodeType = TypeVar("RuleNodeType", bound="RuleNode")  # 规则节点类型变量
# Input data type for rule evaluation


class RuleType(Enum):
    """
    基础规则类型枚举，标识节点的存在性判断类型。
    Basic rule type enumeration, identifying the existence judgment type of nodes.
    """

    exist = "Exist"  # 存在性判断：目标存在
    # Existence check: target exists
    not_exist = "NotExist"  # 存在性判断：目标不存在
    # Existence check: target does not exist


class RuleNode(Generic[ConditionType]):
    """
    规则节点基类，所有自定义规则需继承此类。
    自动实现子类注册、type_name生成、序列化/反序列化功能。

    Base class for rule nodes, all custom rules must inherit from this class.
    Automatically implements subclass registration, type_name generation, and serialization/deserialization.

    Attributes:
        _type_registry (ClassVar[Dict[str, type]]): 子类注册表，存储类型名与类的映射
                                                Subclass registry, storing mappings of type names to classes
        type_name (ClassVar[str]): 规则类型名（自动生成，子类无需手动声明）
                                   Rule type name (automatically generated, no manual declaration required for subclasses)
    """

    _type_registry: ClassVar[Dict[str, Type['RuleNode']]] = {}
    type_name: ClassVar[str]  # 子类可显式声明此属性

    def __init_subclass__(cls, **kwargs):
        """
        子类初始化钩子：优先使用子类显式声明的type_name，无则自动生成。
        生成规则：将子类类名转为全大写（如EqualsRule → EQUALS RULE）。

        Subclass initialization hook: uses explicitly declared type_name first,
        generates automatically if not present.
        """
        super().__init_subclass__(**kwargs)
        # 核心修改：优先使用子类显式声明的type_name
        if hasattr(cls, "type_name") and isinstance(cls.type_name, str):
            # 若子类显式声明了type_name，直接使用（建议全大写，保持一致性）
            cls.type_name = cls.type_name.strip().upper()
        else:
            # 无显式声明时，按默认规则生成
            cls.type_name = cls.__name__.upper()
        # 注册子类到注册表（无论type_name是显式还是自动生成）
        RuleNode._type_registry[cls.type_name] = cls

    def evaluate(self, condition: ConditionType) -> bool:
        """
        抽象方法：执行规则判断，子类必须实现此方法。

        Abstract method: executes rule evaluation, subclasses must implement this method.

        Args:
            condition (ConditionType): 规则判断的输入数据（类型由泛型指定）
                                      Input data for rule evaluation (type specified by generic)

        Returns:
            bool: 规则判断结果（True=满足规则，False=不满足规则）
                  Rule evaluation result (True=meets the rule, False=does not meet the rule)

        Raises:
            NotImplementedError: 若子类未实现此方法则抛出
                                 Raised if the subclass does not implement this method
        """
        raise NotImplementedError(
            f"Subclass {self.__class__.__name__} must implement evaluate() method"
        )

    def and_(self, other: "RuleNode") -> "AndNode":
        """
        逻辑AND组合：将当前规则与另一规则组合为"同时满足"的逻辑。

        Logical AND combination: combines the current rule with another rule into "both satisfy" logic.

        Args:
            other (RuleNode): 待组合的另一规则节点
                             Another rule node to be combined

        Returns:
            AndNode: 组合后的AND逻辑节点
                     Combined AND logic node
        """
        return AndNode(self, other)

    def or_(self, other: "RuleNode") -> "OrNode":
        """
        逻辑OR组合：将当前规则与另一规则组合为"满足其一"的逻辑。

        Logical OR combination: combines the current rule with another rule into "either satisfies" logic.

        Args:
            other (RuleNode): 待组合的另一规则节点
                             Another rule node to be combined

        Returns:
            OrNode: 组合后的OR逻辑节点
                    Combined OR logic node
        """
        return OrNode(self, other)

    def not_(self) -> "NotNode":
        """
        逻辑NOT反转：对当前规则结果取反。

        Logical NOT inversion: inverts the result of the current rule.

        Returns:
            NotNode: 反转后的NOT逻辑节点
                     Inverted NOT logic node
        """
        return NotNode(self)

    def serialize(self) -> str:
        """
        自动序列化：将规则节点转换为字符串格式，支持嵌套规则。

        Automatic serialization: converts the rule node to a string format, supporting nested rules.

        Returns:
            str: 序列化后的字符串（格式：TYPE_NAME(param1,param2,...)）
                 Serialized string (format: TYPE_NAME(param1,param2,...))

        Raises:
            AttributeError: 若实例缺少构造函数参数对应的属性则抛出
                           Raised if the instance lacks attributes corresponding to constructor parameters
        """
        # 获取子类构造函数参数（排除self）
        sig = inspect.signature(type(self).__init__)
        params = [p for p in sig.parameters.values() if p.name != "self"]

        # 收集参数值（从实例属性中提取）
        args = []
        for param in params:
            if not hasattr(self, param.name):
                raise AttributeError(
                    f"Instance lacks attribute '{param.name}' for constructor parameter"
                )
            args.append(getattr(self, param.name))

        # 序列化每个参数（支持嵌套RuleNode）
        args_str = ",".join(self._serialize_arg(arg) for arg in args)
        return f"{self.type_name}({args_str})"

    @classmethod
    def deserialize(cls, data: str) -> "RuleNode":
        """
        类方法：将序列化字符串解析为当前类型的规则节点实例。

        Class method: parses a serialized string into a rule node instance of the current type.

        Args:
            data (str): 序列化字符串（格式：TYPE_NAME(param1,param2,...)）
                        Serialized string (format: TYPE_NAME(param1,param2,...))

        Returns:
            RuleNode: 解析后的规则节点实例
                      Parsed rule node instance
        """
        # 提取括号内的参数部分
        content = data[len(cls.type_name) + 1 : -1]
        # 无参数情况（如空规则）
        if not content:
            return cls()

        # 解析参数列表（支持嵌套规则）
        args = [
            cls._deserialize_arg(arg_str.strip())
            for arg_str in cls._split_args(content)
        ]
        # 直接创建实例而不是访问__init__
        return cls(*args)

    @classmethod
    def from_serialized(cls, data: str) -> "RuleNode":
        """
        通用反序列化入口：自动识别规则类型并解析为对应实例。

        General deserialization entry: automatically identifies the rule type and parses it into the corresponding instance.

        Args:
            data (str): 序列化字符串（格式：TYPE_NAME(param1,param2,...)）
                        Serialized string (format: TYPE_NAME(param1,param2,...))

        Returns:
            RuleNode: 解析后的规则节点实例
                      Parsed rule node instance

        Raises:
            ValueError: 若序列化格式无效或规则类型未知则抛出
                        Raised if the serialization format is invalid or the rule type is unknown
        """
        if "(" not in data:
            raise ValueError(f"Invalid serialized format: {data} (missing '(')")

        # 提取类型名（第一个'('之前的部分）
        type_name = data.split("(", 1)[0]
        if type_name not in cls._type_registry:
            raise ValueError(f"Unknown rule type: {type_name} (not in registry)")

        # 调用对应类型的反序列化方法
        rule_class = cls._type_registry[type_name]
        return rule_class.deserialize(data)


    @staticmethod
    def _serialize_arg(arg: Any) -> str:
        """
        辅助方法：序列化单个参数（内部使用）。

        Helper method: serializes a single parameter (used internally).

        Args:
            arg (Any): 待序列化的参数（支持RuleNode、str、数字等类型）
                       Parameter to be serialized (supports RuleNode, str, number, etc.)

        Returns:
            str: 序列化后的参数字符串
                 Serialized parameter string
        """
        # 嵌套RuleNode：递归序列化
        if isinstance(arg, RuleNode):
            return arg.serialize()
        # 字符串：添加引号并转义内部引号
        if isinstance(arg, str):
            escaped_arg = arg.replace('"', '\\"')
            return '"' + escaped_arg + '"'
        # 其他类型（数字、布尔等）：直接转字符串
        return str(arg)

    @staticmethod
    def _deserialize_arg(arg_str: str) -> Any:
        """
        辅助方法：反序列化单个参数（内部使用）

        Args:
            arg_str (str): 待反序列化的参数字符串
                          Parameter string to be deserialized

        Returns:
            Any: 反序列化后的参数值
                Deserialized parameter value
        """
        if not arg_str:
            return None
        # 处理字符串（带引号）：去除引号并恢复转义
        if arg_str.startswith('"') and arg_str.endswith('"'):
            return arg_str[1:-1].replace('\\"', '"')
        # 处理嵌套RuleNode（带括号）：递归反序列化
        if "(" in arg_str and arg_str.endswith(")"):
            return RuleNode.from_serialized(arg_str)
        # 新增：处理布尔值（True/False）
        if arg_str.lower() == "true":
            return True
        if arg_str.lower() == "false":
            return False
        # 处理整数
        if arg_str.isdigit():
            return int(arg_str)
        # 处理浮点数
        try:
            return float(arg_str)
        except ValueError:
            # 其他类型：直接返回字符串
            return arg_str

    @staticmethod
    def _split_args(content: str) -> List[str]:
        """
        辅助方法：分割参数列表（支持嵌套括号场景）。

        Helper method: splits parameter list (supports nested parentheses).

        Args:
            content (str): 括号内的参数总字符串
                           Total parameter string inside parentheses

        Returns:
            List[str]: 分割后的单个参数字符串列表
                       List of split individual parameter strings
        """
        args: List[str] = []
        current: List[str] = []
        balance: int = 0  # 括号平衡计数器：处理嵌套括号
        # Parentheses balance counter: handle nested parentheses
        for c in content:
            # 逗号且括号平衡时：分割参数
            if c == "," and balance == 0:
                args.append("".join(current).strip())
                current = []
            else:
                current.append(c)
                # 更新括号平衡计数
                if c == "(":
                    balance += 1
                elif c == ")":
                    balance -= 1
        # 添加最后一个参数
        if current:
            args.append("".join(current).strip())
        return args


# 逻辑组合节点：AND/OR/NOT（无需手动声明type_name）
# Logical Combination Nodes: AND/OR/NOT (no manual type_name declaration required)
class AndNode(RuleNode[ConditionType]):
    """
    逻辑AND节点：同时满足左右两个子规则时返回True。

    Logical AND node: returns True only if both left and right sub-rules are satisfied.

    Args:
        left (RuleNode[ConditionType]): 左侧子规则
                                        Left sub-rule
        right (RuleNode[ConditionType]): 右侧子规则
                                         Right sub-rule
    """

    type_name = "AND"

    def __init__(self, left: RuleNode[ConditionType], right: RuleNode[ConditionType]):
        self.left = left
        self.right = right

    def evaluate(self, condition: ConditionType) -> bool:
        """
        执行AND逻辑判断：左右子规则均满足则返回True

        Args:
            condition (ConditionType): 规则判断的输入数据
                                      Input data for rule evaluation

        Returns:
            bool: 规则判断结果
                  Rule evaluation result
        """
        return self.left.evaluate(condition) and self.right.evaluate(condition)


class OrNode(RuleNode[ConditionType]):
    """
    逻辑OR节点：满足任意一个子规则时返回True。

    Logical OR node: returns True if either of the two sub-rules is satisfied.

    Args:
        left (RuleNode[ConditionType]): 左侧子规则
                                        Left sub-rule
        right (RuleNode[ConditionType]): 右侧子规则
                                         Right sub-rule
    """

    type_name = "OR"

    def __init__(self, left: RuleNode[ConditionType], right: RuleNode[ConditionType]):
        self.left = left
        self.right = right

    def evaluate(self, condition: ConditionType) -> bool:
        """
        执行OR逻辑判断：任意子规则满足则返回True

        Args:
            condition (ConditionType): 规则判断的输入数据
                                      Input data for rule evaluation

        Returns:
            bool: 规则判断结果
                  Rule evaluation result
        """
        return self.left.evaluate(condition) or self.right.evaluate(condition)


class NotNode(RuleNode[ConditionType]):
    """
    逻辑NOT节点：对单个子规则结果取反。

    Logical NOT node: inverts the result of a single sub-rule.

    Args:
        node (RuleNode[ConditionType]): 待取反的子规则
                                        Sub-rule to be inverted
    """

    type_name = "NOT"

    def __init__(self, node: RuleNode[ConditionType]):
        self.node = node

    def evaluate(self, condition: ConditionType) -> bool:
        """
        执行NOT逻辑判断：返回子规则结果的反值

        Args:
            condition (ConditionType): 规则判断的输入数据
                                      Input data for rule evaluation

        Returns:
            bool: 规则判断结果
                  Rule evaluation result
        """
        return not self.node.evaluate(condition)


class RuleBuilder(Generic[ConditionType]):
    """
    规则构建器：通过链式调用简化复杂规则的组合（支持分组逻辑）。

    Rule Builder: simplifies the combination of complex rules through method chaining (supports grouped logic).

    Attributes:
        stack (List[Tuple[Optional[RuleNode], Optional[RuleNode], Optional[str]]]):
            规则构建栈，存储当前层级的规则状态：(当前规则, 待组合规则, 逻辑运算符)
            Rule building stack, storing the current level's rule state: (current_rule, pending_rule, logic_operator)
    """

    def __init__(self):
        # 栈初始化：初始状态为(无当前规则, 无待组合规则, 无逻辑运算符)
        self.stack: List[Tuple[Optional[RuleNode[ConditionType]], Optional[RuleNode[ConditionType]], Optional[str]]] = [(None, None, None)]

    @property
    def current_level(self) -> Tuple[Optional[RuleNode[ConditionType]], Optional[RuleNode[ConditionType]], Optional[str]]:
        """
        获取当前栈顶的规则状态（当前层级）

        Returns:
            Tuple[Optional[RuleNode[ConditionType]], Optional[RuleNode[ConditionType]], Optional[str]]: 
                当前规则、待组合规则、逻辑运算符
        """
        return self.stack[-1]

    @current_level.setter
    def current_level(self, value: Tuple[Optional[RuleNode[ConditionType]], Optional[RuleNode[ConditionType]], Optional[str]]) -> None:
        """
        更新当前栈顶的规则状态（当前层级）

        Args:
            value (Tuple[Optional[RuleNode[ConditionType]], Optional[RuleNode[ConditionType]], Optional[str]]):
                新的规则状态值
        """
        self.stack[-1] = value

    def condition(self, condition_node: RuleNode[ConditionType]) -> "RuleBuilder[ConditionType]":
        """
        添加基础规则节点（核心方法）。

        Args:
            condition_node (RuleNode[ConditionType]): 待添加的规则节点
                                                     Rule node to be added

        Returns:
            RuleBuilder[ConditionType]: 构建器自身（支持链式调用）
                                        Builder itself (supports method chaining)
        """
        self._handle_new_node(condition_node)
        return self

    def and_(self) -> "RuleBuilder[ConditionType]":
        """
        声明后续规则使用AND逻辑组合。

        Declares that subsequent rules will be combined with AND logic.

        Returns:
            RuleBuilder[ConditionType]: 构建器自身（支持链式调用）
                                        Builder itself (supports method chaining)

        Raises:
            ValueError: 若调用前未添加基础规则则抛出
                        Raised if no basic rule is added before calling
        """
        current_node, _, _ = self.current_level
        if current_node is None:
            raise ValueError("Call condition() first before and_()")
        # 记录待组合规则和逻辑运算符
        self.current_level = (current_node, current_node, "and")
        return self

    def or_(self) -> "RuleBuilder[ConditionType]":
        """
        声明后续规则使用OR逻辑组合。

        Declares that subsequent rules will be combined with OR logic.

        Returns:
            RuleBuilder[ConditionType]: 构建器自身（支持链式调用）
                                        Builder itself (supports method chaining)

        Raises:
            ValueError: 若调用前未添加基础规则则抛出
                        Raised if no basic rule is added before calling
        """
        current_node, _, _ = self.current_level
        if current_node is None:
            raise ValueError("Call condition() first before or_()")
        # 记录待组合规则和逻辑运算符
        self.current_level = (current_node, current_node, "or")
        return self

    def group(self) -> "RuleBuilder[ConditionType]":
        """
        开启规则分组（用于处理优先级逻辑，如 (A AND B) OR C）。

        Starts a rule group (for handling priority logic, e.g., (A AND B) OR C).

        Returns:
            RuleBuilder[ConditionType]: 构建器自身（支持链式调用）
                                        Builder itself (supports method chaining)
        """
        # 压入新的空状态到栈顶，代表新分组
        self.stack.append((None, None, None))
        return self

    def end_group(self) -> "RuleBuilder[ConditionType]":
        """
        结束当前规则分组，并将分组结果作为单个规则节点回退到上一层。

        Ends the current rule group and pushes the group result back to the previous level as a single rule node.

        Returns:
            RuleBuilder[ConditionType]: 构建器自身（支持链式调用）
                                        Builder itself (supports method chaining)

        Raises:
            ValueError: 若未开启分组或分组内无规则则抛出
                        Raised if no group is started or no rules are in the group
        """
        if len(self.stack) <= 1:
            raise ValueError("Call group() first before end_group()")
        # 弹出当前分组状态，获取分组内构建的规则
        group_node = self.stack.pop()[0]
        if group_node is None:
            raise ValueError("No rules added in the current group (empty group)")
        # 将分组结果作为新节点添加到上一层
        self._handle_new_node(group_node)
        return self

    def _handle_new_node(self, new_node: RuleNode[ConditionType]) -> None:
        """
        内部方法：处理新添加的规则节点，根据当前逻辑运算符完成组合。

        Internal method: processes newly added rule nodes and completes combination based on current logic operator.

        Args:
            new_node (RuleNode[ConditionType]): 新添加的规则节点
                                               Newly added rule node
        """
        current_node, pending_node, pending_logic = self.current_level
        # 无待组合规则/运算符：直接将新节点设为当前规则
        if pending_node is None or pending_logic is None:
            self.current_level = (new_node, None, None)
        # 有待组合规则/运算符：按逻辑组合并更新当前规则
        else:
            combined_node = (
                pending_node.and_(new_node)
                if pending_logic == "and"
                else pending_node.or_(new_node)
            )
            self.current_level = (combined_node, None, None)

    def build(self) -> RuleNode[ConditionType]:
        """
        完成规则构建，返回最终的根规则节点。

        Completes rule building and returns the final root rule node.

        Returns:
            RuleNode[ConditionType]: 构建完成的根规则节点
                                    Final root rule node after building

        Raises:
            ValueError: 若存在未闭合分组或未添加任何规则则抛出
                        Raised if there are unclosed groups or no rules added
        """
        if len(self.stack) != 1:
            raise ValueError(
                f"Unclosed groups detected: need {len(self.stack)-1} more end_group() calls"
            )
        root_node = self.current_level[0]
        if root_node is None:
            raise ValueError("No rules added (empty rule set)")
        return root_node
