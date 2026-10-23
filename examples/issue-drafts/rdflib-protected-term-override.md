SPDX-License-Identifier: Community-Spec-1.0

# Draft for RDFLib/rdflib

Not filed. Case 1 is already reported as
[RDFLib/rdflib#3534](https://github.com/RDFLib/rdflib/issues/3534)
("Property-scoped context does not override a protected term (W3C toRdf
test #tpr40)", open since 2026-09-02); a fix,
[PR #3553](https://github.com/RDFLib/rdflib/pull/3553), passed
`override_protected` through `_subcontext` and was closed unmerged on
2026-10-14. So:

- **Case 1:** do not open a new issue. Add Case 1b (scalar value with
  `@type: @vocab`, the case that affects SPDX) as a comment on #3534, and
  point to PR #3553 as prior work.
- **Case 2:** looks new; file it as its own issue.

The text below is kept as the full write-up of both cases. Related finding: [T-3 in FINDINGS.md](../FINDINGS.md#t-3-rdflib-does-not-let-a-property-scoped-context-override-a-protected-term).

---

**Title:** JSON-LD: property-scoped context cannot override a `@protected`
term, and protected term redefinition raises no error

## Summary

rdflib's JSON-LD parser handles `@protected` terms differently from the
JSON-LD 1.1 Processing Algorithms and from pyld and jsonld.js, in two ways:

1. A **property-scoped context** cannot redefine a protected term. JSON-LD 1.1
   allows this ("a property-scoped context is not affected by protection, and
   can therefore override protected terms", JSON-LD 1.1 §4.1.11). rdflib
   silently keeps the protected definition, so values expand to a different
   IRI than in other processors. This is W3C test `toRdf/pr40`, already in
   `known_bugs` in `test/jsonld/test_onedotone.py` ("Investigate property
   issues").
2. Redefining a protected term **outside** a property-scoped context raises no
   error. JSON-LD 1.1 requires a `protected term redefinition` error. rdflib
   silently keeps the first definition.

## Case 1: property-scoped override is ignored

Case 1a, node-object value:

```json
{
  "@context": {
    "@version": 1.1,
    "name": {"@id": "http://example.org/name", "@protected": true},
    "kind": {"@id": "http://example.org/kind",
             "@context": {"name": "http://example.org/Kind/name"}}
  },
  "@id": "http://example.org/x",
  "kind": {"name": "v"}
}
```

| Processor | Predicate of `"v"` |
| --- | --- |
| pyld 3.3.0 | `http://example.org/Kind/name` |
| jsonld.js 8.3.3 and 9.0.0 | `http://example.org/Kind/name` |
| rdflib 7.6.0 and `main` (7.7.0a0) | `http://example.org/name` |

**Expected:** `http://example.org/Kind/name`. The value is a map, so
[Expansion](https://www.w3.org/TR/json-ld11-api/#expansion-algorithm) step 8
processes the property-scoped context with *override protected* `true`, and
[Create Term Definition](https://www.w3.org/TR/json-ld11-api/#create-term-definition)
replaces the protected term within that scope.

Case 1b, scalar value (`@type: @vocab`), the case that affects SPDX:

```json
{
  "@context": {
    "@version": 1.1,
    "name": {"@id": "http://example.org/name", "@protected": true},
    "kind": {"@id": "http://example.org/kind", "@type": "@vocab",
             "@context": {"name": "http://example.org/Kind/name"}}
  },
  "@id": "http://example.org/x",
  "kind": "name"
}
```

```python
import rdflib
g = rdflib.Graph().parse("case1.json", format="json-ld")
print(list(g.objects()))
```

| Processor | Value of `http://example.org/kind` |
| --- | --- |
| pyld 3.3.0 | `http://example.org/Kind/name` |
| jsonld.js 8.3.3 and 9.0.0 | `http://example.org/Kind/name` |
| rdflib 7.6.0 and `main` (7.7.0a0) | `http://example.org/name` |

**Expected:** `http://example.org/Kind/name`, as in pyld and jsonld.js and
per §4.1.11. Note that for scalar values, Expansion step 4.2 does not pass
*override protected*, so a literal reading of the algorithm gives a
`protected term redefinition` error here instead; this looks like the same
omission that w3c/json-ld-api#301 fixed for step 8. Either way, silently
using the protected term's IRI is not a conformant result.

## Case 2: no error on protected term redefinition

```json
{
  "@context": [
    {"@version": 1.1, "name": {"@id": "http://example.org/name", "@protected": true}},
    {"name": "http://example.org/other"}
  ],
  "@id": "http://example.org/x",
  "name": "a"
}
```

| Processor | Result |
| --- | --- |
| pyld 3.3.0 | error: `tried to redefine a protected term` |
| jsonld.js 8.3.3 and 9.0.0 | error: `tried to redefine a protected term` |
| rdflib 7.6.0 and `main` (7.7.0a0) | no error; predicate `http://example.org/name` |

**Expected:** a `protected term redefinition` error (Create Term Definition,
when *override protected* is false and the new definition differs from the
protected one).

## Cause

`Context.add_term` in `rdflib/plugins/shared/jsonld/context.py`:

```python
if self.version >= 1.1:
    existing = self.terms.get(name)
    if existing and existing.protected:
        return
```

There is no *override protected* flag, so the same silent `return` is used
both where the spec allows an override and where it requires an error.

## Suggested fix

- Add an `override_protected` parameter to the context-reading path
  (`_read_source` / `_read_term` / `add_term`).
- Pass `True` only when processing a term's scoped context from
  `get_context_for_term`, and `False` otherwise. `_subcontext` is also
  reached from `subcontext()` and `get_context_for_type` (type-scoped
  contexts), which must not override protected terms.
- In `add_term`: if the existing term is protected and `override_protected`
  is false, raise an error unless the new definition is identical (the spec
  allows an identical redefinition); if it is true, replace the term.

## Impact

Real-world: the SPDX 3 JSON-LD context. When generated with protected terms,
vocabulary values such as `profileConformance: "extension"` rely on a
property-scoped mapping to override the protected top-level term `extension`.
rdflib, and tools built on it such as pyshacl and spdx3-validate, expand the
value to the wrong IRI, while pyld and jsonld.js expand it correctly. The
SPDX generators currently work around this by leaving such terms unprotected.

## Environment

- rdflib 7.6.0 (PyPI) and `main` (7.7.0a0, 2026-10-23), Python 3.13 / 3.14
- pyld 3.3.0, jsonld.js 8.3.3 and 9.0.0 for comparison
