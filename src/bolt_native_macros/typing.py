from dataclasses import dataclass

from beet.core.utils import required_field
from nbtlib import Base


class MacroRepresentation: ...


class QuotedStringWithMacro(str, MacroRepresentation): ...


class StringWithMacro(str, MacroRepresentation): ...

class DictWithMacro(dict, MacroRepresentation): ...

class ListWithMacro(list, MacroRepresentation): ...

@dataclass
class MacroTag(Base, MacroRepresentation):
    name: str = required_field()
    parser: str | None = required_field()

    def __post_init__(self):
        self.serializer = "macro"

    def __str__(self):
        return f"$({self.name})"
    
    def __hash__(self) -> int:
        return hash(hash(self.name) + hash(self.parser))