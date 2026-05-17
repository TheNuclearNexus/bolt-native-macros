from dataclasses import dataclass
from typing import Any, Generator, List, Optional

from bolt import (
    Accumulator,
    AstDict,
    AstFormatString,
    AstList,
    visit_generic,
    visit_single,
)
from mecha import AstNode, Visitor, rule

from .ast import AstMacroArgument, AstMacroExpression, AstMacroStringWrapper
from .typing import (
    DictWithMacro,
    ListWithMacro,
    MacroRepresentation,
    MacroTag,
    QuotedStringWithMacro,
)


def ast_to_macro(macro: AstMacroArgument):
    return MacroTag(macro.name, macro.parser)


def make_macro_string():
    """
    Returns the type `StringWithMacro`, this is to add the type to the scope w/o making it globally accessible.

    Kind of hacky but works well
    """
    return QuotedStringWithMacro


def make_macro_format_string():
    def _do(template: str, values: list[Any]):
        if any(map(lambda v: isinstance(v, MacroTag), values)):
            return QuotedStringWithMacro(template.format(*values))
        else:
            return template.format(*values)

    return _do


def has_macro_repr(root: Any) -> bool:
    match root:
        case MacroRepresentation():
            return True
        case dict():
            for k, v in root.items():
                if isinstance(k, MacroRepresentation) or has_macro_repr(v):
                    return True
        case list():
            for v in root:
                if has_macro_repr(v):
                    return True

    return False


def make_macro_dict():
    def _do(dict: dict):
        if has_macro_repr(dict):
            return DictWithMacro(dict)
        else:
            return dict

    return _do


def make_macro_list():
    def _do(list):
        if has_macro_repr(list):
            return ListWithMacro(list)
        else:
            return list

    return _do


HELPERS = [
    ast_to_macro,
    make_macro_string,
    make_macro_format_string,
    make_macro_list,
    make_macro_dict,
]


@dataclass
class MacroCodegen(Visitor):
    @rule(AstList)
    def list(
        self,
        node: AstList,
        acc: Accumulator,
    ) -> Generator[AstNode, Optional[List[str]], Optional[List[str]]]:
        items: List[str] = []

        for item in node.items:
            value = yield from visit_single(item, required=True)
            items.append(value)

        result = acc.make_variable()
        resolved = acc.helper(make_macro_list.__name__)
        acc.statement(f"{result} = {resolved}([{', '.join(items)}])", lineno=node)
        return [result]

    @rule(AstDict)
    def dict(
        self,
        node: AstDict,
        acc: Accumulator,
    ) -> Generator[AstNode, Optional[List[str]], Optional[List[str]]]:
        items: List[str] = []

        for item in node.items:
            value = yield from visit_single(item, required=True)
            items.append(value)

        result = acc.make_variable()
        resolved = acc.helper(make_macro_dict.__name__)
        acc.statement(f"{result} = {resolved}({{{', '.join(items)}}})", lineno=node)
        return [result]

    @rule(AstFormatString)
    def format_string(
        self,
        node: AstFormatString,
        acc: Accumulator,
    ) -> Generator[AstNode, Optional[List[str]], Optional[List[str]]]:
        values: List[str] = []

        for value in node.values:
            result = yield from visit_single(value, required=True)
            values.append(result)

        result = acc.make_variable()
        resolved = acc.helper(
            make_macro_format_string.__name__,
        )
        acc.statement(
            f"{result} = {resolved}({node.fmt!r}, [{', '.join(values)}])", lineno=node
        )
        return [result]

    @rule(AstMacroExpression)
    def macro(
        self, node: AstMacroExpression, acc: Accumulator
    ) -> Generator[AstNode, Optional[List[str]], Optional[List[str]]]:
        # This allows for macros to be used as literals
        result = yield from visit_generic(node, acc)

        if result is None:
            result = acc.make_ref(node)

        result = acc.helper(ast_to_macro.__name__, result)

        return [result]

    @rule(AstMacroStringWrapper)
    def wrapper(
        self, node: AstMacroStringWrapper, acc: Accumulator
    ) -> Generator[AstNode, Optional[List[str]], Optional[List[str]]]:
        # Codegen the underlying child and get its result
        child = yield from visit_single(node.child, required=True)

        # Create a variable and assign it to a new instance of StringWithMacro
        result = acc.make_variable()
        # make_macro_string returns the **type** StringWithMacro, you must manually create the instance afterwards
        acc.statement(f"{result} = {acc.helper(make_macro_string.__name__)}({child})")

        return [result]
