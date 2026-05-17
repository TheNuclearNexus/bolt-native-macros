$data modify storage foo:bar baz set value "$(macro)"
$data modify storage foo:bar baz set value [$(macro)]
$data modify storage foo:bar baz set value {x: "$(macro)"}
$data modify storage foo:bar baz set value {x: $(macro)}
$data modify storage foo:bar baz set value {x: "$(macro)"}
$data modify storage foo:bar baz set value {$(key): $(macro)}
$data modify storage foo:bar baz.foo."$(macro)".taco set value {x: $(macro)}
$data modify storage foo:bar baz[{bar: $(bar)}] set value {x: $(macro)}
$data modify storage foo:bar foo.baz[{bar: $(bar)}] set value {x: $(macro)}
$data modify storage foo:bar baz[{$(bar): $(foo)}] set value {x: $(macro)}
$data modify storage foo:bar foo.baz[{"$(bar)": "$(foo)"}] set value {x: $(macro)}
$data modify storage foo:bar baz[$(bar)] set value {x: $(macro)}
$data modify storage foo:bar baz set from storage foo:bar baz[$(bar)]
$say $(macro)
$data modify storage foo:bar baz set value {x: "$(macro)"}
$data modify storage foo:bar baz set value {macro: "$(macro)"}
$data modify storage foo:bar baz set value [$(macro)]
$data modify storage foo:bar baz set value {x: $(macro)}
$data modify storage foo:bar baz set value {x: "$(macro_quoted)"}
$data modify storage foo:bar baz set value {"$(macro_quoted)": $(macro)}
$data modify storage foo:bar baz[{bar: $(macro)}] set value {x: $(macro)}
$data modify storage foo:bar foo.baz[{bar: $(macro)}] set value {x: $(macro)}
$say $(macro)
