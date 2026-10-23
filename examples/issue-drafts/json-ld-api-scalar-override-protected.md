SPDX-License-Identifier: Community-Spec-1.0

# Draft issue for w3c/json-ld-api

Draft of an issue to file at <https://github.com/w3c/json-ld-api/issues>.
Not filed yet. Related finding: [T-3 in FINDINGS.md](../FINDINGS.md#t-3-rdflib-does-not-let-a-property-scoped-context-override-a-protected-term).

---

**Title:** Expansion step 4.2 does not pass `override protected` for
property-scoped contexts of scalar values

## Summary

JSON-LD 1.1 §4.1.11 says "a property-scoped context is not affected by
protection, and can therefore override protected terms". The Expansion
Algorithm passes `true` for *override protected* when it applies a
property-scoped context to a map (step 8; added by #301), but not when the
element is a scalar (step 4.2):

> 4.2) If property-scoped context is defined, set active context to the result
> of the Context Processing algorithm, passing active context, property-scoped
> context as local context, and base URL from the term definition for active
> property in active context.

So, read literally, this is a `protected term redefinition` error:

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

while the same scoped context applied to `"kind": {"name": "v"}` is allowed.

## Implementations

pyld 3.3.0 and jsonld.js 8.3.3 pass *override protected* for every
property-scoped context, scalar or not, and expand `"kind": "name"` to
`http://example.org/Kind/name`. That matches §4.1.11.

## Why it matters

A vocabulary-valued property (`@type: @vocab`) with a scoped context that
maps entry names is a natural way to keep enumerated values compact. If any
entry name equals a protected top-level term, a processor that follows step
4.2 literally rejects every value of that property. The SPDX 3 JSON-LD
context has this pattern (for example `profileConformance: "extension"` vs
the `extension` property).

## Suggested change

In Expansion step 4.2, add "and `true` for override protected", as in step 8.
If that is not the intent, §4.1.11 should say that property-scoped contexts
override protected terms only for node object values.
