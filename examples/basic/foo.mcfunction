from bolt_native_macros.typing import MacroTag

# Non-variable interpolation
data modify storage foo:bar baz set value f"{$(macro)}"
data modify storage foo:bar baz set value [$(macro)]
data modify storage foo:bar baz set value {x: f"{$(macro)}"}
data modify storage foo:bar baz set value {x: $(macro)}
data modify storage foo:bar baz set value {x: $(macro: string)}
data modify storage foo:bar baz set value {$(key): $(macro)}
data modify storage foo:bar baz.foo.$(macro).taco set value {x: $(macro)}
data modify storage foo:bar baz[{bar: $(bar)}] set value {x: $(macro)}
data modify storage foo:bar foo.baz[{bar: $(bar)}] set value {x: $(macro)}
data modify storage foo:bar baz[{$(bar): $(foo)}] set value {x: $(macro)}
data modify storage foo:bar foo.baz[{$(bar: string): $(foo: string)}] set value {x: $(macro)}
data modify storage foo:bar baz[$(bar)] set value {x: $(macro)}
data modify storage foo:bar baz set from storage foo:bar baz[$(bar)]
say f"{$(macro)}"

# Variable interpolation
macro = $(macro)
macro_quoted = MacroTag("macro_quoted", "string")
data modify storage foo:bar baz set value {x: f"{macro}"}
data modify storage foo:bar baz set value ({macro.name: f"{macro}"})
data modify storage foo:bar baz set value [macro]
data modify storage foo:bar baz set value {x: macro}
data modify storage foo:bar baz set value {x: macro_quoted}
data modify storage foo:bar baz set value ({macro_quoted: macro})
data modify storage foo:bar baz[{bar: macro}] set value {x: macro}
data modify storage foo:bar foo.baz[{bar: macro}] set value {x: macro}
say f"{$(macro)}"