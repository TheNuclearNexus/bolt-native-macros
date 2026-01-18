data modify storage foo:bar baz set value f"{$(macro)}"
data modify storage foo:bar baz set value {x: $(macro)}
data modify storage foo:bar baz set value {$(key): $(macro)}
data modify storage foo:bar baz.foo.$(macro).taco set value {x: $(macro)}
data modify storage foo:bar baz[{bar: $(bar)}] set value {x: $(macro)}
data modify storage foo:bar foo.baz[{bar: $(bar)}] set value {x: $(macro)}
data modify storage foo:bar baz[{$(bar): $(foo)}] set value {x: $(macro)}
data modify storage foo:bar foo.baz[{$(bar: string): $(foo: string)}] set value {x: $(macro)}
data modify storage foo:bar baz[$(bar)] set value {x: $(macro)}
say f"{$(macro)}"
