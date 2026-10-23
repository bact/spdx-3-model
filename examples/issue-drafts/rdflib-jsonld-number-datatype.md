SPDX-License-Identifier: Community-Spec-1.0

# Draft issue for RDFLib/rdflib

Draft of an issue to file at <https://github.com/RDFLib/rdflib/issues>.
Not filed yet. Related finding: [T-8 in FINDINGS.md](../FINDINGS.md#t-8-rdflib-types-json-numbers-by-notation-not-by-value).

---

**Title:** JSON-LD: native numbers are typed by notation, not by value
(`1.0` becomes `xsd:double`)

## Summary

JSON-LD 1.1 maps a native JSON number to `xsd:double` only if it has a
non-zero fractional part or an absolute value of at least 10^21; otherwise it
is `xsd:integer` ([Object to RDF Conversion](https://www.w3.org/TR/json-ld11-api/#object-to-rdf-conversion),
[Data Round Tripping](https://www.w3.org/TR/json-ld11-api/#data-round-tripping)).
The double's lexical form is the canonical XSD form (`3.5E-1`). rdflib uses
the JSON notation instead.

## Repro

```python
import json, rdflib
for v in ["5", "1.0", "1e3", "0.35"]:
    doc = '{"@id": "http://x/a", "http://x/p": %s}' % v
    g = rdflib.Graph().parse(data=doc, format="json-ld")
    print(v, [o.n3() for o in g.objects()])
```

| JSON | Expected (pyld, jsonld.js) | rdflib 7.6.0 |
| --- | --- | --- |
| `5` | `"5"^^xsd:integer` | `"5"^^xsd:integer` |
| `1.0` | `"1"^^xsd:integer` | `"1.0"^^xsd:double` |
| `1e3` | `"1000"^^xsd:integer` | `"1000.0"^^xsd:double` |
| `0.35` | `"3.5E-1"^^xsd:double` | `"0.35"^^xsd:double` |

The value of `0.35` is the same either way; the datatype of `1.0` and `1e3`
is not.

## Impact

pySHACL uses rdflib, so `{"count": 2.0}` fails `sh:datatype xsd:integer` in
pySHACL but passes in a validator built on a conformant JSON-LD processor.

## Suggested fix

In the JSON-LD to RDF conversion, for a native number `n` that is not a
boolean: if `n` has a zero fractional part and `abs(n) < 1e21`, emit
`xsd:integer` with the integer's canonical form; otherwise emit `xsd:double`
with the canonical double form.
