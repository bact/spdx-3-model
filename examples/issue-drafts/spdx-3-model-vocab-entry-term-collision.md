SPDX-License-Identifier: Community-Spec-1.0

# Draft for spdx/spdx-3-model

Not filed. Related finding:
[S-1 in FINDINGS.md](../FINDINGS.md#s-1-vocabulary-entries-that-share-a-name-with-a-context-term-expand-to-the-wrong-iri).
Tool results were run on 2026-10-24 with the document below: spdx3-validate
0.0.7, tools-java master `86ddcc9` (store 1.0.6), spdx-python-model upstream
bindings, pyld 3.3.0, rdflib 7.6.0, all with the published 3.0.1 context.

---

**Title:** Vocabulary entry names must not match a top-level JSON-LD context term

## Problem

A vocabulary entry that has the same name as a top-level term in the JSON-LD
context (a Core property, class, or keyword alias) is serialized to the wrong
IRI.

For a vocabulary-valued property, JSON-LD expands a string value against the
context's terms first. It falls back to the property's scoped `@vocab` only if
no term matches. So an entry named like a top-level term expands to that
term's IRI, not to the entry's IRI.

The JSON looks valid, but the RDF says something else.

## Current cases

| JSON | Expected IRI | Actual IRI | Since |
| --- | --- | --- | --- |
| `"profileConformance": ["extension"]` | `Core/ProfileIdentifierType/extension` | `Core/extension` (property) | 3.0.0 |
| `"relationshipType": "createdBy"` | `Core/RelationshipType/createdBy` | `Core/createdBy` (property) | 3.1-dev |
| `"externalIdentifierType": "requirementUID"` | `Core/ExternalIdentifierType/requirementUID` | `Core/requirementUID` (property) | 3.1-dev |

Two of the three collisions were added during 3.1 development without anyone
noticing.

## Not a problem

Entries in different vocabularies can share a name. For example, `other` is in
18 vocabularies and `noAssertion` in 5. Each property resolves its value
against its own vocabulary, so these work.

The only conflict is with top-level context terms.

## Why this matters for adoption

### SPDX tools disagree on the same document

This minimal 3.0.1 document declares the Extension profile:

```json
{
  "@context": "https://spdx.org/rdf/3.0.1/spdx-context.jsonld",
  "@graph": [
    {
      "type": "CreationInfo",
      "@id": "_:creationinfo",
      "created": "2026-10-24T00:00:00Z",
      "createdBy": ["https://example.org/agent/alice"],
      "specVersion": "3.0.1"
    },
    {
      "type": "Person",
      "spdxId": "https://example.org/agent/alice",
      "name": "Alice",
      "creationInfo": "_:creationinfo"
    },
    {
      "type": "SpdxDocument",
      "spdxId": "https://example.org/doc",
      "creationInfo": "_:creationinfo",
      "profileConformance": ["core", "extension"],
      "rootElement": ["https://example.org/agent/alice"],
      "element": ["https://example.org/agent/alice"]
    }
  ]
}
```

| Tool | Reads `"extension"` as | Result |
| --- | --- | --- |
| tools-java (master) | `Core/ProfileIdentifierType/extension` | valid |
| spdx-python-model | `Core/ProfileIdentifierType/extension` | reads fine |
| pyld, rdflib | `Core/extension` (the property) | wrong IRI, no error |
| spdx3-validate 0.0.7 (rdflib, pySHACL) | `Core/extension` (the property) | **invalid**: `sh:class` and `sh:in` violations on `profileConformance` |

With `"profileConformance": ["core"]`, the same document is valid in all of
them.

- **Tools that read SPDX 3 JSON as plain JSON**, using the SPDX model without
  JSON-LD processing, see the entry.
- **JSON-LD processors**, and tools built on them, expand the value as the
  published context says, to the property IRI. They follow JSON-LD
  correctly; the context is what is wrong.

Consequences:

- A producer who follows the spec gets a validation error they cannot fix,
  except by not declaring the profile.
- A consumer that loads SPDX into a graph store gets a property IRI as a
  profile value, with no error.

### New 3.1 features would ship broken

`"relationshipType": "createdBy"` and `"externalIdentifierType":
"requirementUID"` both expand to property IRIs. Every relationship of that
type would fail `sh:in`, and the type-specific shapes (`createdBy_from`,
`createdBy_to`) would never match it.

This follows from the generated context and shapes. It has not been run
through a validator, since none supports 3.1 yet.

### The workaround blocks another feature adopters asked for

JSON-LD context generators (spec-parser) can work around a collision by
mapping the entry explicitly in the property's scoped context. This is not
done today.

The mapped terms then cannot safely be `@protected`:

- The mapping redefines the term, and the JSON-LD 1.1 API (Expansion step
  4.2) gives no permission to override a protected term for a plain string
  value.
- pyld and jsonld.js allow the override anyway.
- rdflib ignores the override and still expands to the property IRI, which
  is wrong (RDFLib/rdflib#3534).

Protecting every SPDX term is what would allow extension contexts in
`@context` (spdx/spdx-spec#1312, requested by an adopter in
TNG/KernelSbom#68).

Renaming the entries fixes all of this at the source, at no cost for the two
that are not yet released.

## Proposal

1. **Naming rule:** a vocabulary entry must not have the same name as any
   top-level term in the generated context:
   - Core properties and classes (unprefixed)
   - prefixed terms from other namespaces (e.g. `software_...`)
   - the aliases `spdxId` and `type`, and the prefix `spdx`
2. **Fix the existing cases:**
   - `RelationshipType/createdBy`: rename the entry before 3.1 is released.
     The property is from 3.0. See also #1274.
   - `requirementUID`: rename the entry or the property before 3.1 is
     released. Both are new in 3.1.
   - `ProfileIdentifierType/extension`: deprecate it in 3.1 and remove it in
     4.0. It declares nothing a tool can check (see #991).
3. **Check in CI:** fail the build when the generated context has an
   entry/term collision, so new ones cannot be merged.
