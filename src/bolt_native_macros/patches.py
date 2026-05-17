from contextlib import suppress
from typing import Any

from mecha import AstNbt, AstNbtValue, AstNode, AstNumber
from nbtlib import Serializer as NbtSerializer


from .ast import AstMacroNbtArgument, AstMacroNumber
from .serialize import serialize_macro
from .typing import MacroTag


def nbt():
    old_from_value = AstNbt.from_value

    @classmethod
    def from_value(cls: type[AstNbt], value: Any) -> AstNbt:
        if isinstance(value, MacroTag):
            return AstMacroNbtArgument.from_value(value)  # type: ignore
        return old_from_value(value)

    AstNbt.from_value = from_value  # type: ignore


def apply_patches():
    NbtSerializer.serialize_macro = serialize_macro  # type: ignore

    nbt()

    with suppress(ImportError):
        import bolt_expressions.typing

        convert_tag = bolt_expressions.typing.convert_tag

        def convert_tag_with_macro(value: Any):
            match value:
                case MacroTag():
                    return value
                case _:
                    return convert_tag(value)

        bolt_expressions.typing.convert_tag = convert_tag_with_macro
