$data modify storage foo:bar baz set value "$(macro)"
$data modify storage foo:bar baz set value {x: $(macro)}
$data modify storage foo:bar baz[{bar: $(bar)}] set value {x: $(macro)}
$say $(macro)
