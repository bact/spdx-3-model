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
| [S-1](#s-1-vocabulary-entries-that-share-a-name-with-a-context-term-expand-to-the-wrong-iri) | Vocabulary entries that share a name with a context term expand to the wrong IRI | Serialization | **High** | 3.0.0, 3.0.1, 3.1-dev | Fix proposed: [spec-parser branch](https://github.com/bact/spec-parser/tree/fix-vocab-term-collision), [specmd branch](https://github.com/bact/specmd/tree/fix-vocab-term-collision); root fix: [rename or drop the entries](#root-fix-remove-the-collisions-in-the-model) | Partial |
| [S-2](#s-2-extension-property-values-need-json-ld-value-objects) | Extension property values need JSON-LD value objects | Serialization | Medium | 3.0.1, 3.1-dev | Spec text proposed: [spdx-spec branch](https://github.com/bact/spdx-spec/tree/serialize-extensions) | No |
| [S-3](#s-3-spdx-shacl-shapes-target-nothing-outside-pyshacl) | SPDX SHACL shapes target nothing outside pySHACL | Serialization | **High** | 3.0.0, 3.0.1, 3.1-dev | Fix proposed: [spec-parser branch](https://github.com/bact/spec-parser/tree/fix-shacl-target-class), [specmd branch](https://github.com/bact/specmd/tree/fix-shacl-target-class) | No |
| [S-4](#s-4-the-spdx-json-schema-does-not-accept-an-extension-context) | The SPDX JSON schema does not accept an extension context | Serialization | Medium | 3.0.0, 3.0.1, 3.1-dev | Fix proposed: [shacl2code `allow-extra-contexts`](https://github.com/bact/shacl2code/tree/allow-extra-contexts), [spec-parser `protect-context-terms`](https://github.com/bact/spec-parser/tree/protect-context-terms), [spdx3-validate `context-array-version`](https://github.com/bact/spdx3-validate/tree/context-array-version) | No |
| [S-5](#s-5-the-31-dev-prefix-map-can-redefine-spdx-terms) | The 3.1-dev prefix map can redefine SPDX terms | Serialization | **High** | 3.1-dev | Fix proposed: [shacl2code `fix-context-term-redefinition`](https://github.com/bact/shacl2code/tree/fix-context-term-redefinition), [spec-parser `protect-context-terms`](https://github.com/bact/spec-parser/tree/protect-context-terms) | Partial (terms protected; rdflib ignores it, T-3) |
| [S-6](#s-6-an-extension-object-can-carry-a-context-that-redefines-spdx-terms) | An extension object can carry a `@context` that redefines SPDX terms | Serialization | **High** | 3.0.1, 3.1-dev | Fix proposed: [shacl2code `forbid-embedded-context`](https://github.com/bact/shacl2code/tree/forbid-embedded-context), [spec-parser `protect-context-terms`](https://github.com/bact/spec-parser/tree/protect-context-terms) | Partial (terms protected; rdflib ignores it, T-3) |
| [M-1](#m-1-no-way-to-declare-which-extensions-a-document-uses) | No way to declare which extensions a document uses | Model design | Medium | 3.0, 3.1-dev | Model change proposed: [spdx-3-model branch](https://github.com/bact/spdx-3-model/tree/extension-definition) | No (model issue) |
| [M-2](#m-2-extension-objects-cannot-be-top-level-and-their-sharing-is-unspecified) | Extension objects cannot be top-level, and their sharing is unspecified | Model design | Low | 3.0, 3.1-dev | Spec text proposed: [spdx-3-model branch](https://github.com/bact/spdx-3-model/tree/extension-semantics) | No (model issue) |
| [M-3](#m-3-shacl-for-extension-is-a-deny-list) | SHACL for `extension` is a deny-list (3.0.1+), or rejects every custom extension (3.0.0) | Model / generator | **High** in 3.0.0, Low in 3.0.1+ | 3.0.0, 3.0.1, 3.1-dev | Validator check proposed: [spdx3-validate branch](https://github.com/bact/spdx3-validate/tree/extension-class-check) | No |
| [M-4](#m-4-only-elements-can-have-extensions) | Only Elements can have extensions | Model design | Low | 3.0, 3.1-dev | Open (options listed) | No (model issue) |
| [T-1](#t-1-spdx-python-model-cannot-write-json-ld-value-objects-in-extensions) | spdx-python-model cannot write JSON-LD value objects in extensions | Tool | Medium | spdx-python-model `v3_0_1`, `v3_1` | Fix proposed: [shacl2code branch](https://github.com/bact/shacl2code/tree/fix-extensible-value-objects) | n/a |
| [T-2](#t-2-spdx3-validate-cannot-check-extension-constraints) | spdx3-validate cannot check extension constraints | Tool | Low | spdx3-validate 0.0.7 | Fix proposed: [spdx3-validate branch](https://github.com/bact/spdx3-validate/tree/extra-shacl) | n/a |
| [T-3](#t-3-rdflib-does-not-let-a-property-scoped-context-override-a-protected-term) | rdflib does not let a property-scoped context override a `@protected` term (and JSON-LD 1.1 API step 4.2 omits the override) | Tool / spec | Medium | rdflib 7.6.0 and `main` (so spdx3-validate, pyshacl); JSON-LD 1.1 API | Open: [RDFLib/rdflib#3534](https://github.com/RDFLib/rdflib/issues/3534); drafts ([rdflib comment + issue](issue-drafts/rdflib-protected-term-override.md), [json-ld-api](issue-drafts/json-ld-api-scalar-override-protected.md)); worked around in [specmd branch](https://github.com/bact/specmd/tree/fix-vocab-term-collision) | Affected (see S-1) |
| [T-4](#t-4-specmd-emits-an-empty-string-term-in-the-json-ld-context) | specmd emits an empty-string term in the JSON-LD context | Tool (generator) | **High** | specmd 0.3.5 | Fix proposed: [specmd branch](https://github.com/bact/specmd/tree/fix-empty-context-term) | Affected |
| [T-5](#t-5-spdx-java-library-rejects-every-custom-extension-type) | SPDX Java library rejects every custom extension type | Tool | **High** | spdx-java-v3jsonld-store (tools-java 2.0.7, `master`) | Fix proposed: [store branch](https://github.com/bact/spdx-java-v3jsonld-store/tree/support-custom-extensions) (+ library, core) | n/a |
| [T-6](#t-6-spdx-java-library-truncates-numbers-in-extension-properties) | SPDX Java library truncates numbers in extension properties | Tool | Medium | spdx-java-v3jsonld-store | Fix proposed: [store branch](https://github.com/bact/spdx-java-v3jsonld-store/tree/fix-number-truncation) (+ library, core) | n/a |
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

## Fix branches and merge order

All branches are in the forks under [github.com/bact](https://github.com/bact/), with no pull
requests yet. Order: 1 model, 2 context and SHACL generators, 3 schema and
binding generator, 4 validators and libraries, 5 spec text and guides.
Within an order, branches are independent unless "Based on" names another
branch. Checked 2026-10-24.

| Order | Repository | Branch | Findings | Based on | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | spdx-3-model | [`rename-relationshiptype-createdby`](https://github.com/bact/spdx-3-model/tree/rename-relationshiptype-createdby) | S-1 | develop | Before 3.1. |
| 1 | spdx-3-model | [`deprecate-profile-extension`](https://github.com/bact/spdx-3-model/tree/deprecate-profile-extension) | S-1 | develop | Before 3.1. |
| 1 | spdx-3-model | [`extension-definition`](https://github.com/bact/spdx-3-model/tree/extension-definition) | M-1 | develop | Model proposal; needs discussion. |
| 1 | spdx-3-model | [`extension-semantics`](https://github.com/bact/spdx-3-model/tree/extension-semantics) | M-2 | develop | |
| 2 | spec-parser | [`fix-vocab-term-collision`](https://github.com/bact/spec-parser/tree/fix-vocab-term-collision) | S-1 | main | |
| 2 | spec-parser | [`protect-context-terms`](https://github.com/bact/spec-parser/tree/protect-context-terms) | S-4, S-5, S-6 | `fix-vocab-term-collision` | Exceptions disappear once the S-1 renames land. |
| 2 | spec-parser | [`fix-shacl-target-class`](https://github.com/bact/spec-parser/tree/fix-shacl-target-class) | S-3 | main | |
| 2 | specmd | [`fix-empty-context-term`](https://github.com/bact/specmd/tree/fix-empty-context-term) | T-4 | main | Merge with `fix-vocab-term-collision`. |
| 2 | specmd | [`fix-vocab-term-collision`](https://github.com/bact/specmd/tree/fix-vocab-term-collision) | S-1 | main | |
| 2 | specmd | [`fix-shacl-target-class`](https://github.com/bact/specmd/tree/fix-shacl-target-class) | S-3 | main | |
| 3 | shacl2code | [`fix-extensible-value-objects`](https://github.com/bact/shacl2code/tree/fix-extensible-value-objects) | T-1 | main | |
| 3 | shacl2code | [`fix-context-term-redefinition`](https://github.com/bact/shacl2code/tree/fix-context-term-redefinition) | S-5 | main | |
| 3 | shacl2code | [`allow-extra-contexts`](https://github.com/bact/shacl2code/tree/allow-extra-contexts) | S-4 | `fix-context-term-redefinition` | Enable the option only after SPDX terms are protected (order 2). |
| 3 | shacl2code | [`forbid-embedded-context`](https://github.com/bact/shacl2code/tree/forbid-embedded-context) | S-6 | main | Conflicts with `allow-extra-contexts` only in appended tests. |
| 4 | spdx3-validate | [`extra-shacl`](https://github.com/bact/spdx3-validate/tree/extra-shacl) | T-2 | main | |
| 4 | spdx3-validate | [`extension-class-check`](https://github.com/bact/spdx3-validate/tree/extension-class-check) | M-3 | `extra-shacl` | Squash: one rebased commit title still says "with --shacl". |
| 4 | spdx3-validate | [`context-array-version`](https://github.com/bact/spdx3-validate/tree/context-array-version) | S-4 | main | |
| 4 | spdx-java-core | [`fix-number-truncation`](https://github.com/bact/spdx-java-core/tree/fix-number-truncation) | T-6 | main | Release order: core, library, store, tools-java. Core and store add public API (minor version). |
| 4 | spdx-java-core | [`support-custom-extensions`](https://github.com/bact/spdx-java-core/tree/support-custom-extensions) | T-5 | `fix-number-truncation` | |
| 4 | Spdx-Java-Library | [`fix-number-truncation`](https://github.com/bact/Spdx-Java-Library/tree/fix-number-truncation) | T-5, T-6 | master | Needs core `TypedLiteral`. |
| 4 | spdx-java-v3jsonld-store | [`fix-number-truncation`](https://github.com/bact/spdx-java-v3jsonld-store/tree/fix-number-truncation) | T-6 | main | |
| 4 | spdx-java-v3jsonld-store | [`support-custom-extensions`](https://github.com/bact/spdx-java-v3jsonld-store/tree/support-custom-extensions) | T-5, S-4, S-6 | `fix-number-truncation` | Store 1.0.6 cannot read blank-node string references it writes (release note). |
| 5 | spdx-spec | [`serialize-extensions`](https://github.com/bact/spdx-spec/tree/serialize-extensions) | S-2, S-4 | develop | After the context and schema decisions (orders 2 and 3). |
| 5 | using | [`extension-guide`](https://github.com/bact/using/tree/extension-guide) | S-2 | main | After `serialize-extensions`. |

Related prior work, not in the merge order: spec-parser
[`use-protected`](https://github.com/bact/spec-parser/tree/use-protected) (2026-01) protects terms
and lists every vocabulary entry (option A+ in S-1, P-1), with new
per-namespace prefixes.

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
| [spdx/spdx-spec#1458](https://github.com/spdx/spdx-spec/issues/1458) Provide an Extension how-to and an Extension example | open | all | **Addressed by** [Extension/SyntheticData](Extension/SyntheticData/) and [Extension/ModelEvaluation](Extension/ModelEvaluation/) (examples and test artifacts) and the [guide branch](https://github.com/bact/using/tree/extension-guide). |
| [RDFLib/rdflib#3534](https://github.com/RDFLib/rdflib/issues/3534) Property-scoped context does not override a protected term (W3C test pr40); [PR #3553](https://github.com/RDFLib/rdflib/pull/3553) (closed unmerged) | open | T-3 | The rdflib half of T-3. |
| [spdx/tools-java#241](https://github.com/spdx/tools-java/issues/241) Add Extension class to SpdxV3Example | open | T-5 | Extension support in tools-java examples. |
| [spdx/spdx-spec#1307](https://github.com/spdx/spdx-spec/issues/1307) JSON-LD Context fails to compact | open | S-1 | Same root area: compacting with the SPDX context does not give schema-valid JSON. S-1 adds one more cause (compacted vocabulary IRIs). |
| [spdx/spdx-spec#1312](https://github.com/spdx/spdx-spec/issues/1312) Use `@protected` rather than a fixed `@context` | open | S-2, S-4, S-5, T-3 | Would let extensions add terms (fixes much of S-2). If done with option A of S-1, rdflib must handle property-scoped overrides (T-3). |
| [TNG/KernelSbom#68](https://github.com/TNG/KernelSbom/issues/68) Compact IRIs | closed | S-4 | The producer report behind spdx-spec#1312: a custom prefix in `@context`, rejected by the 3.0.1 schema although spdx-3-model's JSON-LD examples use one. |
| [spdx/spdx-3-model#1476](https://github.com/spdx/spdx-3-model/issues/1476) NamespaceMap collides with JSON Schema validation | open | S-2, S-4 | Same cause as S-2: the fixed `@context` blocks prefixes. |
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
themselves, S-3, M-1, T-1, T-4 or T-8, nor for the JSON-LD API part of T-3.
The rdflib part of T-3 is
[RDFLib/rdflib#3534](https://github.com/RDFLib/rdflib/issues/3534) (found in
the second review; an earlier search missed it). Searched 2026-10-23: spdx/spec-parser,
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

Rerun 2026-10-24 on a minimal document with only `"profileConformance":
["core", "extension"]` (in the
[issue draft](issue-drafts/spdx-3-model-vocab-entry-term-collision.md)), with
tools-java master `86ddcc9`, spdx-python-model, pyld, rdflib and
spdx3-validate 0.0.7: same results; with `["core"]` it is valid everywhere.

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
An entry named like the vocabulary property itself, or like a keyword alias
(`spdxId`, `type`) or the `spdx` prefix, cannot be mapped this way: the
scoped term would replace the property term (and its `@type: @vocab`) or the
alias in that scope. spec-parser logs an error for such an entry instead, so
it gets renamed in the model. None exists in 3.1-dev.

**specmd** ([branch](https://github.com/bact/specmd/tree/fix-vocab-term-collision), plus [T-4 branch](https://github.com/bact/specmd/tree/fix-empty-context-term)). specmd already maps
every entry in the scoped context. The fix removes `@protected` from the
top-level terms whose names are also vocabulary entry names (`extension`,
`createdBy`, `requirementUID` in 3.1-dev), keeps it on all other terms, and
logs a warning for each. It logs an error, and does not map the entry, for
an entry named like a keyword alias or like its own property, as spec-parser
does. Unit tests build minimal graphs with the `extension` clash (checking
the rdflib expansion) and with the error cases.

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

#### Root fix: remove the collisions in the model

The generator fix (option A) and the `@protected` exceptions it needs (S-4)
are workarounds. The collisions can be removed at the source, one name at a
time, by renaming or dropping the vocabulary entry, so that every SPDX term
can be protected with no exceptions:

| Name | Property (since) | Vocabulary entry (since) | Proposal | Cost |
| --- | --- | --- | --- | --- |
| `extension` | `Core/extension` (3.0) | `ProfileIdentifierType/extension` (3.0) | Deprecate the entry in 3.1, remove it in 4.0. ([branch](https://github.com/bact/spdx-3-model/tree/deprecate-profile-extension)) | Documents that list it still parse; in JSON-LD they are already wrong in 3.0.x (Example 1). |
| `requirementUID` | `Core/requirementUID` (3.1-dev) | `ExternalIdentifierType/requirementUID` (3.1-dev) | Rename one of them before 3.1 is released (e.g. the entry to `requirementIdentifier`). | None: both are unreleased. |
| `createdBy` | `Core/createdBy` (3.0, on CreationInfo, used by every document) | `RelationshipType/createdBy` (3.1-dev) | Rename the entry before 3.1 is released (e.g. to `definedBy`, [branch](https://github.com/bact/spdx-3-model/tree/rename-relationshiptype-createdby)); keep the property. | None for the entry: unreleased. |

- **`extension` in `profileConformance` declares nothing checkable.**
  Listing a profile "shall constitute a declaration that all constituent
  elements conform to the restrictions specified by that profile"
  (ElementCollection), but the Extension profile adds no restriction beyond
  the abstract `Extension` class, and since
  [spdx-3-model#991](https://github.com/spdx/spdx-3-model/issues/991)
  (closed by [#1470](https://github.com/spdx/spdx-3-model/pull/1470))
  profile conformance no longer refers to schema files. A consumer cannot
  check an extension from this value, since it does not say which extension
  or where its definition is; that is what an `ExtensionDefinition` would do
  (M-1). The spec has no requirement to list `extension` when a document uses
  extensions, so dropping the entry removes no obligation. Tools that read
  3.0 documents should accept and ignore the value.
- **`requirementUID`**: both names came in as `requirementUUID` with the
  FunctionalSafety work ([#1177](https://github.com/spdx/spdx-3-model/pull/1177),
  [#1178](https://github.com/spdx/spdx-3-model/pull/1178), 2025-12) and were
  renamed together in [#1276](https://github.com/spdx/spdx-3-model/pull/1276)
  (2026-05), so the collision has existed since they were added. The
  property's range is `ExternalIdentifier`, and the entry is the type of that
  identifier, so the pair is intended to match; only one name can be the bare
  term.
- **`createdBy`**: the property has been in Core since 3.0 and cannot be
  renamed. The relationship type was added in
  [#1092](https://github.com/spdx/spdx-3-model/pull/1092) (Hardware and
  SupplyChain separation, 2025-08) and is not in 3.0.0 or 3.0.1.
  [spdx-3-model#1274](https://github.com/spdx/spdx-3-model/issues/1274)
  already asks to rename one of them, for meaning. A name in the style of
  the other `...By` entries (`performedBy`, `invokedBy`) works, as long as it
  is not a context term itself: `originatedBy`, for example, is already a
  Core property (`Artifact`). `definedBy` is free and fits both an
  Action and a DefinedProcess (a process definition is defined, not
  initiated or authored)
  ([branch](https://github.com/bact/spdx-3-model/tree/rename-relationshiptype-createdby)).
- **Which side to rename for `requirementUID`**: it matches its siblings
  `evidenceUID` and `verificationUID`, which are also both a property and an
  `ExternalIdentifierType` entry. Those do not collide only because their
  properties are in the FunctionalSafety namespace, so their terms are
  prefixed (`functionalSafety_evidenceUID`). Renaming the Core property keeps
  the three entries uniform; renaming the entry keeps the three properties
  uniform.

Drafts: an [issue for the naming rule](issue-drafts/spdx-3-model-vocab-entry-term-collision.md)
and a [comment for spdx-3-model#1274](issue-drafts/spdx-3-model-1274-comment.md).

Once these are gone, the generators' collision handling has nothing to do:
spec-parser's `protect-context-terms` computes its exceptions from the
collisions it finds, so with none it protects every term. Keep the CI check
(Recommendation 3) and the naming guideline (4) so new collisions fail the
build instead of shipping.

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

**Problem.** The 3.0.x JSON schema requires `@context` to be exactly the
SPDX context URL, and the 3.1-dev schema allows a prefix map at most, so an
extension cannot add its own terms (S-4). Therefore:

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
- Schema: allow extension contexts after the SPDX context URL, so
  extensions can define terms and coercions (S-4, which has the details).

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

**Problem.** Each SPDX class with constraints is its own shape: an
`owl:Class` that is typed `sh:NodeShape` or has `sh:property` or
`sh:nodeKind`, with no `sh:targetClass`. SHACL applies the implicit class target only to a
shape that is a SHACL instance of `rdfs:Class` (SHACL §2.1.3.3). An
`owl:Class` is one only if the shapes graph states
`owl:Class rdfs:subClassOf rdfs:Class`, which the SPDX model does not.
pySHACL treats `owl:Class` as `rdfs:Class` anyway; other engines follow the
spec and select no focus nodes.

Evidence: `valid-minimal.spdx3.json` with the Person's `creationInfo`
removed, validated against the 3.0.1 shapes. For rdf-validate-shacl the SPDX
model is added to the data graph (as pySHACL's ontology option does), so
that `rdfs:subClassOf` is available:

| Engine | Shapes as published | with `sh:targetClass` added |
| --- | --- | --- |
| pySHACL 0.40 | 1 violation | 1 violation |
| rdf-validate-shacl 0.5 (JS) | **conforms**, 0 results | 1 violation |

So a validator not built on pySHACL accepts any SPDX document.
[`tools/check_shacl_targets.py`](tools/check_shacl_targets.py) lists the
affected shapes: 52 in 3.0.0 (all typed `sh:NodeShape`), 67 in 3.0.1 (52
typed `sh:NodeShape`, 15 more that are shapes only through `sh:property` or
`sh:nodeKind`, such as `Person` and `Extension/Extension`), none with the
fix branch.

**Why it happens.** spec-parser (and specmd) type each class as
`sh:NodeShape` and rely on the implicit class target, which was tested only
with pySHACL.

**Fix** ([`bact/spec-parser` `fix-shacl-target-class`](https://github.com/bact/spec-parser/tree/fix-shacl-target-class),
[`bact/specmd` `fix-shacl-target-class`](https://github.com/bact/specmd/tree/fix-shacl-target-class)).
Add `sh:targetClass <class>` to each class shape.

**Why the fix works.** An explicit class target selects the same focus nodes
(SHACL instances of the class, subclasses included) in every engine, so
other engines start validating. pySHACL results change in one way: shapes
that were not typed `sh:NodeShape` (the 15 in 3.0.1 with only `sh:property`
or `sh:nodeKind`, such as `Person` and `Agent`) now have a target, so their
constraints, e.g. `sh:nodeKind sh:IRI`, are checked too. Before, pySHACL did
not treat them as shapes. Like
every `sh:class` check, this needs the class hierarchy (`rdfs:subClassOf`) in
the data graph (SHACL §2.1.3.2), so a validator should add the SPDX model to
the data graph before validating; without it, subclass instances are missed
and `sh:class` reports false violations. Typing
the classes as `rdfs:Class` instead would also work, but puts reserved
vocabulary on OWL classes, outside OWL 2 DL. Publish with the next patch
version (P-4).

---

### S-4. The SPDX JSON schema does not accept an extension context

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/).
- **Affects:**
  - SPDX 3.0.0 and 3.0.1 JSON schemas: `@context` must be exactly the SPDX
    context URL (`"const"`).
  - 3.1-dev JSON schema (shacl2code 1.0.0 and later): `@context` may also be
    an array with the SPDX context URL and objects whose values are strings,
    that is, a prefix map. Context URLs other than SPDX's, and term
    definitions (object values), are rejected.
- **Consequence:** S-2.

**Problem.** In JSON-LD, a document defines terms for its extension in its
own `@context`, after the SPDX context: inline, or by the URL of a context
file the extension publishes. The extension's keys and values can then be
plain JSON, like SPDX's own properties, with the right IRIs and datatypes:

```json
"@context": [
  "https://spdx.org/rdf/3.1/spdx-context.jsonld",
  "https://example.org/spdx3-ext/synthetic-data/context.jsonld"
]
```

```json
{"type": "sd:SyntheticDataExtension", "generationMethod": "mixed",
 "syntheticFraction": "0.35", "generatorModel": "https://example.org/spdx/model/teacher-llm"}
```

with the extension's context
([synthetic-data-context.jsonld](Extension/SyntheticData/synthetic-data-context.jsonld)):

```json
{"@context": {
  "sd": "https://example.org/spdx3-ext/synthetic-data/",
  "generationMethod": {"@id": "sd:generationMethod", "@type": "@vocab",
    "@context": {"@vocab": "https://example.org/spdx3-ext/synthetic-data/DataGenerationMethodType/"}},
  "syntheticFraction": {"@id": "sd:syntheticFraction",
    "@type": "http://www.w3.org/2001/XMLSchema#decimal"},
  "generatorModel": {"@id": "sd:generatorModel", "@type": "@id"}
}}
```

No SPDX schema accepts this. Extension authors are left with full IRIs (or
prefixes, in 3.1-dev) and value objects (S-2).

The spec text and the schemas disagree. The "Parsing @context" clause
already describes `@context` as "a list comprising a string and an object"
(the namespace map), which matches the 3.1-dev schema; the 3.0.1 clause
allows "additional namespace mappings ... within a separate object within
the context", which the 3.0.1 schema rejects
([spdx-3-model#1476](https://github.com/spdx/spdx-3-model/issues/1476)).
Neither allows an extension context URL or term definitions.

The schema also limits an extension's `type`: it must match `^(?!_:).+:.+`.
A compact IRI (`"sd:SyntheticDataExtension"`) passes; a term
(`"SyntheticDataExtension"`) is rejected even when the extension context
defines it.

Repros:

- [known-issues/extension-context.spdx3.json](Extension/SyntheticData/known-issues/extension-context.spdx3.json)
  (3.0.1): [valid-full](Extension/SyntheticData/documents/valid-full.spdx3.json)
  with the extension context inline. Same RDF graph as `valid-full` (apart
  from the SpdxDocument's id and name) in rdflib and pyld; passes the
  extension SHACL.
- [proposed/extension-context-url.spdx3.json](Extension/SyntheticData/proposed/extension-context-url.spdx3.json)
  (3.1-dev): the same, with the extension context by URL. The URL is not
  published, so a processor needs it mapped to the local file (pyld with a
  document loader gives the expected extension triples).

| Tool | Result |
| --- | --- |
| JSON schema 3.0.1 | **Rejected:** `@context` must be the SPDX URL. No other error. |
| JSON schema 3.1-dev | **Rejected** (both forms): the extension context URL, or an object with object values, is not a `Context`. The same data with a prefix map, compact keys and value objects passes. |
| spdx3-validate 0.0.7 | **Rejected** before validation: "has unknown version @context" (even with `-s 3.0.1`). |
| rdflib, pyld, pySHACL | Read correctly. |
| spdx-python-model (upstream and shacl2code branch) | **Rejected** on read: "Extensible object properties must be IRIs. Got 'generationMethod'". The bindings use the generated SPDX context only and ignore the document's. |
| tools-java master | **Rejected:** "Missing type for core object" (T-5). |
| tools-java with the `support-custom-extensions` branches | Before `25d2db5`: `Verify` reported the schema error, but `Convert` **silently changed the data**: it wrote the SPDX context only and kept the compact keys, so `generationMethod`, `syntheticFraction` and `generatorModel` were dropped and the type became the IRI `sd:SyntheticDataExtension` (scheme `sd`). Since [`25d2db5`](https://github.com/bact/spdx-java-v3jsonld-store/commit/25d2db5): rejected with "Unsupported @context item ...: this store only processes the SPDX context". |

**Why it happens.** The schema pins `@context` (3.0.x) or limits it to a
prefix map (3.1-dev) so that every SPDX key keeps one meaning and JSON
Schema can validate it: a term definition or another context could map an
SPDX key to another IRI (as S-5 shows, the 3.1-dev prefix map already can).
The JSON-only reading of the spec ("Parsing @context") also only knows
prefixes. Tools then assume the SPDX context alone, and some do not check.

**Related.** [spdx-spec#1312](https://github.com/spdx/spdx-spec/issues/1312)
("Use @protect rather than a fixed @context", open since 2025-11-18) came
from [TNG/KernelSbom#68](https://github.com/TNG/KernelSbom/issues/68), a
producer that wanted a custom prefix in `@context` to shorten its own IRIs
and found that SPDX's own JSON-LD examples in spdx-3-model use one, while
the 3.0.1 schema rejects it. #1312 proposes allowing more contexts and
protecting SPDX terms with `@protected` instead. The discussion so far,
rechecked against JSON-LD 1.1 and with pyld and rdflib
([`proposed/extension-context-url.spdx3.json`](Extension/SyntheticData/proposed/extension-context-url.spdx3.json),
S-5, S-6):

| Point made in #1312 | Recheck |
| --- | --- |
| The fixed `@context` is how SPDX prevents term overriding today. | Only partly. The schema fixes the top-level `@context`, but not a `@context` inside an extension object, which can already redefine SPDX terms (S-6). |
| With extra contexts, the last one wins, so a later context could take over `spdxId`. | Correct for unprotected terms (pyld, rdflib). |
| `@protected` on every SPDX term prevents that. | Mostly. A later or embedded context that redefines a protected SPDX term is an error in pyld and jsonld.js (rdflib silently keeps the SPDX meaning, T-3). Not covered: a **property-scoped** context of an extension term may redefine protected SPDX terms inside that term's values (JSON-LD 1.1 §4.1.11 allows it), so an SPDX Element nested there can still be changed (tested with pyld). Not covered, but harmless with the schema: `@base` (spdxIds must be absolute) and `@vocab` (SPDX objects are closed). Default `@language` has no effect, since every SPDX term has an `@type`. |
| Draft schema: `@context` is the SPDX URL, or an array that `contains` it, with string or object items. | Allows the hijacks above, since items are not checked. Position does not matter for safety (an earlier context loses to the protected SPDX terms, or errors if it protects the same term), but validators detect the version from `@context` by exact match today (spdx3-validate), so a fixed position (first) is simpler. |
| Two places to change: the shacl2code schema template and the spec-parser context. | Also: validators' version detection, the spec's "Parsing @context" (JSON-only readers know prefixes only), and readers that ignore `@context` (spdx-python-model, tools-java). shacl2code is generic, so its change must come from its inputs (the given contexts), not from SPDX names. |
| (JPEWdev) If `@protected` goes in the published context file, no problem adding it now. | It does go there; documents need no change. |
| You can generate your own schema with several `--context` URLs in shacl2code. | Correct (the template requires every given URL), but a document valid against a custom schema is not valid against the SPDX schema. |

The issue was moved to 3.1-rc2. Since then, shacl2code 1.0.0
(2026-03-08) generates an array form that accepts the SPDX URL with
string-valued objects only, and the SPDX context is still not protected,
which leaves the hole in S-5. A context with `@protected` terms is in a
[comment on spdx-3-model#1167](https://github.com/spdx/spdx-3-model/issues/1167#issuecomment-3787848517).

**Fix.** Accept extension contexts after the SPDX context, and make sure
they cannot change SPDX terms. Branches:
[`bact/spec-parser` `protect-context-terms`](https://github.com/bact/spec-parser/tree/protect-context-terms)
(item 1),
[`bact/shacl2code` `allow-extra-contexts`](https://github.com/bact/shacl2code/tree/allow-extra-contexts)
(item 2, on top of the S-5 branch),
[`bact/spdx3-validate` `context-array-version`](https://github.com/bact/spdx3-validate/tree/context-array-version)
(item 4, version detection).

1. **Context (generators):** mark every SPDX term `@protected`
   ([spdx-spec#1312](https://github.com/spdx/spdx-spec/issues/1312), P-3),
   except the S-1 collisions until T-3 is fixed in rdflib. A JSON-LD
   processor then rejects any later context that redefines an SPDX term, so
   an extension context can only add terms.
2. **Schema (shacl2code `jsonschema.j2`, next minor version).**
   shacl2code is a generic generator, so the change uses only its inputs
   (the contexts passed with `--context`, and the model's extensible
   classes), with no SPDX names, behind an opt-in option (for example
   `--allow-extra-contexts`) so other models keep today's schema:
   - `@context` is the model's context URL(s), or an array that starts with
     them in the given order, followed by additional contexts: absolute URLs,
     or objects.
   - The keys of an additional context object must not be terms defined by
     the model's contexts (shacl2code already loads them, so it can generate
     a `propertyNames` exclusion, which also closes S-5), nor `@base`. Values
     are strings or term definitions, and a term definition's own
     (property-scoped) `@context` has the same key exclusion: `@protected`
     does not stop a property-scoped redefinition.
   - No `@context` in any other object (S-6).
   - An extensible class's `type` may be a term that is not a class name of
     the model.

   For SPDX, the generated schema then requires the SPDX context URL first
   and excludes every SPDX term.
3. **Spec:** replace the "list comprising a string and an object" text with
   that rule, and state that a reader processing SPDX JSON as plain JSON
   cannot interpret extension terms and must either expand the document with
   a JSON-LD processor or keep extension objects as they are. For 3.0.x
   documents, the rule stays "SPDX context URL only"
   ([`bact/spdx-spec` `serialize-extensions`](https://github.com/bact/spdx-spec/tree/serialize-extensions)
   already scopes it so).
4. **Validators and tools:** detect the SPDX version from the first item of
   the array; process the extension contexts (loading a URL, or a local
   copy). JSON Schema cannot see inside a context given by URL, so a
   validator must check a loaded context against the rules in item 2. A tool that cannot process them must reject the document, not read
   its keys under the SPDX context alone (tools-java branch, T-5). An
   ExtensionDefinition (M-1) could also give the location and hash of the
   extension's context, as it does for its ontology.

Tested with the SPDX 3.0.1 schema generated as spdx-spec does (with the
JSON serialization annotations), on all extension example documents: every
valid document stays valid on all branches, with and without the option;
`extension-context` passes only with `--allow-extra-contexts`; the S-5
document fails on `fix-context-term-redefinition`; `embedded-context` fails
on `forbid-embedded-context`. With the protected 3.1-dev context, pyld
rejects the S-5 and S-6 redefinitions and still reads `extension-context-url`
correctly; rdflib keeps the SPDX meaning silently (T-3). The three S-1
collision terms stay unprotected in the context, so only the schema stops
their redefinition. Limits: JSON Schema cannot see inside a context given by
URL, nor detect a new term that aliases an SPDX IRI.

**Why the fix works.** Protected SPDX terms stop any later or embedded
context from redefining them; the schema rules (and the validator, for
contexts by URL) close the one case protection allows, a property-scoped
context, and remove embedded contexts. So every SPDX key means the same IRI
whatever the extension context says, and the SPDX part of a document
validates against the same closed schema and means the same thing. The
extension context only adds terms, so an extension's plain JSON values
expand to the intended IRIs and datatypes, and S-2's value objects become
optional. Readers that cannot process the extension context fail loudly
instead of losing data.

---

### S-5. The 3.1-dev prefix map can redefine SPDX terms

- **Found by:** checking the 3.1-dev schema while writing S-4.
- **Affects:** 3.1-dev JSON schema (shacl2code 1.0.0 and later) with the
  3.1-dev context from spec-parser (no `@protected` terms).

**Problem.** The 3.1-dev schema accepts any key in the `@context` object,
including SPDX term names. This document is valid against the 3.1-dev
schema:

```json
{
  "@context": [
    "https://spdx.org/rdf/3.1/spdx-context.jsonld",
    {"name": "https://example.org/not-spdx/name"}
  ],
  "@graph": [
    {"type": "Person", "spdxId": "https://example.org/p", "name": "Alice", "creationInfo": "_:c"},
    {"type": "CreationInfo", "@id": "_:c", "created": "2026-10-23T00:00:00Z",
     "createdBy": ["https://example.org/p"], "specVersion": "3.1"}
  ]
}
```

pyld and rdflib both give `<https://example.org/p>
<https://example.org/not-spdx/name> "Alice"`: the Person has no SPDX
`name`. A JSON reader following "Parsing @context" sees an SPDX `name`
instead (the map only rewrites prefixes of identifiers). So the same valid
document means different things to JSON and JSON-LD readers.

**Why it happens.** The schema's `Context` object allows
`patternProperties: {".*": {"type": "string"}}`, meant for prefixes, and the
spec-parser context does not protect SPDX terms. This is the term
hijacking that [spdx-spec#1312](https://github.com/spdx/spdx-spec/issues/1312)
warned about (a later context "wins" unless SPDX terms are `@protected`):
the array form shipped in shacl2code 1.0.0 without protecting the
context. specmd protects every term
(so pyld and jsonld.js raise a protected-term error), but rdflib silently
keeps the first definition (T-3, case 2).

**Fix** ([`bact/shacl2code` `fix-context-term-redefinition`](https://github.com/bact/shacl2code/tree/fix-context-term-redefinition),
[`bact/spec-parser` `protect-context-terms`](https://github.com/bact/spec-parser/tree/protect-context-terms)).
As S-4: protect SPDX terms in the context (spec-parser, specmd),
and in shacl2code generate a `propertyNames` exclusion, for additional
context objects, of every term defined by the model's contexts (for SPDX,
that includes `spdxId`, `type` and `spdx`). shacl2code reads the term names
from the contexts it is given; nothing SPDX-specific is hard-coded.

**Why the fix works.** Protection makes a JSON-LD processor reject the
redefinition; the schema rule rejects it for JSON Schema validators and
JSON-only readers too, so no valid document can change an SPDX key's
meaning.

### S-6. An extension object can carry a `@context` that redefines SPDX terms

- **Found by:** rechecking the arguments of spdx-spec#1312 (S-4).
- **Affects:** SPDX 3.0.1 and 3.1-dev JSON schemas and contexts (no SPDX
  term is `@protected`). 3.0.0 not tested.

**Problem.** The schema fixes the top-level `@context`, but an extension
object allows any key, including `@context`. An embedded context applies to
that object and everything nested in it, so it can change what SPDX keys
mean for an SPDX Element nested in an extension value:

```json
"extension": [{
  "@context": {"name": "https://example.org/not-spdx/name",
               "software_packageVersion": "https://example.org/not-spdx/version"},
  "type": "https://example.org/spdx3-ext/synthetic-data/SyntheticDataExtension",
  "https://example.org/spdx3-ext/synthetic-data/generatorModel": {
    "type": "ai_AIPackage", "spdxId": "https://example.org/spdx/model/teacher-llm",
    "name": "teacher-llm", "software_packageVersion": "2.1", ...}
}]
```

Repro:
[known-issues/embedded-context.spdx3.json](Extension/SyntheticData/known-issues/embedded-context.spdx3.json).

| Tool | Result |
| --- | --- |
| JSON schema 3.0.1 | Valid. |
| spdx3-validate 0.0.7 | **Pass.** |
| pyld, rdflib | The AIPackage has no SPDX `name` or `packageVersion`; its name and version are `https://example.org/not-spdx/...` properties. |
| spdx-python-model (upstream and branch), tools-java (master and branches) | Rejected: `@context` is not an IRI / "Missing type for core object"; with the store branch at `25d2db5`, "Unsupported embedded @context ...". |

So the same valid document means different things to JSON readers (which
ignore the embedded context, or reject it) and JSON-LD readers, and the
validator does not notice.

**Why it happens.** Extension objects are open in the schema, to allow
custom properties, and JSON-LD allows `@context` in any node object. The SPDX
context does not protect its terms, so nothing stops the redefinition.

**Fix** ([`bact/shacl2code` `forbid-embedded-context`](https://github.com/bact/shacl2code/tree/forbid-embedded-context),
[`bact/spec-parser` `protect-context-terms`](https://github.com/bact/spec-parser/tree/protect-context-terms)).
In shacl2code's schema template, forbid `@context` in objects of
extensible classes and in any object nested in their custom properties (a
`not: {required: ["@context"]}` on those objects); this is generic, since it
depends only on which classes the model marks extensible, and can be on by
default or behind the S-4 option. Protect SPDX terms in the SPDX context
(S-4, item 1), which makes the redefinition an error in pyld and jsonld.js
even for readers that do not use the schema. In the spec, state that
`@context` appears only at the top level.

**Why the fix works.** With no embedded contexts, the only contexts are the
top-level ones, which S-4 constrains; with protected terms, any redefinition
that slips through is an error rather than a silent change.

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

Tried end to end with
[ModelEvaluation/proposed/declared-extension.spdx3.json](Extension/ModelEvaluation/proposed/declared-extension.spdx3.json)
and the prototype consumer
[`tools/validate_declared_extensions.py`](tools/validate_declared_extensions.py):
it verifies the definition's SHA-256, checks that every class and property
IRI outside SPDX is in a declared namespace, and validates the document against the SPDX shapes of
the branch plus the declared definition. A wrong hash, an undeclared
namespace and invalid extension data are each reported.

The demo needs a copy of the definition that subclasses the SPDX 3.1
`Extension` IRI: with the 3.0.1 definition, a positive `sh:class Extension`
check (M-3) fails. An extension definition is tied to the IRIs of one SPDX
version, and an extension for several versions needs one definition per
version. Open design question: should SPDX keep a version-independent IRI
for `Extension` (or state `owl:equivalentClass` across versions), so that one
extension definition can serve several SPDX versions?

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

Evidence for sharing:
[ModelEvaluation/known-issues/shared-by-iri.spdx3.json](Extension/ModelEvaluation/known-issues/shared-by-iri.spdx3.json)
defines one extension with an IRI inline on one Relationship and refers to it
from another. It passes spdx3-validate and the extension SHACL. The fixed
Java store writes it back inlined under the other Relationship: the same RDF
graph, a different JSON layout. What sharing means is not specified.

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
[`bact/spdx3-validate` `extension-class-check`](https://github.com/bact/spdx3-validate/tree/extension-class-check) (on top of `extra-shacl`). The opt-in `--require-known-extensions` option
adds a shape requiring every `Core/extension` value to be an
`Extension/Extension` (`sh:class`, so subclasses resolve through the merged
ontology, which includes the definitions passed with `--shacl`). It is opt-in
because `--shacl` is also used for policy shapes that define no extension
classes. The shape is not added when the model already has the positive
check (3.0.0). A document whose extension `type` has a typo is reported with
the option, and accepted without it. An extension value that is an IRI listed
in an `ExternalMap` is still reported: an `ExternalMap` maps Elements, and an
extension is not one (see M-4). For
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

### M-4. Only Elements can have extensions

- **Found by:** [Extension/ModelEvaluation](Extension/ModelEvaluation/),
  while choosing where to attach evaluation results.
- **Affects:** SPDX 3.0, 3.1-dev.

**Problem.** `extension` is a property of `Element` only. Structured values
such as `ExternalIdentifier`, `ExternalRef`, `IntegrityMethod`,
`CreationInfo` or `DictionaryEntry` cannot carry an extension, so data that
belongs to one of them has to be attached to the enclosing Element and point
back to the value, which has no identity (usually a blank node). For
example, a tool cannot add a "verified at" timestamp to one `Hash` of a
package.

ModelEvaluation could attach its results to a Relationship because
Relationship is an Element. The same design would not work for, say, a
per-`ExternalIdentifier` annotation.

**Why it happens.** Extension was designed to characterize Elements
(the `Extension` description: "extended characterization of Elements"). Non-Element
classes are treated as closed structured values.

**Fix.** Not proposed yet; options to discuss:

1. Keep it, and say so in the Extension description, with guidance (attach
   to the Element; give the value an IRI if it must be referenced).
2. Move `extension` to a common superclass of Element and the structured
   values. This changes many classes and the JSON schema.
3. Add `extension` only to the classes where users ask for it
   (`ExternalIdentifier`, `ExternalRef`, `IntegrityMethod`).

Option 1 costs nothing and removes the surprise; 3 can follow on demand.

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

[ModelEvaluation](Extension/ModelEvaluation/) then showed that nested
objects of custom classes (an extension value that is itself a node object,
such as `MetricResult`) were kept as plain dicts and could not be written.
The branch adds a `NodeObject` value type for them (type, id, properties,
read recursively), written back as a node object in JSON-LD and as a node
with its triples in RDF. An unknown-type node used more than once is written
inline where first used and referenced by IRI elsewhere, instead of at the
top level of `@graph`.

A second review of the branch fixed: blank-node references inside
extension values (now linked to the object and relabelled with it, so labels
cannot collide and output is the same across runs); expansion with the
static context and with the gen-delim prefix rule for node types and keys;
nodes with several types; unknown-type `@graph` items, now decoded with the
range of the property that references them; and `_:` ids that the RDF
writer wrote as IRIs. Still not supported: `@list` in extension values, and
an RDF subject of unknown type that no property references (it is still
guessed as the first extensible class).

With the branch, every 3.0.1 document of both examples round-trips through
JSON-LD and through RDF, with extension data unchanged and output that passes
spdx3-validate. 37 SPDX 3.0.1 documents without extensions read and write as
with upstream; read from RDF, five differ only in blank-node labels (upstream
wrote IRIs there). golang, rust and cpp templates are not changed.

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
8.3.3 and 9.0.0 (correct per §4.1.11), but to `http://example.org/name` in rdflib. The
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
Expansion step 4.2, so the spec matches §4.1.11 and the processors.

The rdflib bug is already reported as
[RDFLib/rdflib#3534](https://github.com/RDFLib/rdflib/issues/3534) (node-object
case, W3C test pr40); a fix,
[RDFLib/rdflib#3553](https://github.com/RDFLib/rdflib/pull/3553), was closed
unmerged. The draft
[`issue-drafts/rdflib-protected-term-override.md`](issue-drafts/rdflib-protected-term-override.md)
(not filed) adds the scalar case as a comment for #3534, and a separate
issue for a second deviation: redefining a protected term outside a property
scope raises no error in rdflib, while pyld and jsonld.js raise
`tried to redefine a protected term`. Until it is
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
with [`bact/spdx-java-core` `support-custom-extensions`](https://github.com/bact/spdx-java-core/tree/support-custom-extensions)
and [`bact/Spdx-Java-Library` `fix-number-truncation`](https://github.com/bact/Spdx-Java-Library/tree/fix-number-truncation),
which has the library change both fixes need).
Accept an absolute IRI outside the SPDX namespace as a type where the model
allows an extension (values of `extension`, and inside extension property
values), and represent it with a generic `Extension` subclass through the
existing `ModelRegistry` extension hook, unless the application registered
its own class. Read `{"@id"}` as a reference (an Element in the graph, or a
URI value) and `{"@value", "@type"}` as a new `TypedLiteral` value type in
spdx-java-core; write them back in the same form, and keep the `@id` of
inlined nodes. When an object with an IRI appears more than once, merge
the values of every occurrence, as JSON-LD node map generation does; a
different value for a single-valued SPDX property is an error. The default
extension class is used only for SPDX 3 and never for IRIs in the SPDX
namespace. Rejected types get a message saying why.

For release notes: core and store add public API (`TypedLiteral`,
`ModelRegistry` methods, `GenericExtension`), so they need a minor version.
A node shared by blank-node id is written inline once and referenced as
`"_:..."` elsewhere, which the released store (1.0.6) cannot read back.

The store also rejects any `@context` other than the SPDX context URL(s), and
any embedded `@context`, instead of reading the keys as if only the SPDX
context applied, which silently dropped extension properties defined by an
extension context (S-4; [`25d2db5`](https://github.com/bact/spdx-java-v3jsonld-store/commit/25d2db5)).

Still open in the Java stack: an Element
written inline in an extension value is moved to the top level on write and
then added to the SpdxDocument's `element` list on the next read; `@language`,
`@list` and untyped nested nodes in extension values are rejected with an
error; and the 3.0.1 Java model names `PROP_SECURITY_LOCATOR`
`SecurityLocator` instead of `locator` (unrelated to extensions, found while
testing).

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
extension property's double back as a JSON number (as an `xsd:double` value
object in canonical form when JSON-LD would read the number as an integer),
and SPDX decimal properties in plain decimal notation, which the JSON schema
requires. Reject a value of an SPDX integer property that is not an integer
or does not fit in an `int`, instead of truncating or wrapping it.

**Why the fix works.** The value read is the value JSON-LD defines for the
number, so nothing is lost, and the written JSON means the same as the input.

### T-7. tools-java `Verify` does not check SHACL

- **Found by:** [Extension/SyntheticData](Extension/SyntheticData/), with
  tools-java.
- **Affects:** tools-java 2.0.7 and `master`.

**Problem.** `Verify` on an SPDX 3 document runs the JSON schema and the Java
model's own checks, but no SHACL (`Verify.java` has a `TODO` to "Implement
verification against the OWL schema"). So it accepts
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
overrides left are the three names of S-1. Leave exactly those
unprotected (as the specmd fix does) until they are removed: two are
unreleased and can be renamed before 3.1, and `extension` can be deprecated
(see [S-1, root fix](#root-fix-remove-the-collisions-in-the-model)).

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

Tools to run the example corpora through next: SPDX Online Tools, Pitloom
(`loom fragment validate`).

Scripts to rerun all checks are in [`tools/`](tools/README.md).
