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
| [S-2](#s-2-extension-property-values-need-json-ld-value-objects) | Extension property values need JSON-LD value objects | Serialization | Medium | 3.0.1, 3.1-dev | Spec text proposed: [spdx-spec branch](https://github.com/bact/spdx-spec/tree/serialize-extensions) | No |
| [S-3](#s-3-spdx-shacl-shapes-target-nothing-outside-pyshacl) | SPDX SHACL shapes target nothing outside pySHACL | Serialization | **High** | 3.0.0, 3.0.1, 3.1-dev | Fix proposed: [spec-parser branch](https://github.com/bact/spec-parser/tree/fix-shacl-target-class), [specmd branch](https://github.com/bact/specmd/tree/fix-shacl-target-class) | No |
| [M-1](#m-1-no-way-to-declare-which-extensions-a-document-uses) | No way to declare which extensions a document uses | Model design | Medium | 3.0, 3.1-dev | Model change proposed: [spdx-3-model branch](https://github.com/bact/spdx-3-model/tree/extension-definition) | No (model issue) |
| [M-2](#m-2-extension-objects-cannot-be-top-level-and-their-sharing-is-unspecified) | Extension objects cannot be top-level, and their sharing is unspecified | Model design | Low | 3.0, 3.1-dev | Spec text proposed: [spdx-3-model branch](https://github.com/bact/spdx-3-model/tree/extension-semantics) | No (model issue) |
| [M-3](#m-3-shacl-for-extension-is-a-deny-list) | SHACL for `extension` is a deny-list (3.0.1+), or rejects every custom extension (3.0.0) | Model / generator | **High** in 3.0.0, Low in 3.0.1+ | 3.0.0, 3.0.1, 3.1-dev | Validator check proposed: [spdx3-validate branch](https://github.com/bact/spdx3-validate/tree/extension-class-check) | No |
| [T-1](#t-1-spdx-python-model-cannot-write-json-ld-value-objects-in-extensions) | spdx-python-model cannot write JSON-LD value objects in extensions | Tool | Medium | spdx-python-model `v3_0_1`, `v3_1` | Fix proposed: [shacl2code branch](https://github.com/bact/shacl2code/tree/fix-extensible-value-objects) | n/a |
| [T-2](#t-2-spdx3-validate-cannot-check-extension-constraints) | spdx3-validate cannot check extension constraints | Tool | Low | spdx3-validate 0.0.7 | Fix proposed: [spdx3-validate branch](https://github.com/bact/spdx3-validate/tree/extra-shacl) | n/a |
| [T-3](#t-3-rdflib-does-not-let-a-property-scoped-context-override-a-protected-term) | rdflib does not let a property-scoped context override a `@protected` term (and JSON-LD 1.1 API step 4.2 omits the override) | Tool / spec | Medium | rdflib 7.6.0 and `main` (so spdx3-validate, pyshacl); JSON-LD 1.1 API | Open; issues drafted ([rdflib](issue-drafts/rdflib-protected-term-override.md), [json-ld-api](issue-drafts/json-ld-api-scalar-override-protected.md)); worked around in [specmd branch](https://github.com/bact/specmd/tree/fix-vocab-term-collision) | Affected (see S-1) |
| [T-4](#t-4-specmd-emits-an-empty-string-term-in-the-json-ld-context) | specmd emits an empty-string term in the JSON-LD context | Tool (generator) | **High** | specmd 0.3.5 | Fix proposed: [specmd branch](https://github.com/bact/specmd/tree/fix-empty-context-term) | Affected |
| [T-5](#t-5-spdx-java-library-rejects-every-custom-extension-type) | SPDX Java library rejects every custom extension type | Tool | **High** | spdx-java-v3jsonld-store (tools-java 2.0.7, `master`) | Fix proposed: [store branch](https://github.com/bact/spdx-java-v3jsonld-store/tree/support-custom-extensions) (+ library, core) | n/a |
| [T-6](#t-6-spdx-java-library-truncates-numbers-in-extension-properties) | SPDX Java library truncates numbers in extension properties | Tool | Medium | spdx-java-v3jsonld-store | Fix proposed: [store branch](https://github.com/bact/spdx-java-v3jsonld-store/tree/fix-number-truncation) (+ library) | n/a |
| [T-7](#t-7-tools-java-verify-does-not-check-shacl) | tools-java `Verify` does not check SHACL | Tool | Low | tools-java 2.0.7, `master` | Open | n/a |
| [T-8](#t-8-rdflib-types-json-numbers-by-notation-not-by-value) | rdflib types JSON numbers by notation, not by value | Tool | Low | rdflib 7.6.0 (so pyshacl, spdx3-validate) | Open; issue drafted ([draft](issue-drafts/rdflib-jsonld-number-datatype.md)) | n/a |

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
| [spdx/spdx-3-model#1017](https://github.com/spdx/spdx-3-model/issues/1017) Does the JSON schema support serialization of Extensions? | closed | S-2, M-3 | Confirms extensions need a full-IRI `type`; led to spec-parser#186 and an in-place re-publication of the 3.0.1 SHACL (see P-4: a precedent not to repeat). Asked for "Adding Extensions" documentation, still missing. |
| [spdx/spdx-spec#1456](https://github.com/spdx/spdx-spec/issues/1456) Correct extension from [0..1] to [0..*] | open | M-2 | The Core diagram shows `Element.extension` as `[0..1]`; the model says `[0..*]`. |
| [spdx/spdx-3-model#1348](https://github.com/spdx/spdx-3-model/issues/1348) Specify programmatic profile-conformance checking via SHACL | open | S-1, M-1 | Profile conformance checking depends on `profileConformance` values expanding correctly (S-1), and on knowing which extension shapes apply (M-1). |
| [spdx/spdx-3-model#1358](https://github.com/spdx/spdx-3-model/issues/1358) Add round-trip validation CI for new-namespace examples | open | S-1, T-1 | Asks for exactly the schema + JSON-LD + round-trip checks that found S-1 and T-1; `tools/check_vocab_term_collisions.py` can be one of them. |
| [spdx/spdx-3-model#1466](https://github.com/spdx/spdx-3-model/issues/1466) Casing convention for vocab entries | open | S-1 | A naming convention for vocabulary entries can also rule out names that clash with terms. |
| [spdx/spdx-3-model#1165](https://github.com/spdx/spdx-3-model/issues/1165) SPDX could use a flat (not per-module) namespace | open | S-1 | A flat namespace would remove the profile prefixes from terms and add 4 more collisions (see S-1). |
| [spdx/spdx-spec#1427](https://github.com/spdx/spdx-spec/issues/1427) Define a normative IRI and `@context` versioning policy | open | S-1 | Needed to decide how the 3.0.x context errata is published. |
| [spdx/spdx-3-model#1345](https://github.com/spdx/spdx-3-model/issues/1345) cdxProperty 'map' is misleading; [#1168](https://github.com/spdx/spdx-3-model/issues/1168) merge CdxPropertyEntry and DictionaryEntry | open | (Extension namespace) | Other open issues on the Extension namespace, for context. |

No existing issue or PR was found for the S-1 vocabulary collisions
themselves, S-3, M-1, T-1, T-3 or T-4. Searched 2026-10-23: spdx/spec-parser,
spdx/spdx-3-model, spdx/spdx-spec, spdx/spdx-python-model, JPEWdev/shacl2code,
JPEWdev/spdx3-validate and RDFLib/rdflib.

---

## Serialization

### S-1. Vocabulary entries that share a name with a context term expand to the wrong IRI

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/), while
  declaring `profileConformance: ["extension"]`.
- **Affects:** every SPDX 3 version so far (see table).
- **Fix proposed:**
  - spec-parser: [`bact/spec-parser` `fix-vocab-term-collision`](https://github.com/bact/spec-parser/tree/fix-vocab-term-collision).
  - specmd: [`bact/specmd` `fix-vocab-term-collision`](https://github.com/bact/specmd/tree/fix-vocab-term-collision), together with [`fix-empty-context-term`](https://github.com/bact/specmd/tree/fix-empty-context-term) (T-4).
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
<doc> <https://spdx.org/rdf/3.0.1/terms/Core/profileConformance>
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

A scoped context that maps the short names to their individuals does not
help with `"@type": "@id"`: IRI expansion of `@id`-typed values does not use
terms (JSON-LD 1.1 API, IRI Expansion with *vocab* false). The short names
work under `@id` only as compact IRIs, such as `"spdx:Core/NoAssertionElement"`,
which the schema accepts and which expand the same under `@vocab` and `@id`.
The trade-off should be settled in spec-parser#204 before merging.

#### How tools disagree

The same JSON document means different things depending on how a tool reads
it. Tested 2026-10-23 with collision 1 (`profileConformance: "extension"`,
3.0.1); collisions 2 and 3 behave the same way under the 3.1-dev context.

| Tool kind | Tested with | Reads `"extension"` as | Verdict on the document |
| --- | --- | --- | --- |
| JSON Schema validator | SPDX 3.0.0 and 3.0.1 JSON schema | a string in the allowed enum | valid |
| Code generated from the model, using its own name table | spdx-python-model `v3_0_1` | `ProfileIdentifierType/extension` (intended) | valid |
| Java library reading JSON directly | tools-java 2.0.7 and `master` (spdx-java-v3jsonld-store) | `ProfileIdentifierType/extension` (intended); `Convert` writes `"extension"` back | valid (`Verify`), on a copy of the repro without the custom extension (tools-java rejects custom extensions first, T-5) |
| JSON-LD processor (expansion, toRDF) | rdflib 7.6.0, pyld 3.3.0, jsonld.js 8.3.3 and 9.0.0 | `Core/extension` (the property) | n/a (no validation) |
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
| A+. Explicit mapping of **every** entry ([spdx-3-model#1167](https://github.com/spdx/spdx-3-model/issues/1167), specmd) | unchanged | unchanged | unchanged | correct (if not `@protected`) | correct | correct | `"extension"` | Good; larger context. With `@protected` top-level terms, it is a protected term redefinition per the expansion algorithm (step 4.2, see T-3), and rdflib expands to the wrong IRI |
| B. Reset the scoped context: `"@context": [null, {"@vocab": ...}]` | unchanged | unchanged | unchanged | IRI (deviates from the spec) | **string literal** | **string literal** | n/a | Rejected: per the spec, the reset also drops the property's `@vocab` type mapping, so values become string literals (pyld, jsonld.js); rdflib's IRI result is a processor deviation |
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
2. **3.0.x: publish a fixed context as a new version (3.0.2)**, not by
   editing the published 3.0.0 or 3.0.1 contexts in place; see
   [P-4](#p-4-do-not-change-published-contexts-publish-a-new-version). The
   fix only changes the expansion of a value that is invalid today, so no
   valid document breaks when moving to 3.0.2. The publication policy is open
   in [spdx-spec#1427](https://github.com/spdx/spdx-spec/issues/1427).
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

Writing plain JSON values instead looks natural and passes `spdx3-validate`
(though tools also lose plain numbers: T-1, T-6), but in RDF the IRIs become string literals and the
decimal becomes a double or a string. Repro:
[plain-scalar-values.spdx3.json](Extension/SyntheticData/known-issues/plain-scalar-values.spdx3.json)
(6 violations against the extension's own SHACL).

So today there is no compact form that is both semantically correct and
supported by tools.

**Why it happens.** The JSON schema fixes `@context` to the single SPDX
context URL (`"const"`). The spec text does not: the 3.0.1 serialization
clause says "Additional namespace mappings may be defined within a separate
object within the context", so spec and schema contradict each other
([spdx-3-model#1476](https://github.com/spdx/spdx-3-model/issues/1476)).
Conformance requires schema validity, so the schema wins in practice. This keeps the JSON keys
predictable, which JSON Schema validation needs. But the SPDX context only
defines terms for SPDX. An extension's properties therefore have no term (so
keys must be full IRIs) and no type coercion (so a value's IRI-ness or
datatype must be stated in the value itself, as a value object). Nothing in the
spec explains this to extension authors.

Related: [spdx-spec#1312](https://github.com/spdx/spdx-spec/issues/1312) (use `@protected` instead of a
fixed `@context`), [spdx-3-model#1476](https://github.com/spdx/spdx-3-model/issues/1476) (NamespaceMap vs the
fixed `@context`), [spdx-spec#650](https://github.com/spdx/spdx-spec/issues/650),
[spdx-3-model#1017](https://github.com/spdx/spdx-3-model/issues/1017).

**Fix.** The spec text is proposed in
[`bact/spdx-spec` `serialize-extensions`](https://github.com/bact/spdx-spec/tree/serialize-extensions): a new "Extensions" section in the JSON serialization
chapter, and a note that the SPDX schema and ontology do not validate custom
extension data. A user guide is proposed for spdx/using:
[`bact/using` `extension-guide`](https://github.com/bact/using/tree/extension-guide).

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

### S-3. SPDX SHACL shapes target nothing outside pySHACL

- **Found by:** reviewing the example's own SHACL against the SHACL spec,
  then checking the SPDX model the same way.
- **Affects:** SPDX 3.0.0 and 3.0.1 SHACL (`spdx-model.ttl`), 3.1-dev as
  generated by spec-parser and specmd.

**Problem.** Every SPDX class is its own shape (`owl:Class, sh:NodeShape`),
with no `sh:targetClass`. SHACL applies the implicit class target only to a
shape that is a SHACL instance of `rdfs:Class` (SHACL §2.1.3.3). An
`owl:Class` is one only if the shapes graph states
`owl:Class rdfs:subClassOf rdfs:Class`, which the SPDX model does not.
pySHACL treats `owl:Class` as `rdfs:Class` anyway; other engines follow the
spec and select no focus nodes.

Evidence: `valid-minimal.spdx3.json` with the Person's `creationInfo`
removed, validated against the 3.0.1 shapes:

| Engine | Shapes as published | with `sh:targetClass` added |
| --- | --- | --- |
| pySHACL 0.40 | 1 violation | 1 violation |
| rdf-validate-shacl 0.5 (JS) | **conforms**, 0 results | 1 violation |

So a validator not built on pySHACL accepts any SPDX document.
[`tools/check_shacl_targets.py`](tools/check_shacl_targets.py) lists the
affected shapes: 52 in 3.0.0, 67 in 3.0.1, none with the fix branch.

**Why it happens.** spec-parser (and specmd) type each class as
`sh:NodeShape` and rely on the implicit class target, which was tested only
with pySHACL.

**Fix** ([`bact/spec-parser` `fix-shacl-target-class`](https://github.com/bact/spec-parser/tree/fix-shacl-target-class),
[`bact/specmd` `fix-shacl-target-class`](https://github.com/bact/specmd/tree/fix-shacl-target-class)).
Add `sh:targetClass <class>` to each class shape.

**Why the fix works.** An explicit class target selects the same focus nodes
(SHACL instances of the class, subclasses included) in every engine, so
pySHACL results do not change, and other engines start validating. Typing
the classes as `rdfs:Class` instead would also work, but puts reserved
vocabulary on OWL classes, outside OWL 2 DL. Publish with the next patch
version (P-4).

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
breaks three of the extension's constraints, and still passes `spdx3-validate`.

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

**Fix** ([`bact/spdx-3-model` `extension-definition`](https://github.com/bact/spdx-3-model/tree/extension-definition)). Add a way to declare the extensions used: an optional
property `SpdxDocument.extensionDefinition`, whose values are a new class
`/Extension/ExtensionDefinition` with a new `extensionNamespace` (the
namespace IRI of the extension), and the existing `locationHint` and
`verifiedUsing` properties, as in `ExternalMap`. The branch passes
spec-parser, and the generated context adds no collisions.

**Why the fix works.**

- A validator can fetch the declared definitions, check their hashes, and add
  them to its shapes and ontology graphs (T-2). The extension's own rules are
  then checked in the same run as SPDX's, as the `pyshacl` run in this
  example does by hand.
- A consumer can tell which extensions a document relies on without
  scanning every Element.
- The property is optional, so every existing document stays valid, and the
  open-world design is kept for documents that do not declare anything.

### M-2. Extension objects cannot be top-level, and their sharing is unspecified

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/).

**Problem.** `Extension` is not an `Element`. An extension object has no
`spdxId`, has no `creationInfo`, and the JSON schema does not allow it at the
top level of `@graph`; it must be inlined in one Element's `extension` array.
It can have an IRI `@id`
([valid-iri-node.spdx3.json](Extension/SyntheticData/documents/valid-iri-node.spdx3.json)),
and the schema then also lets other Elements, in the same or another
document, refer to it by that IRI (`"extension": ["<IRI>"]` passes
spdx3-validate and the extension SHACL). Nothing says whether that sharing is
allowed or what it means, and a reference from another document has no way
to import the definition. It has no provenance of its own.

Related: [spdx-3-model#1204](https://github.com/spdx/spdx-3-model/issues/1204) (several extensions of the same
type on one Element), [spdx-spec#1456](https://github.com/spdx/spdx-spec/issues/1456) (diagram shows
`extension` as `[0..1]`).

**Why it happens.** `Extension` is modelled as a structured value of an
Element (like `Hash` or `ExternalRef`), not as an Element. The JSON schema
follows the model: only Elements and a few other classes may appear at the top
level of `@graph`. The spec does not say whether this is intended, nor what
it means to attach several extensions of the same type to one Element
(spdx-3-model#1204).

**Fix** ([`bact/spdx-3-model` `extension-semantics`](https://github.com/bact/spdx-3-model/tree/extension-semantics)). Decide and document the intent. If extensions are property bags of
one Element (the likely intent), state that an extension node belongs to
exactly one Element, define the meaning of several extensions of one type
(spdx-3-model#1204), and fix the `[0..1]` in the Core diagram
(spdx-spec#1456). If sharing is wanted, allow extension nodes with an IRI
`@id` at the top level of `@graph`. The branch takes the property-bag
reading: it adds the rules to the Extension class description and fixes the
cardinality in `docs/model.drawio` (the PNG in spdx-spec needs re-exporting).

**Why the fix works.** The data model already supports the property-bag
reading; what is missing is a stated rule. Once it is stated, tools can
implement the same behavior (for example, whether merging two documents may
merge extension nodes), and the diagram no longer contradicts the model.

### M-3. SHACL for `extension` is a deny-list

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/), reading
  the generated 3.0.1 SHACL; the 3.0.0 behavior was found while testing the
  validator fix.

| Version | SHACL on `Core/extension` | Effect on a custom extension, without its definition |
| --- | --- | --- |
| 3.0.0 | positive `sh:class Extension/Extension` | **always rejected**: `Value does not have class Extension/Extension` |
| 3.0.1 (as re-published in 2025) | deny-list of SPDX classes | always accepted, also with a typo in `type` |
| 3.1-dev | deny-list (spec-parser#207) | always accepted |

So in SPDX 3.0.0, no document with a custom extension passes SHACL
validation. Repro:
[custom-extension-3-0-0.spdx3.json](Extension/SyntheticData/known-issues/custom-extension-3-0-0.spdx3.json)
(the `valid-minimal` document with the 3.0.0 context).

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

Implemented in spdx3-validate:
[`bact/spdx3-validate` `extension-class-check`](https://github.com/bact/spdx3-validate/tree/extension-class-check) (on top of `extra-shacl`). When extension definitions are
passed with `--shacl`, it adds a shape requiring every `Core/extension` value
to be an `Extension/Extension` (`sh:class`, so subclasses resolve through the
merged ontology). The shape is not added when the model already has the
positive check (3.0.0). A document whose extension `type` has a typo is
reported with the definitions supplied, and accepted without them. For
3.0.0, supplying the definition with `--shacl` also makes custom extensions
pass, since the merged ontology then knows they are Extensions, but only if
the definition subclasses the 3.0.0 `Extension` IRI. The example's
`synthetic-data.ttl` uses 3.0.1 IRIs, so the 3.0.0 repro still fails with it;
a copy rewritten to 3.0.0 IRIs passes.

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
way: the JSON encoder's `write_float` writes `json.dumps(str(v))`
(`bindings/v3_0_1/model.py`, same in `v3_1`), so `0.35` comes back as
`"0.35"`.

**Fix** ([`bact/shacl2code` `fix-extensible-value-objects`](https://github.com/bact/shacl2code/tree/fix-extensible-value-objects)).
In shacl2code's Python templates (and so in spdx-python-model's generated
bindings), represent node references, typed literals and language-tagged
strings in extensible objects as distinct value types (`IRIRef`,
`TypedLiteral`, `LangString`), and encode them back as `{"@id"}`,
`{"@value", "@type"}` and `{"@value", "@language"}`, in JSON-LD and in RDF.
Keep JSON numbers as numbers; write a float that JSON-LD would read as
`xsd:integer` (`1.0`) or that JSON cannot carry (NaN, infinities) as an
`xsd:double` value object. Node-reference IRIs are never compacted to terms,
only to prefixes ending in a gen-delim character, as JSON-LD 1.1 requires.
The RDF decoder also reads IRIs, blank nodes and typed literals of extension
properties into these types instead of dropping them. The new `Encoder`
methods have defaults, so existing encoder subclasses keep working.

The same branch fixes two related bugs found with
[valid-iri-node.spdx3.json](Extension/SyntheticData/documents/valid-iri-node.spdx3.json):

- The serializer wrote every object with an IRI at the top level of
  `@graph`, including a custom extension, which the JSON schema rejects
  there (M-2). An object whose type is not in the model, referenced once, is
  now kept inline.
- The RDF reader decoded objects of unknown types at the top level before
  reaching them through a property, so it guessed the first extensible class
  (`CdxPropertiesExtension`) and then failed its required `cdxProperty`.
  Such objects are now decoded after objects of known types, as blank nodes
  already were, so the property's range picks the class.

With the branch, every document of the example round-trips through JSON-LD
and through RDF, with extension data unchanged and output that passes
spdx3-validate. golang, rust and cpp templates are not changed.

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

**Fix** ([`bact/spdx3-validate` `extra-shacl`](https://github.com/bact/spdx3-validate/tree/extra-shacl)). A repeatable `--shacl FILE_OR_URL` option, and an `extra_shacl`
parameter of `validate()`. Each file is merged into the graph that is passed to
pyshacl as both the shapes graph and the ontology graph. Without the option,
nothing changes. Later, definitions declared in the document (M-1) can be
loaded the same way automatically.

Results on the example, exit code without / with
`--shacl synthetic-data.ttl`: `valid-ext-invalid` 0 / 1 (the 3 expected
violations), the three valid documents 0 / 0. 24 tests pass.

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

**Problem.** JSON-LD 1.1 lets a property-scoped context redefine a
`@protected` term: "a property-scoped context is not affected by protection,
and can therefore override protected terms" (JSON-LD 1.1 §4.1.11). rdflib
keeps the protected top-level definition instead, without an error. pyld and
jsonld.js apply the override.

The normative algorithm is less clear than §4.1.11. The Expansion Algorithm
passes "override protected" when the value is a map (step 8), but not when it
is a scalar (step 4.2), the case of every vocabulary value. Read literally,
a scalar value under a property-scoped context that redefines a protected
term is a "protected term redefinition" error. pyld and jsonld.js pass the
override in both cases. Step 8 lacked it too until
[w3c/json-ld-api#301](https://github.com/w3c/json-ld-api/issues/301); step 4.2
looks like the same omission (no issue found; drafted in
[`issue-drafts/json-ld-api-scalar-override-protected.md`](issue-drafts/json-ld-api-scalar-override-protected.md)).
Either way, rdflib's result (the protected term's IRI, no error) is wrong.

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
8.3.3 (correct per §4.1.11), but to `http://example.org/name` in rdflib. The
same happens for a node-object value, where step 8 passes "override
protected" unambiguously: with `"kind": {"name": "v"}`, rdflib uses
`http://example.org/name` as the predicate, pyld and jsonld.js use
`http://example.org/Kind/name`. This is W3C test `toRdf/pr40`, which rdflib
lists as a known failure (`test/jsonld/test_onedotone.py`, "Investigate
property issues").

**Why it happens.** In rdflib's `Context.add_term`
(`rdflib/plugins/shared/jsonld/context.py`, 7.6.0 and `main`), a new
definition for a name whose existing term is protected is silently dropped:

```python
if self.version >= 1.1:
    existing = self.terms.get(name)
    if existing and existing.protected:
        return
```

The JSON-LD 1.1 Expansion Algorithm instead passes an "override protected"
flag when it processes a property-scoped context (step 8, and in practice
step 4.2), which allows the redefinition. rdflib has no such flag. (Outside
property-scoped contexts, redefining a protected term with a different
definition is a "protected term redefinition" error; rdflib does not raise
it either.)

**Fix.** In rdflib, pass an override flag only when a term's scoped context
is processed (`get_context_for_term`; `_subcontext` is also reached from
`subcontext()` and `get_context_for_type`, which must not pass it), let
`add_term` replace a protected term when the flag is set, and raise the
redefinition error otherwise. Ask W3C to add "override protected" to
Expansion step 4.2, so the spec matches §4.1.11 and the processors. Report with the repro above (no existing issue found); the
issue is drafted in
[`issue-drafts/rdflib-protected-term-override.md`](issue-drafts/rdflib-protected-term-override.md),
not filed yet. It also covers a second deviation: redefining a protected
term outside a property scope raises no error in rdflib, while pyld and
jsonld.js raise `tried to redefine a protected term`. Until it is
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

**Fix** ([`bact/specmd` `fix-empty-context-term`](https://github.com/bact/specmd/tree/fix-empty-context-term)).
Skip subjects whose name part is empty. A test asserts the context has no
empty term.

**Why the fix works.** Namespace IRIs are not terms and are already covered
by the `spdx` prefix, so skipping them removes no real term. With every key
non-empty, pyld and jsonld.js accept the context. Verified: the regenerated
3.1-dev context loads in pyld, and all 382 specmd tests pass.

---

### T-5. SPDX Java library rejects every custom extension type

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/), with
  tools-java.
- **Affects:** spdx-java-v3jsonld-store (tools-java 2.0.7 and `master`
  `86ddcc9`), and so every tool on the SPDX Java library that reads SPDX 3
  JSON-LD.

**Problem.** `Verify` and `Convert` stop on every document with a custom
extension:

```text
Missing type for core object
```

**Why it happens.** The JSON-LD store maps every `type` to a class of the
SPDX Java model. A full IRI is turned into a name like `Core.https://...`,
which is not found (`JsonLDDeserializer.typeNodeToType`). Value objects
(`{"@id"}`, `{"@value", "@type"}`) in extension properties are sent to the
same path and fail the same way. On write, type IRIs are split on `.` and
inlined objects lose their `@id`.

**Fix** ([`bact/spdx-java-v3jsonld-store` `support-custom-extensions`](https://github.com/bact/spdx-java-v3jsonld-store/tree/support-custom-extensions),
with companion branches of the same name in
[`bact/Spdx-Java-Library`](https://github.com/bact/Spdx-Java-Library/tree/support-custom-extensions)
and [`bact/spdx-java-core`](https://github.com/bact/spdx-java-core/tree/support-custom-extensions)).
Accept an absolute IRI outside the SPDX namespace as a type where the model
allows an extension (values of `extension`, and inside extension property
values), and represent it with a generic `Extension` subclass through the
existing `ModelRegistry` extension hook, unless the application registered
its own class. Read `{"@id"}` as a reference (an Element in the graph, or a
URI value) and `{"@value", "@type"}` as a new `TypedLiteral` value type in
spdx-java-core; write them back in the same form, and keep the `@id` of
inlined nodes.

Still open in the Java stack: an Element written inline in an extension
value is moved to the top level on write and then added to the
SpdxDocument's `element` list on the next read; `@language`, `@list` and
untyped nested nodes in extension values are rejected with an error; and the
3.0.1 Java model names `PROP_SECURITY_LOCATOR` `SecurityLocator` instead of
`locator` (unrelated to extensions, found while testing).

**Why the fix works.** The SPDX Java model already has an extension hook and
an `Extension` base class; the store just never used them for unknown types.
With a class for every custom type and a value type for every JSON-LD value
form, reading and writing preserve the extension data, while SPDX types and
properties are handled as before.

### T-6. SPDX Java library truncates numbers in extension properties

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/), with
  tools-java (seen after changing the extension `type` to an SPDX class,
  since T-5 stops the read first).
- **Affects:** spdx-java-v3jsonld-store, as T-5.

**Problem.** A plain JSON number in a property the SPDX model does not know
is read with `asInt()`: `0.35` becomes `0`, silently.

**Why it happens.** With no schema type for the property, the deserializer
assumes an integer. The library also did not accept `Double` in lists.

**Fix** ([`bact/spdx-java-v3jsonld-store` `fix-number-truncation`](https://github.com/bact/spdx-java-v3jsonld-store/tree/fix-number-truncation),
with branches of the same name in
[`bact/Spdx-Java-Library`](https://github.com/bact/Spdx-Java-Library/tree/fix-number-truncation)
and [`bact/spdx-java-core`](https://github.com/bact/spdx-java-core/tree/fix-number-truncation)).
Type an untyped JSON number as JSON-LD does: `xsd:double` if it has a
non-zero fraction or an absolute value of at least 10^21, otherwise
`xsd:integer` (unbounded, so large integers are kept exactly). Write an
extension property's double back as a JSON number, and SPDX decimal
properties in plain decimal notation, which the JSON schema requires.

**Why the fix works.** The value read is the value JSON-LD defines for the
number, so nothing is lost, and the written JSON means the same as the input.

### T-7. tools-java `Verify` does not check SHACL

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/), with
  tools-java.
- **Affects:** tools-java 2.0.7 and `master`.

**Problem.** `Verify` on an SPDX 3 document runs the JSON schema and the Java
model's own checks, but no SHACL (the code has a `TODO`). So it accepts
documents that spdx3-validate rejects, for example
[profile-conformance-extension.spdx3.json](Extension/SyntheticData/known-issues/profile-conformance-extension.spdx3.json)
(with the custom extension removed, see T-5): the Java reader takes
`"extension"` as the intended vocabulary entry, while the RDF meaning is the
`Core/extension` property (S-1).

**Fix.** Not proposed yet. Either run the SPDX SHACL shapes in `Verify` (for
example with Apache Jena SHACL, which needs S-3 fixed to target anything), or
document that `Verify` is not a full conformance check.

### T-8. rdflib types JSON numbers by notation, not by value

- **Found by:** reviewing the spdx-spec text for S-2.
- **Affects:** rdflib 7.6.0 JSON-LD parser, and so pyshacl and spdx3-validate.

**Problem.** JSON-LD 1.1 maps a JSON number to `xsd:double` only if it has a
non-zero fractional part or an absolute value of at least 10^21, and to
`xsd:integer` otherwise (JSON-LD 1.1 API, Object to RDF Conversion; Data
Round Tripping). rdflib uses the notation instead:

| JSON | JSON-LD 1.1 (pyld) | rdflib 7.6.0 |
| --- | --- | --- |
| `5` | `"5"^^xsd:integer` | `"5"^^xsd:integer` |
| `1.0` | `"1"^^xsd:integer` | `"1.0"^^xsd:double` |
| `1e3` | `"1000"^^xsd:integer` | `"1000.0"^^xsd:double` |
| `0.35` | `"3.5E-1"^^xsd:double` | `"0.35"^^xsd:double` |

So `"count": 2.0` fails an `sh:datatype xsd:integer` shape in pyshacl, but
passes in a validator built on a conformant processor.

**Fix.** Not proposed yet; report to rdflib (issue drafted in
[`issue-drafts/rdflib-jsonld-number-datatype.md`](issue-drafts/rdflib-jsonld-number-datatype.md),
not filed). Until then, write integers
without a fraction or exponent (the spdx-spec text and the guide say so), and
write any other non-integer number as a value object.

## Proposal: JSON-LD context design following semantic web best practices

The fixes above are the smallest changes that remove each problem. This
section proposes the longer-term design they should converge to, following
the W3C [JSON-LD Best Practices](https://w3c.github.io/json-ld-bp/) (BP, editor's draft of a W3C Note) and Linked Data practice.
It also settles the two open decisions: `@vocab` vs `@id` for references
([spec-parser#204](https://github.com/spdx/spec-parser/issues/204)), and how to fix published 3.0.x
contexts.

### P-1. Vocabulary values: list every entry, no `@vocab` fallback

**Practice.** BP "Use things not strings": properties with enumerated values
are typed `"@type": "@vocab"` so that short strings are identifiers. Every
value should be an explicitly defined term ([spdx-3-model#1167](https://github.com/spdx/spdx-3-model/issues/1167)).

**Design.** Keep `"@type": "@vocab"`, and in each property's scoped context
define every entry of its vocabulary explicitly. Drop the scoped `@vocab`
(this is specmd's current design, option A+ in S-1).

**Why it is better than today.**

- An entry's meaning no longer depends on lookup order, so collisions with
  top-level terms (S-1) cannot happen for any listed entry.
- An unknown word no longer turns into an IRI in the SPDX namespace. Tested
  with `profileConformance: ["core", "extension", "foo"]`:

  | Context | `"extension"` | `"foo"` |
  | --- | --- | --- |
  | today (scoped `@vocab`) | `Core/extension` (wrong) | `.../ProfileIdentifierType/foo` (looks valid, is not defined) |
  | every entry listed, no `@vocab` | `.../ProfileIdentifierType/extension` | relative IRI, not in the SPDX namespace |

  `"extension"` expands the same in rdflib, pyld and jsonld.js. What `"foo"`
  becomes depends on the processor and the base IRI: jsonld.js keeps the
  relative `foo` and drops the triple in toRDF, pyld resolves it against its
  default base, and rdflib against the document URL. In no case is it an
  SPDX IRI, so the error is no longer hidden; SHACL `sh:in` reports it when
  the triple is produced, and the JSON schema enum rejects it in any case.
- Compaction emits the short names, so the JSON schema enum keeps matching.

### P-2. References: `@id`, with well-known individuals as compact IRIs

**Practice.** BP "Type external references": properties whose values are
references should be typed `"@type": "@id"`. A term name should never be able
to stand for an Element reference by accident.

**The catch.** Under `@id`, JSON-LD does not look values up as terms, so the
bare names the 3.0 schema allows (`"NoAssertionElement"`, `"NoneElement"`,
`"SpdxOrganization"`, `"expandedlicensing_NoAssertionLicense"`,
`"expandedlicensing_NoneLicense"`) become relative IRIs. Compact IRIs work in
both designs. Tested with `"to": [...]`:

| Value | `"@type": "@vocab"` (today) | `"@type": "@id"` |
| --- | --- | --- |
| `"NoAssertionElement"` | `Core/NoAssertionElement` | relative IRI (wrong) |
| `"spdx:Core/NoAssertionElement"` | `Core/NoAssertionElement` | `Core/NoAssertionElement` |
| `"https://example.org/b"` | unchanged | unchanged |

Same in rdflib, pyld and jsonld.js. The 3.0.1 JSON schema already accepts
`"spdx:Core/NoAssertionElement"` (it matches the IRI pattern).

**Design: migrate in two steps, with no breaking change in between.**

1. **3.1 (documentation only).** Recommend writing well-known individuals as
   compact IRIs with the `spdx:` prefix that the context already defines
   (`"spdx:Core/NoAssertionElement"`), and make tools write that form. Bare
   names keep working because references stay `@vocab`. No artifact changes.
2. **Next major version.** Type references `"@type": "@id"`
   (spec-parser#204/#205 and specmd), and drop bare names from the schema.
   By then, producers already write compact IRIs, so their documents are
   unaffected.

This keeps today's documents valid, removes the term-leak risk described in
S-1 ("references in object properties") at the end, and avoids the silent
breakage that switching to `@id` in one step would cause.

### P-3. Protect terms only when no override is needed

**Practice.** Protected terms let other contexts be added without changing
SPDX meanings; that is what allows extensions to bring their own context
([spdx-spec#1312](https://github.com/spdx/spdx-spec/issues/1312), S-2). BP "Provide ordering to arrays"
notes that protection interacts with context order.

**Design.** Protect all SPDX terms, and make sure no SPDX term ever needs to
be overridden: with P-1 plus the naming rule (no vocabulary entry named like
a term, checked in CI by `tools/check_vocab_term_collisions.py`), the only
overrides left are the three legacy names of S-1. Leave exactly those
unprotected (as the specmd fix does), or rename them in the next major
version.

**Why.** Protection then works the same in every processor, without relying
on the property-scoped exception that rdflib does not implement (T-3).

### P-4. Do not change published contexts; publish a new version

**Practice.** "Cool URIs don't change", and BP "Cache JSON-LD Contexts over
HTTP": clients keep a cached copy of a context. A versioned context URL must
always return the same content.

**Design.** Do not edit `https://spdx.org/rdf/3.0.1/spdx-context.jsonld` in
place. Publish the S-1 fix as a new patch version (3.0.2: context, schema and
SHACL together), and state the rule in the IRI and `@context` versioning
policy ([spdx-spec#1427](https://github.com/spdx/spdx-spec/issues/1427)).

**Why.** An in-place edit reaches only clients that refetch, so for a while
the same document means different things to different clients, which is
exactly the disagreement this work tries to remove. A new version makes the
change explicit: a document says which context it uses. The 2025 in-place
re-publication of the 3.0.1 SHACL ([spdx-3-model#1017](https://github.com/spdx/spdx-3-model/issues/1017)) is
a precedent to avoid repeating, not to follow. Recommendation 2 under S-1
follows this.

### Summary of the proposal

| Concern | Today | Proposed | Breaking? |
| --- | --- | --- | --- |
| Vocabulary values | scoped `@vocab` fallback | every entry listed (P-1) | no |
| References | `@vocab`, bare individual names | compact IRIs now, `@id` next major (P-2) | no, if done in two steps |
| Protection | none (spec-parser), all (specmd) | all, except legacy collisions (P-3) | no |
| Published artifacts | edited in place (3.0.1 SHACL, 2025) | new patch version (P-4) | no |

---

## Not yet tested

Tools to run the example corpus through next: SPDX Online Tools, Pitloom
(`loom fragment validate`).

Scripts to rerun all checks are in [`tools/`](tools/README.md).
