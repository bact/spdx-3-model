SPDX-License-Identifier: Community-Spec-1.0

# SPDX 3 flaws found by building examples, and proposed fixes

**Status: draft proposal.** This document collects flaws in the SPDX 3 model,
in its serializations (JSON-LD context, JSON schema, SHACL) and in tools, and
proposes fixes for each. It is meant to be the basis for changes to the model,
to the generators (spec-parser, specmd) and to tools.

Every finding was found or confirmed by building a concrete example and
running it through real tools, which exposes problems that reading the model
does not. Each entry names the example that exposed it, gives a repro, the
SPDX versions affected, related issues and pull requests, and then:

- **Why it happens**: the cause in the model, the spec, the generator
  (spec-parser, specmd) or the tool.
- **Fix**: what to change, with a link to a fix branch where one exists.
  Fix branches are not pull requests yet; they are for review.
- **Why the fix works**: how the change removes the cause, and what it
  leaves unchanged.

Add new findings at the end of the relevant section and keep IDs stable.

| ID | Title | Category | Severity | Affects | Status | In specmd 0.3.5 |
| --- | --- | --- | --- | --- | --- | --- |
| [S-1](#s-1-vocabulary-entries-that-share-a-name-with-a-context-term-expand-to-the-wrong-iri) | Vocabulary entries that share a name with a context term expand to the wrong IRI | Serialization | **High** | 3.0.0, 3.0.1, 3.1-dev | Fix proposed: [spec-parser branch](https://github.com/bact/spec-parser/tree/fix-vocab-term-collision), [specmd branch](https://github.com/bact/specmd/tree/fix-vocab-term-collision) | Partial |
| [S-2](#s-2-extension-property-values-need-json-ld-value-objects) | Extension property values need JSON-LD value objects | Serialization | Medium | 3.0.1, 3.1-dev | Open | No |
| [M-1](#m-1-no-way-to-declare-which-extensions-a-document-uses) | No way to declare which extensions a document uses | Model design | Medium | 3.0, 3.1-dev | Open | No (model issue) |
| [M-2](#m-2-extension-objects-cannot-stand-alone) | Extension objects cannot stand alone | Model design | Low | 3.0, 3.1-dev | Open | No (model issue) |
| [M-3](#m-3-shacl-for-extension-is-a-deny-list) | SHACL for `extension` is a deny-list | Model / generator | Low | 3.0.1, 3.1-dev | Open | No |
| [T-1](#t-1-spdx-python-model-cannot-write-json-ld-value-objects-in-extensions) | spdx-python-model cannot write JSON-LD value objects in extensions | Tool | Medium | spdx-python-model `v3_0_1`, `v3_1` | Open | n/a |
| [T-2](#t-2-spdx3-validate-cannot-check-extension-constraints) | spdx3-validate cannot check extension constraints | Tool | Low | spdx3-validate 0.0.7 | Open (needs M-1) | n/a |
| [T-3](#t-3-rdflib-does-not-let-a-property-scoped-context-override-a-protected-term) | rdflib does not let a property-scoped context override a `@protected` term | Tool | Medium | rdflib 7.6.0 and `main` (so spdx3-validate, pyshacl) | Open; worked around in [specmd branch](https://github.com/bact/specmd/tree/fix-vocab-term-collision) | Affected (see S-1) |
| [T-4](#t-4-specmd-emits-an-empty-string-term-in-the-json-ld-context) | specmd emits an empty-string term in the JSON-LD context | Tool (generator) | **High** | specmd 0.3.5 | Fix proposed: [specmd branch](https://github.com/bact/specmd/tree/fix-empty-context-term) | Affected |

Severity:

- **High**: valid-looking data silently means something else, or a model
  feature cannot be used at all.
- **Medium**: a feature works only with workarounds, or tools lose data.
- **Low**: a limitation or a weak check, with no data corruption.

"In specmd" says whether [specmd](https://github.com/bact/specmd)
(0.3.5, commit `2be4173`), the successor generator to spec-parser, already
fixes the finding: **Yes**, **No**, or **Partial**. Checked 2026-10-23 by
generating the 3.1-dev model with specmd and running the same tests.

## Related issues and pull requests

| Link | State | Related finding | Relation |
| --- | --- | --- | --- |
| [spdx/spdx-3-model#1167](https://github.com/spdx/spdx-3-model/issues/1167) Wrong use of `@vocab` in context | open | S-1 | Same area. Proposes listing every enum value in the context ("complex context", as GS1 EPCIS did), which also removes the collisions. |
| [spdx/spdx-3-model#1274](https://github.com/spdx/spdx-3-model/issues/1274) `createdBy` property vs "createdBy" relationship type | open | S-1 (collision 2) | Same name clash, raised for meaning only. Renaming either one fixes collision 2. |
| [spdx/spec-parser#204](https://github.com/spdx/spec-parser/issues/204) Set `@type` to `@id` for terms that refer to a class | open | S-1 (references) | Would stop short reference values expanding to terms, but also breaks `NoAssertionElement` short names. |
| [spdx/spec-parser#205](https://github.com/spdx/spec-parser/pull/205) Set type to `@id` for terms refer to a class | open PR | S-1 (references) | Implementation of #204. Same trade-off. |
| [spdx/spec-parser#143](https://github.com/spdx/spec-parser/issues/143), [#144](https://github.com/spdx/spec-parser/issues/144) `@vocab` vs `@id` for Element ranges | closed | S-1 (references) | Explain why references use `@vocab`: to allow `NoAssertionElement`, `NoneElement`, `SpdxOrganization` short names. |
| [spdx/spec-parser#186](https://github.com/spdx/spec-parser/pull/186) Allow classes derived from Extension | merged 2025-05 | M-3 | Introduced the deny-list. |
| [spdx/spec-parser#207](https://github.com/spdx/spec-parser/issues/207) Class constraint for Extension class is no longer generated | open | M-3 | Asks to restore a positive `sh:class Extension` check. |
| [spdx/spdx-3-model#1204](https://github.com/spdx/spdx-3-model/issues/1204) Multiplicity of extensions of the same type | open | M-2 | Semantics of several extensions of one type on one Element. |
| [JPEWdev/spdx3-validate#14](https://github.com/JPEWdev/spdx3-validate/issues/14) Model bundle | open | T-2 | Bundling model artifacts; a natural place to also accept extra shapes. |
| [spdx/spdx-spec#1458](https://github.com/spdx/spdx-spec/issues/1458) Provide an Extension how-to and an Extension example | open | all | **Addressed by** [Extension/SyntheticData](Extension/SyntheticData/), which is that example and test artifact. |
| [spdx/spdx-spec#1307](https://github.com/spdx/spdx-spec/issues/1307) JSON-LD Context fails to compact | open | S-1 | Same root area: compacting with the SPDX context does not give schema-valid JSON. S-1 adds one more cause (compacted vocabulary IRIs). |
| [spdx/spdx-spec#1312](https://github.com/spdx/spdx-spec/issues/1312) Use `@protected` rather than a fixed `@context` | open | S-2, T-3 | Would let extensions add terms (fixes much of S-2). If done with option A of S-1, rdflib must handle property-scoped overrides (T-3). |
| [spdx/spdx-3-model#1476](https://github.com/spdx/spdx-3-model/issues/1476) NamespaceMap collides with JSON Schema validation | open | S-2 | Same cause as S-2: the fixed `@context` blocks prefixes. |
| [spdx/spdx-spec#650](https://github.com/spdx/spdx-spec/issues/650) Support for additional properties disabled in JSON schema | open | S-2 | Earlier (2.x) form of the same need: carrying data beyond the spec. |
| [spdx/spdx-3-model#1017](https://github.com/spdx/spdx-3-model/issues/1017) Does the JSON schema support serialization of Extensions? | closed | S-2, M-3 | Confirms extensions need a full-IRI `type`; led to spec-parser#186 and a re-publication of the 3.0.1 SHACL (precedent for S-1 errata). Asked for "Adding Extensions" documentation, still missing. |
| [spdx/spdx-spec#1456](https://github.com/spdx/spdx-spec/issues/1456) Correct extension from [0..1] to [0..*] | open | M-2 | The Core diagram shows `Element.extension` as `[0..1]`; the model says `[0..*]`. |
| [spdx/spdx-3-model#1348](https://github.com/spdx/spdx-3-model/issues/1348) Specify programmatic profile-conformance checking via SHACL | open | S-1, M-1 | Profile conformance checking depends on `profileConformance` values expanding correctly (S-1), and on knowing which extension shapes apply (M-1). |
| [spdx/spdx-3-model#1358](https://github.com/spdx/spdx-3-model/issues/1358) Add round-trip validation CI for new-namespace examples | open | S-1, T-1 | Asks for exactly the schema + JSON-LD + round-trip checks that found S-1 and T-1; `tools/check_vocab_term_collisions.py` can be one of them. |
| [spdx/spdx-3-model#1466](https://github.com/spdx/spdx-3-model/issues/1466) Casing convention for vocab entries | open | S-1 | A naming convention for vocabulary entries can also rule out names that clash with terms. |
| [spdx/spdx-3-model#1165](https://github.com/spdx/spdx-3-model/issues/1165) SPDX could use a flat (not per-module) namespace | open | S-1 | A flat namespace would remove the profile prefixes from terms and add 4 more collisions (see S-1). |
| [spdx/spdx-spec#1427](https://github.com/spdx/spdx-spec/issues/1427) Define a normative IRI and `@context` versioning policy | open | S-1 | Needed to decide how the 3.0.x context errata is published. |
| [spdx/spdx-3-model#1345](https://github.com/spdx/spdx-3-model/issues/1345) cdxProperty 'map' is misleading; [#1168](https://github.com/spdx/spdx-3-model/issues/1168) merge CdxPropertyEntry and DictionaryEntry | open | (Extension namespace) | Other open issues on the Extension namespace, for context. |

No existing issue or PR was found for the S-1 vocabulary collisions
themselves, M-1, T-1, T-3 or T-4. Searched 2026-10-23: spdx/spec-parser,
spdx/spdx-3-model, spdx/spdx-spec, spdx/spdx-python-model, JPEWdev/shacl2code,
JPEWdev/spdx3-validate and RDFLib/rdflib.

---

## Serialization

### S-1. Vocabulary entries that share a name with a context term expand to the wrong IRI

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/), while
  declaring `profileConformance: ["extension"]`.
- **Affects:** every SPDX 3 version so far (see table).
- **Fix proposed:**
  - spec-parser: [`bact/spec-parser` `fix-vocab-term-collision`](https://github.com/bact/spec-parser/tree/fix-vocab-term-collision)
    (commit `c949ad2`).
  - specmd: [`bact/specmd` `fix-vocab-term-collision`](https://github.com/bact/specmd/tree/fix-vocab-term-collision) (commit
    `b936393`), together with [`fix-empty-context-term`](https://github.com/bact/specmd/tree/fix-empty-context-term) (commit
    `8040c73`, T-4).
- **Related:** [spdx-3-model#1167](https://github.com/spdx/spdx-3-model/issues/1167),
  [spdx-3-model#1274](https://github.com/spdx/spdx-3-model/issues/1274),
  [spec-parser#204](https://github.com/spdx/spec-parser/issues/204) / [#205](https://github.com/spdx/spec-parser/pull/205).
- **In specmd 0.3.5:** Partial. See [specmd](#specmd-035).

| Version | Context checked | Vocabulary entries checked | Collisions |
| --- | --- | --- | --- |
| 3.0.0 | published `https://spdx.org/rdf/3.0.0/spdx-context.jsonld` | 288 | 1 |
| 3.0.1 | published `https://spdx.org/rdf/3.0.1/spdx-context.jsonld` | 289 | 1 |
| 3.1-dev | generated by spec-parser (`upstream/main`) from spdx-3-model `develop` at `06a4dc57` | 430 | 3 |
| 3.1-dev with fix | generated by the fix branch above | 430 | 0 with rdflib, pyld and jsonld.js |
| 3.1-dev with specmd 0.3.5 | generated by specmd from the same model | 430 | 3 with rdflib (see T-3); pyld and jsonld.js reject the context (T-4); 0 with pyld and jsonld.js once the empty term is removed by hand |
| 3.1-dev with both specmd fix branches | generated by specmd with the two branches above | 430 | 0 with rdflib, pyld and jsonld.js, no manual edits |

Checked 2026-10-23 with
[`tools/check_vocab_term_collisions.py`](tools/check_vocab_term_collisions.py),
which expands every vocabulary entry with a JSON-LD processor (rdflib) and
compares the result with the expected IRI.

#### Mechanism

In the JSON-LD context, a vocabulary-valued property uses `"@type": "@vocab"`
with a scoped `@vocab`, so short names expand to vocabulary entries:

```json
"profileConformance": {
  "@id": "https://spdx.org/rdf/3.0.1/terms/Core/profileConformance",
  "@type": "@vocab",
  "@context": { "@vocab": "https://spdx.org/rdf/3.0.1/terms/Core/ProfileIdentifierType/" }
}
```

JSON-LD 1.1 IRI expansion looks a value up in the **terms** of the active
context first, and only falls back to `@vocab` if no term matches. The scoped
context inherits all top-level terms. So when a vocabulary entry has the same
name as a top-level term (a Core property, Core class or Core individual,
which have no namespace prefix in the context), the value expands to that
term. JSON-LD processors raise no error.

#### Why it happens

**In the model.** Core properties, Core classes and Core individuals appear in
the JSON-LD context as plain, unprefixed terms (`extension`, `createdBy`,
`requirementUID`). Vocabulary entries are written as the same kind of plain
short strings (`"extension"`). So in JSON, Core term names and vocabulary
entry names share one space of names. Nothing in the model, its naming rules
or its tooling checks names across the two, so a vocabulary entry can be given
the name of a Core property without anyone noticing. 3.0 had one such name;
3.1 development added two more.

**In spec-parser.** `jsonld_context()` in `spec_parser/rdf.py` builds the
scoped context of a vocabulary property with only an `@vocab` entry. It
assumes that every short value falls through to that `@vocab`. That holds
only if no value is also a term, because a scoped context inherits all
top-level terms, and JSON-LD looks up terms before applying `@vocab`. The
generator also skips vocabulary individuals when it builds terms ("Skip named
individuals in vocabularies"), so it never compares entry names against term
names, and nothing warns.

**In specmd 0.3.5.** specmd lists every vocabulary entry in the scoped context
(so the cause above is handled), but it also marks every top-level term
`@protected`. JSON-LD 1.1 lets a property-scoped context override a protected
term; rdflib does not (T-3), so rdflib-based tools still expand to the
property. Separately, its context has an empty term that strict processors
reject (T-4).

#### All collisions

| # | Property | Value | Should expand to | Actually expands to | 3.0.0 | 3.0.1 | 3.1-dev |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `profileConformance` | `extension` | `Core/ProfileIdentifierType/extension` | `Core/extension` (property) | yes | yes | yes |
| 2 | `relationshipType` | `createdBy` | `Core/RelationshipType/createdBy` | `Core/createdBy` (property) | no (entry did not exist) | no (entry did not exist) | yes (entry added 2025-08) |
| 3 | `externalIdentifierType` | `requirementUID` | `Core/ExternalIdentifierType/requirementUID` | `Core/requirementUID` (property) | no | no | yes (property added 2025-12, renamed from `requirementUUID` 2026-05) |

#### Example 1: `profileConformance: "extension"` (3.0.0, 3.0.1, 3.1-dev)

```json
{
  "type": "SpdxDocument",
  "profileConformance": ["core", "extension"],
  ...
}
```

Expanded RDF:

```turtle
<doc> spdx:Core/profileConformance
    <https://spdx.org/rdf/3.0.1/terms/Core/ProfileIdentifierType/core> ,
    <https://spdx.org/rdf/3.0.1/terms/Core/extension> .   # wrong
```

`spdx3-validate -s 3.0.1` (same with `-s 3.0.0`):

```text
Value Node: <https://spdx.org/rdf/3.0.1/terms/Core/extension>
Message: Value does not have class ns1:ProfileIdentifierType
```

Consequences:

- The JSON schema accepts `"extension"` (it is in the enum), SHACL rejects
  it. Writing the full IRI `.../ProfileIdentifierType/extension` instead
  passes SHACL but fails the JSON schema, which allows short names only.
  **No valid SPDX 3.0.x JSON document can claim conformance to the Extension
  profile.**
- Tools disagree on the same document: spdx-python-model (`v3_0_1`), which
  maps short names with its own table, reads it as
  `ProfileIdentifierType/extension`; JSON-LD/RDF tools read `Core/extension`.
- Repro:
  [profile-conformance-extension.spdx3.json](Extension/SyntheticData/known-issues/profile-conformance-extension.spdx3.json).

#### Example 2: `relationshipType: "createdBy"` (3.1-dev)

```json
{
  "type": "Relationship",
  "from": "https://example.org/action/build-42",
  "relationshipType": "createdBy",
  "to": ["https://example.org/agent/ci-bot"]
}
```

Expanded RDF with the 3.1-dev context:

```turtle
<rel> spdx:Core/relationshipType <https://spdx.org/rdf/3/terms/Core/createdBy> .   # wrong
```

Expected `<https://spdx.org/rdf/3/terms/Core/RelationshipType/createdBy>`.
Every Relationship of this type would fail SHACL (`sh:in` on
`relationshipType`) and be misread by RDF consumers. The `createdBy` property
of `CreationInfo` is not affected.

#### Example 3: `externalIdentifierType: "requirementUID"` (3.1-dev)

```json
{
  "type": "ExternalIdentifier",
  "externalIdentifierType": "requirementUID",
  "identifier": "REQ-0042"
}
```

expands `externalIdentifierType` to
`https://spdx.org/rdf/3/terms/Core/requirementUID` (the property) instead of
`.../Core/ExternalIdentifierType/requirementUID`.

#### Latent collisions: other namespaces

Terms from namespaces other than Core carry a prefix in the context
(`software_packageUrl`, `dataset_sensor`), so they cannot clash with an
unprefixed vocabulary entry today. Four vocabulary entries in 3.1-dev share a
name with a property in another namespace:

| Vocabulary entry | Same name as property |
| --- | --- |
| `ExternalIdentifierType/packageUrl` | `Software/packageUrl` |
| `ExternalIdentifierType/evidenceUID` | `FunctionalSafety/evidenceUID` |
| `ExternalIdentifierType/verificationUID` | `FunctionalSafety/verificationUID` |
| `DatasetType/sensor` | `Dataset/sensor` |

They would become real collisions if the context stopped prefixing non-Core
terms, as a flat namespace would ([spdx-3-model#1165](https://github.com/spdx/spdx-3-model/issues/1165)), or if
any of those properties moved to Core. The checker script catches them in
either case.

#### Related, lower risk: references in object properties

Since 3.0.1, object properties whose range is a class (`to`, `from`,
`element`, `createdBy`, `extension`, ...) are also typed `"@type": "@vocab"`
(37 properties in 3.0.1, 93 in 3.1-dev; in 3.0.0 they were `"@type": "@id"`).
This is deliberate ([spec-parser#143](https://github.com/spdx/spec-parser/issues/143),
[#144](https://github.com/spdx/spec-parser/issues/144)): it lets `"to": ["NoAssertionElement"]` expand to the
`Core/NoAssertionElement` individual. The JSON schema explicitly allows the
short names `NoAssertionElement`, `NoneElement`, `SpdxOrganization`,
`expandedlicensing_NoAssertionLicense` and `expandedlicensing_NoneLicense` in
these places. It also means any other term name used as a reference expands
to that term:

```json
"to": ["NoAssertionElement", "Person", "extension"]
```

becomes `Core/NoAssertionElement` (intended), `Core/Person` (a class) and
`Core/extension` (a property). The JSON schema rejects `"Person"` and
`"extension"` there (references must be IRIs, blank nodes, or one of the
short names above), so only producers that skip schema validation are
exposed.

Switching these properties to `"@type": "@id"`
([spec-parser#204](https://github.com/spdx/spec-parser/issues/204) / [#205](https://github.com/spdx/spec-parser/pull/205), and what specmd
0.3.5 does) removes that risk, but **breaks the short names the schema
allows**. With `@id`, `"NoAssertionElement"` is a relative IRI:

| Processor | `"to": ["NoAssertionElement"]` with `@vocab` (today) | with `@id` |
| --- | --- | --- |
| pyld | `https://spdx.org/rdf/3.0.1/terms/Core/NoAssertionElement` | `https://example.org/NoAssertionElement` (resolved against the document URL) |
| jsonld.js | `https://spdx.org/rdf/3.0.1/terms/Core/NoAssertionElement` | `NoAssertionElement` (relative IRI kept, no base) |

If #205 is merged, it should also give each such property a scoped context
that maps the allowed short names to their individuals, for example:

```json
"to": {
  "@id": "https://spdx.org/rdf/3/terms/Core/to",
  "@type": "@id",
  "@context": {
    "NoAssertionElement": {"@id": "https://spdx.org/rdf/3/terms/Core/NoAssertionElement"}
  }
}
```

Note that a term is still not used for `@id`-typed values, so this needs
`"@type": "@vocab"` again in practice. The trade-off should be settled in
spec-parser#204 before merging.

#### How tools disagree

The same JSON document means different things depending on how a tool reads
it. Tested 2026-10-23 with collision 1 (`profileConformance: "extension"`,
3.0.1); collisions 2 and 3 behave the same way under the 3.1-dev context.

| Tool kind | Tested with | Reads `"extension"` as | Verdict on the document |
| --- | --- | --- | --- |
| JSON Schema validator | SPDX 3.0.0 and 3.0.1 JSON schema | a string in the allowed enum | valid |
| Code generated from the model, using its own name table | spdx-python-model `v3_0_1` | `ProfileIdentifierType/extension` (intended) | valid |
| JSON-LD processor (expansion, toRDF) | rdflib 7.6.0, pyld 3.3.0, jsonld.js 8.3.3 | `Core/extension` (the property) | n/a (no validation) |
| SHACL validator on the RDF | spdx3-validate 0.0.7 (pyshacl over rdflib) | `Core/extension` | **invalid** (`Value does not have class ProfileIdentifierType`) |
| JSON-LD writer (compaction) of the correct IRI | pyld, jsonld.js | writes `"spdx:Core/ProfileIdentifierType/extension"` | **invalid** under the JSON schema (not in the enum) |

So:

- A schema-validating or binding-based producer writes a document that a
  SHACL-validating consumer rejects.
- A JSON-LD-based producer that writes the correct value (by compaction)
  produces a document that the JSON schema rejects.
- All three JSON-LD processors agree with each other, so this is
  spec-conformant JSON-LD behavior caused by the context, not a processor bug.
- The compaction failure adds to the ones already reported in
  [spdx-spec#1307](https://github.com/spdx/spdx-spec/issues/1307).

#### Workarounds until fixed

- 3.0.0 / 3.0.1: omit `extension` from `profileConformance`. There is no
  valid way to express it.
- 3.1-dev: none in JSON with the generated context; avoid the `createdBy`
  relationship type and the `requirementUID` external identifier type, or
  apply the fix below before release.
- Consumers: treat `Core/extension` as a `profileConformance` value as
  `ProfileIdentifierType/extension`.

#### Fix options compared

Goal: remove the disagreement while staying compatible with every kind of tool
above, assuming each tool follows its own specification (JSON Schema, JSON-LD
1.1, SHACL). Tested with rdflib, pyld and jsonld.js on the 3.0.1 and 3.1-dev
contexts.

| Option | JSON documents | JSON schema | Generated bindings | rdflib | pyld | jsonld.js | Compaction writes | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **A. Explicit mapping** of each colliding entry in the property's scoped context ([branch](https://github.com/bact/spec-parser/tree/fix-vocab-term-collision)) | unchanged | unchanged | unchanged | correct | correct | correct | `"extension"` | **Recommended** |
| A+. Explicit mapping of **every** entry ([spdx-3-model#1167](https://github.com/spdx/spdx-3-model/issues/1167), specmd) | unchanged | unchanged | unchanged | correct (if not `@protected`) | correct | correct | `"extension"` | Good; larger context. Fails in rdflib if combined with `@protected` (T-3) |
| B. Reset the scoped context: `"@context": [null, {"@vocab": ...}]` | unchanged | unchanged | unchanged | correct | **string literal** | **string literal** | n/a | Rejected: processors disagree |
| C. Rename the entry or the property in the model | **changed** | changed | regenerated | correct | correct | correct | new name | Breaking for 3.0.x data; acceptable only for the unreleased 3.1 cases |
| D. Accept full IRIs in the JSON schema | optional new form | changed | partly | correct for the full IRI | correct | correct | still compact IRI | Does not fix the short name; only a partial workaround |
| E. `"@type": "@id"` for class ranges ([spec-parser#205](https://github.com/spdx/spec-parser/pull/205)) | unchanged | unchanged | unchanged | not affected | not affected | not affected | n/a | Does not touch vocabulary properties; does not fix S-1 |

Why A is the most compatible:

- It changes only the context, so documents, the JSON schema and generated
  bindings stay exactly as they are. Everything that is valid today stays
  valid, and the only value whose meaning changes is one that is invalid
  today.
- It uses only a plain term definition inside a property-scoped context,
  a JSON-LD 1.1 feature the SPDX context already relies on. All three
  processors give the same, correct result.
- Writers that compact with the fixed context emit the short name
  (`"extension"`, `"createdBy"`, `"requirementUID"`), which the JSON schema
  accepts. So JSON-LD writers and schema validators agree again.
- It must **not** be combined with `@protected` on the colliding top-level
  terms until rdflib handles property-scoped overrides (T-3). Otherwise
  spdx3-validate and pyshacl keep the wrong expansion.

#### The fix

**spec-parser** ([branch](https://github.com/bact/spec-parser/tree/fix-vocab-term-collision)). After all terms are built, `jsonld_context()`
goes over every vocabulary property. For each entry of its vocabulary whose
name is also a top-level term, it adds an explicit mapping to the property's
scoped context, and logs a warning:

```json
"profileConformance": {
  "@id": "https://spdx.org/rdf/3/terms/Core/profileConformance",
  "@type": "@vocab",
  "@context": {
    "@vocab": "https://spdx.org/rdf/3/terms/Core/ProfileIdentifierType/",
    "extension": "https://spdx.org/rdf/3/terms/Core/ProfileIdentifierType/extension"
  }
}
```

The generated context changes only by these three mappings for 3.1-dev.

**specmd** ([branch](https://github.com/bact/specmd/tree/fix-vocab-term-collision), plus [T-4 branch](https://github.com/bact/specmd/tree/fix-empty-context-term)). specmd already maps
every entry in the scoped context. The fix removes `@protected` from the
top-level terms whose names are also vocabulary entry names (`extension`,
`createdBy`, `requirementUID` in 3.1-dev), keeps it on all other terms, and
logs a warning for each. A unit test builds a minimal graph with the
`extension` clash and checks the rdflib expansion.

#### Why the fix works

- In JSON-LD 1.1, when a property's scoped context defines a term, that
  definition replaces the inherited top-level term of the same name **inside
  that property's values only**. So inside `profileConformance`, the lookup of
  `"extension"` finds the explicit mapping first and expands to
  `ProfileIdentifierType/extension`. The problem was only ever that lookup
  order; an explicit term wins it.
- Outside the scope, nothing changes: `extension`, `createdBy` and
  `requirementUID` keys still expand to the properties. Tested: the
  `CreationInfo.createdBy` property still works.
- For compaction, the JSON-LD term selection algorithm picks the term whose
  IRI and scope match, which is now the explicit mapping. So writers emit
  `"extension"`, the form the JSON schema expects.
- In specmd, a term without `@protected` may be redefined by any context.
  rdflib therefore applies the scoped mapping like pyld and jsonld.js do, which
  removes the dependency on T-3. All other terms stay protected, so the
  protection that specmd wants against redefinition by additional contexts is
  kept everywhere except the three names that must be redefined.
- Verified: 0 collisions over all 430 entries with rdflib, pyld and jsonld.js,
  for both the spec-parser branch and the two specmd branches combined.

#### Recommendation

1. **Apply option A in the generator** and regenerate the 3.1 context:
   [bact/spec-parser `fix-vocab-term-collision`](https://github.com/bact/spec-parser/tree/fix-vocab-term-collision). It logs a warning
   for each collision, so new ones are visible when the model is built.
2. **Errata for 3.0.x.** Add the same `extension` mapping to the published
   3.0.0 and 3.0.1 contexts (or publish it in a 3.0.2). This only changes the
   expansion of a value that is invalid today, so no valid document breaks.
   There is a precedent: the 3.0.1 SHACL was re-published in place in 2025
   to accept extensions ([spdx-3-model#1017](https://github.com/spdx/spdx-3-model/issues/1017)). The
   publication policy is open in [spdx-spec#1427](https://github.com/spdx/spdx-spec/issues/1427).
   Processors that cached the old context keep the old behavior until they
   refresh it.
3. **Prevent recurrence.** Run
   [`tools/check_vocab_term_collisions.py`](tools/check_vocab_term_collisions.py)
   in CI for spdx-3-model against the generated context, as part of the
   round-trip CI asked for in [spdx-3-model#1358](https://github.com/spdx/spdx-3-model/issues/1358). Two of
   the three collisions were added during 3.1 development without anyone
   noticing.
4. **Naming guideline for the model.** Avoid giving a vocabulary entry the
   same name as a Core property, class or individual. This fits the
   vocabulary naming convention discussed in
   [spdx-3-model#1466](https://github.com/spdx/spdx-3-model/issues/1466). For collision 2, also
   settle [spdx-3-model#1274](https://github.com/spdx/spdx-3-model/issues/1274), which raises the same clash
   for meaning.
5. **Later, consider A+** (list every entry, as spdx-3-model#1167 proposes) to also stop
   unknown words resolving into the SPDX namespace. If `@protected` is added
   at the same time, check rdflib first (T-3).

#### specmd 0.3.5

**Partial**, fixed by two branches. specmd already lists every vocabulary entry
in each property's scoped context (option A+), through alias terms such as
`ProfileIdentifierType_extension`. Without its two bugs, this expands all 430
entries correctly in pyld and jsonld.js. As released:

- The context contains an empty-string term (T-4), so pyld and jsonld.js
  reject the whole context. Fixed in [`fix-empty-context-term`](https://github.com/bact/specmd/tree/fix-empty-context-term).
- All terms are `@protected`, and rdflib does not apply the property-scoped
  override (T-3), so rdflib, spdx3-validate and pyshacl still get the three
  collisions. Worked around in [`fix-vocab-term-collision`](https://github.com/bact/specmd/tree/fix-vocab-term-collision).
- Class-range properties use `"@type": "@id"`, which breaks the
  `NoAssertionElement` / `NoneElement` / `SpdxOrganization` short names (see
  [above](#related-lower-risk-references-in-object-properties)). Not changed
  yet: this is a design decision to settle with spec-parser#204 first.

### S-2. Extension property values need JSON-LD value objects

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/).
- **Affects:** 3.0.1 and 3.1-dev JSON serialization.

**Problem.** The JSON schema requires `@context` to be exactly the SPDX
context URL, so an extension cannot add its own terms or prefixes. Therefore:

- Extension `type` and property keys must be full IRIs.
- An IRI value (vocabulary entry, Element reference) must be written as
  `{"@id": "..."}`.
- A typed literal must be written as `{"@value": "...", "@type": "..."}`.

This is correct JSON-LD, but it is verbose, it is not mentioned anywhere in
the spec, and most SPDX tools do not handle it (see T-1).

Writing plain JSON values instead looks natural, passes `spdx3-validate`, and
round-trips through tools, but in RDF the IRIs become string literals and the
decimal becomes a double or a string. Repro:
[plain-scalar-values.spdx3.json](Extension/SyntheticData/known-issues/plain-scalar-values.spdx3.json)
(6 violations against the extension's own SHACL).

So today there is no compact form that is both semantically correct and
supported by tools.

**Why it happens.** The spec (serialization clause) and the JSON schema fix
`@context` to the single SPDX context URL. This keeps the JSON keys
predictable, which JSON Schema validation needs. But the SPDX context only
defines terms for SPDX. An extension's properties therefore have no term (so
keys must be full IRIs) and no type coercion (so a value's IRI-ness or
datatype must be stated in the value itself, as a value object). Nothing in the
spec explains this to extension authors.

Related: [spdx-spec#1312](https://github.com/spdx/spdx-spec/issues/1312) (use `@protected` instead of a
fixed `@context`), [spdx-3-model#1476](https://github.com/spdx/spdx-3-model/issues/1476) (NamespaceMap vs the
fixed `@context`), [spdx-spec#650](https://github.com/spdx/spdx-spec/issues/650),
[spdx-3-model#1017](https://github.com/spdx/spdx-3-model/issues/1017).

**Fix.**

- Spec: document in the Extension profile how extension data is serialized in
  JSON, with the value-object rules above.
- Schema: allow an array form for `@context` (SPDX context URL first,
  followed by extension contexts) so extensions can define terms and
  coercions, with SPDX terms `@protected` so they cannot be redefined, as
  spdx-spec#1312 proposes. This needs care to keep the schema closed for SPDX
  classes, and depends on T-3 being fixed for rdflib-based tools.

**Why the fix works.**

- Documenting the value-object rules makes today's correct form discoverable,
  with no change to any artifact.
- An extension context can define terms with coercion
  (`"generationMethod": {"@id": "...", "@type": "@vocab"}`,
  `"syntheticFraction": {"@id": "...", "@type": "xsd:decimal"}`). Plain JSON
  values then expand to the intended IRIs and datatypes, so the compact form
  becomes both natural and correct.
- With SPDX terms `@protected`, an extension context cannot change what any
  SPDX key means, so the SPDX part of the document still validates against
  the same schema. The colliding terms of S-1 must stay unprotected (as in the
  specmd fix), or rdflib must be fixed first (T-3).

---

## Model design

### M-1. No way to declare which extensions a document uses

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/).

**Problem.** Nothing in an `SpdxDocument` points to the ontology or shapes of
the extensions it uses, unlike `import`/`ExternalMap` for external Elements.
A consumer cannot discover the extension's definition, and validators cannot
find its constraints. `profileConformance` cannot help either: its values are
a closed SPDX vocabulary (and `extension` itself is broken, see S-1).

Evidence:
[valid-ext-invalid.spdx3.json](Extension/SyntheticData/documents/valid-ext-invalid.spdx3.json)
breaks every rule of the extension, and still passes `spdx3-validate`.

Related: [spdx-3-model#1348](https://github.com/spdx/spdx-3-model/issues/1348) (programmatic profile
conformance checking), [spdx-spec#1458](https://github.com/spdx/spdx-spec/issues/1458) (validators are
expected to validate extensions "provided that the extension model is
accessible").

**Why it happens.** The Extension design is deliberately open-world: any
class not known to SPDX may be an extension, so the model never needs to know
extensions in advance. The model has a mechanism to point to external
*Elements* (`import`, `ExternalMap`, with `verifiedUsing`), but no equivalent
for external *definitions* (ontologies, shapes). `profileConformance` only
names SPDX's own profiles.

**Fix.** Add a way to declare the extensions used, for example an optional
property on `SpdxDocument` listing extension definitions, each with the
extension namespace IRI, an optional location of its OWL/SHACL definition,
and an optional `verifiedUsing` hash.

**Why the fix works.**

- A validator can fetch the declared definitions, check their hashes, and add
  them to its shapes and ontology graphs (T-2). The extension's own rules are
  then checked in the same run as SPDX's, as the `pyshacl` run in this
  example does by hand.
- A consumer can tell which extensions a document relies on without
  scanning every Element.
- The property is optional, so every existing document stays valid, and the
  open-world design is kept for documents that do not declare anything.

### M-2. Extension objects cannot stand alone

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/).

**Problem.** `Extension` is not an `Element`. An extension object has no
`spdxId`, has no `creationInfo`, and the JSON schema does not allow it at the
top level of `@graph`; it must be inlined in one Element's `extension` array.
It can have an IRI `@id`
([valid-iri-node.spdx3.json](Extension/SyntheticData/documents/valid-iri-node.spdx3.json)),
but then it cannot be shared by several Elements or referenced from another
document, and it has no provenance of its own.

Related: [spdx-3-model#1204](https://github.com/spdx/spdx-3-model/issues/1204) (several extensions of the same
type on one Element), [spdx-spec#1456](https://github.com/spdx/spdx-spec/issues/1456) (diagram shows
`extension` as `[0..1]`).

**Why it happens.** `Extension` is modelled as a structured value of an
Element (like `Hash` or `ExternalRef`), not as an Element. The JSON schema
follows the model: only Elements and a few other classes may appear at the top
level of `@graph`. The spec does not say whether this is intended, nor what
it means to attach several extensions of the same type to one Element
(spdx-3-model#1204).

**Fix.** Decide and document the intent. If extensions are property bags of
one Element (the likely intent), state that an extension node belongs to
exactly one Element, define the meaning of several extensions of one type
(spdx-3-model#1204), and fix the `[0..1]` in the Core diagram
(spdx-spec#1456). If sharing is wanted, allow extension nodes with an IRI
`@id` at the top level of `@graph`.

**Why the fix works.** The data model already supports the property-bag
reading; what is missing is a stated rule. Once it is stated, tools can
implement the same behavior (for example, whether merging two documents may
merge extension nodes), and the diagram no longer contradicts the model.

### M-3. SHACL for `extension` is a deny-list

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/), reading
  the generated 3.0.1 SHACL.

**Problem.** The generated shape on `Element` for `extension` only says the
value is a blank node or IRI and is **not** one of a long list of SPDX classes
known not to derive from `Extension`. It never checks that the value is an
`Extension`, because the extension's `rdfs:subClassOf` triple is not available
to the validator (see M-1). Any unknown class passes, including a typo in an
extension's `type`.

Introduced by [spec-parser#186](https://github.com/spdx/spec-parser/pull/186) (merged 2025-05).
[spec-parser#207](https://github.com/spdx/spec-parser/issues/207) (open) reports that the 3.1 SHACL no longer
has a positive `sh:class Extension` constraint at all. specmd 0.3.5 generates
the same deny-list (**No**).

**Why it happens.** SHACL `sh:class` checks need the `rdfs:subClassOf`
chain. For a custom extension, that triple lives in the extension's own
ontology, which the validator never loads (M-1, T-2). A positive
`sh:class Extension` would therefore reject every custom extension, which is
why spec-parser#186 replaced it with a deny-list of SPDX classes known not to
be extensions.

**Fix.** Keep the deny-list in the published SHACL, since it is the only
check that works without extension definitions. When extension definitions
are available (declared as in M-1, or passed to the validator as in T-2), the
validator adds a positive `sh:class Extension` check over the merged graph.
For tools that need the expected type from the model (spec-parser#207), point
them to `rdfs:range` of `Core/extension`, which the ontology already states.

**Why the fix works.** The deny-list keeps the open-world behavior: unknown
extension classes still pass. The positive check is only applied where the
subclass chain is known, so it cannot reject a valid extension, and it catches
typos in an extension's `type` and values that are not extensions at all.
The `rdfs:range` already carries the type information spec-parser#207 needs,
without adding a constraint that would break custom extensions.

---

## Tools

### T-1. spdx-python-model cannot write JSON-LD value objects in extensions

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/).
- **Affects:** spdx-python-model `v3_0_1` and `v3_1` bindings (generated by
  shacl2code), source at `3d24398`.

**Problem.** `SHACLExtensibleObject` reads `{"@id": ...}` and
`{"@value": ..., "@type": ...}` values as plain dicts, and its
`_encode_properties` only handles `bool`, `str`, `int` and `float`. Writing a
document that it just read fails with:

```text
TypeError: Unsupported serialized type <class 'dict'> with value {'@id': '...'}
```

With plain scalars it round-trips, but a JSON number comes back as a string
(`0.35` becomes `"0.35"`).

**Why it happens.** For extensible objects, the generated decoder stores
each unknown property as the decoded JSON value, so a value object becomes a
plain `dict`. The encoder for those properties was written for JSON scalars
only, and has no branch for `dict`. The JSON number type is also lost on the
way (`0.35` comes back as `"0.35"`); the exact code path was not traced.

**Fix.** In shacl2code's templates (and so in spdx-python-model's generated
bindings), represent IRI references and typed literals in extensible objects
as distinct value types (for example an `IRIRef` and a `TypedLiteral`), and
encode them back as `{"@id"}` and `{"@value", "@type"}`. Keep JSON numbers as
numbers.

**Why the fix works.** Each JSON-LD value form then has a matching Python
type and a matching encoder branch, so reading and writing is an identity
for every value the JSON-LD spec allows, and the RDF meaning is preserved.
Documents that only use scalars behave as before.

### T-2. spdx3-validate cannot check extension constraints

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/).
- **Affects:** spdx3-validate 0.0.7.

**Problem.** spdx3-validate only loads the SPDX schema and SHACL. There is no
option to add extension shapes, so extension constraints have to be checked
with a separate `pyshacl` run.

**Why it happens.** spdx3-validate downloads the SPDX schema, SHACL and
context from fixed URLs per SPDX version (`spdx_versions.py`) and passes the
SHACL as both the shapes graph and the ontology graph to pyshacl. There is no
input for anything else.

**Fix.** Add an option such as `--shacl EXTRA.ttl` (repeatable), merged into
both the shapes graph and the ontology graph. Later, load definitions declared
in the document (M-1) automatically.

**Why the fix works.** pyshacl validates against whatever shapes it is given,
and needs the extension's `rdfs:subClassOf` triples in the ontology graph to
resolve `sh:class`. Merging the extension file into both graphs gives exactly
the run this example does by hand with `pyshacl -s synthetic-data.ttl -e
synthetic-data.ttl`, which finds the 3 violations in
`valid-ext-invalid.spdx3.json`.

### T-3. rdflib does not let a property-scoped context override a `@protected` term

- **Found by:** testing the specmd context for S-1.
- **Affects:** rdflib JSON-LD parser, 7.6.0 (latest release) and `main`
  (7.7.0a0, 2026-10-23), and so every tool built on it, including
  spdx3-validate 0.0.7 and pyshacl. A newer rdflib does not help yet.

**Problem.** JSON-LD 1.1 allows a property-scoped context to redefine a
`@protected` term (that is how a property can give a name a different meaning
inside its values). rdflib keeps the protected top-level definition instead,
without an error. pyld and jsonld.js apply the override.

Evidence, specmd 3.1-dev context (empty term removed), value
`profileConformance: "extension"`:

| Context variant | rdflib | pyld | jsonld.js |
| --- | --- | --- | --- |
| specmd as generated (`@protected` terms) | `Core/extension` (wrong) | `ProfileIdentifierType/extension` | `ProfileIdentifierType/extension` |
| same, `@protected` removed | `ProfileIdentifierType/extension` | `ProfileIdentifierType/extension` | `ProfileIdentifierType/extension` |

Minimal repro, independent of SPDX:

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

`kind` expands to `http://example.org/Kind/name` in pyld 3.3.0 and jsonld.js
8.3.3 (correct), but to `http://example.org/name` in rdflib.

**Why it happens.** In rdflib's `Context.add_term`
(`rdflib/plugins/shared/jsonld/context.py`, 7.6.0 and `main`), a new
definition for a name whose existing term is protected is silently dropped:

```python
if self.version >= 1.1:
    existing = self.terms.get(name)
    if existing and existing.protected:
        return
```

The JSON-LD 1.1 Context Processing algorithm instead passes an
"override protected" flag when it processes a property-scoped context, which
allows the redefinition. rdflib has no such flag. (Outside property-scoped
contexts, the spec requires a "protected term redefinition" error; rdflib
does not raise it either.)

**Fix.** In rdflib, pass an override flag when a term's scoped context is
processed (`get_context_for_term` / `_subcontext`), let `add_term` replace a
protected term when the flag is set, and raise the redefinition error
otherwise. Report with the repro above (no existing issue found). Until it is
fixed and released, SPDX contexts should not rely on overriding protected
terms: the specmd fix leaves exactly the colliding terms unprotected.

**Why the fix works.** With the flag, rdflib follows the same algorithm as
pyld and jsonld.js, so all three produce the same expansion for the same
context. The specmd workaround works with today's rdflib because an
unprotected term can always be redefined.

This also affects
[spdx-spec#1312](https://github.com/spdx/spdx-spec/issues/1312), which
proposes protecting SPDX terms.

### T-4. specmd emits an empty-string term in the JSON-LD context

- **Found by:** testing the specmd context for S-1.
- **Affects:** specmd 0.3.5 (`2be4173`), JSON-LD context generated from
  spdx-3-model `develop`.

**Problem.** The generated context has

```json
"": {"@id": "https://spdx.org/rdf/3/terms/Core/", "@protected": true}
```

The key comes from the Core namespace IRI itself
(`.../terms/Core/` splits into namespace `Core` and an empty name).
JSON-LD 1.1 forbids an empty term, so pyld and jsonld.js reject the **whole
context** (`Invalid JSON-LD syntax; a term cannot be an empty string`), and no
SPDX document using it can be processed. rdflib ignores the error. spec-parser
does not emit this term.

**Why it happens.** specmd adds VANN prefix annotations to each namespace,
so namespace IRIs such as `.../terms/Core/` become subjects in the graph.
`_jsonld_context()` turns every subject under the base IRI into a term by
splitting it into namespace and name. For a namespace IRI the name part is
empty, and nothing filtered it out.

**Fix** ([`bact/specmd` `fix-empty-context-term`](https://github.com/bact/specmd/tree/fix-empty-context-term), commit `8040c73`).
Skip subjects whose name part is empty. A test asserts the context has no
empty term.

**Why the fix works.** Namespace IRIs are not terms and are already covered
by the `spdx` prefix, so skipping them removes no real term. With every key
non-empty, pyld and jsonld.js accept the context. Verified: the regenerated
3.1-dev context loads in pyld, and all 382 specmd tests pass.

---

## Not yet tested

Tools to run the example corpus through next: spdx-tools-java, SPDX Online
Tools, Pitloom (`loom fragment validate`).
