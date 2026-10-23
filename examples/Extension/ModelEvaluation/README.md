SPDX-License-Identifier: Community-Spec-1.0

# Example extension: ModelEvaluation

A small SPDX 3 extension that records the results of evaluating an AI model
on a test dataset. Like [SyntheticData](../SyntheticData/), it is a test
artifact for SPDX tools and for the Extension design. It covers what
SyntheticData does not:

- an extension on a **Relationship** rather than an artifact;
- a **nested custom class** (`MetricResult`) that is not an Extension;
- **several instances** of the same extension on one Element;
- an extension **shared by IRI** between two Elements;
- a **language-tagged string**;
- a document that **declares** its extension with the proposed
  `ExtensionDefinition` (finding M-1).

## Use case

SPDX 3.0 can say that an AI model was tested on a dataset (a `testedOn`
Relationship) and can record metrics of the model (`ai_metric`). It has no
structured way to say which metric value was measured on which test dataset,
or to keep the results of several evaluation runs apart. This extension
attaches the results to the `testedOn` Relationship.

## Definitions (5)

Namespace: `https://example.org/spdx3-ext/model-evaluation/`

| Definition | Kind | Notes |
| --- | --- | --- |
| `EvaluationExtension` | Class, subclass of `Extension/Extension` | On a `testedOn` Relationship. One per evaluation run. |
| `MetricResult` | Class (not an Extension) | Structured value inside `EvaluationExtension` |
| `metricResult` | Object property, 1..* | `EvaluationExtension` → `MetricResult` |
| `metricName` | Data property, `xsd:string`, 1..1 | Plain string, no language tag |
| `metricValue` | Data property, `xsd:decimal`, 1..1 | Value object in JSON |

- [`model/ModelEvaluation/`](model/ModelEvaluation/): the definitions in the
  SPDX 3 model Markdown format. spec-parser accepts them when the folder is
  added to the SPDX model.
- [`model-evaluation.ttl`](model-evaluation.ttl): OWL ontology and SHACL
  shapes.

## Test documents

All in [`documents/`](documents/) and [`known-issues/`](known-issues/) use
SPDX 3.0.1. Results are in [`expected.json`](expected.json).

| File | Purpose | `spdx3-validate` | Extension SHACL |
| --- | --- | --- | --- |
| [`documents/valid-minimal.spdx3.json`](documents/valid-minimal.spdx3.json) | One run, one metric | pass | pass |
| [`documents/valid-multi.spdx3.json`](documents/valid-multi.spdx3.json) | Two runs (two `EvaluationExtension`s on one Relationship), two metrics each | pass | pass |
| [`documents/valid-ext-invalid.spdx3.json`](documents/valid-ext-invalid.spdx3.json) | Valid SPDX that breaks the extension: no `metricValue`, an `EvaluationExtension` where a `MetricResult` is expected | **pass** | fail (3 violations) |
| [`known-issues/shared-by-iri.spdx3.json`](known-issues/shared-by-iri.spdx3.json) | One `EvaluationExtension` with an IRI, used by two Relationships | pass | pass |
| [`known-issues/language-tagged-name.spdx3.json`](known-issues/language-tagged-name.spdx3.json) | `metricName` with a language tag | pass | fail (`xsd:string` expected) |
| [`proposed/declared-extension.spdx3.json`](proposed/declared-extension.spdx3.json) | SPDX 3.1-dev with the proposed `ExtensionDefinition` | see below | see below |

`shared-by-iri` is valid everywhere, but nothing in SPDX says what it means
for two Elements to share one extension instance (finding M-2). Do two
Relationships claim the same evaluation run, or is it a copy?

`language-tagged-name` shows a choice for extension authors: `xsd:string`
rejects a language-tagged string (`rdf:langString`). Use `rdf:langString`, or
`sh:or` of both, if a translated text is wanted.

### How to validate

```bash
python ../../tools/validate_example.py .
```

With the spdx3-validate `extra-shacl` branch, the extension is checked in the
same run:

```bash
spdx3-validate -s 3.0.1 --shacl model-evaluation.ttl -j documents/valid-multi.spdx3.json
```

### Declared extension (proposal M-1)

[`proposed/declared-extension.spdx3.json`](proposed/declared-extension.spdx3.json)
uses the model of the
[`extension-definition`](https://github.com/bact/spdx-3-model/tree/extension-definition)
branch: its SpdxDocument has an `extensionDefinition` with the extension
namespace, a `locationHint` for `model-evaluation.ttl`, and its SHA-256.
[`../../tools/validate_declared_extensions.py`](../../tools/validate_declared_extensions.py)
does what the proposal expects of a consumer: it verifies the hash, checks
that every extension type is in a declared namespace, and validates the
document against the SPDX shapes and the declared definition together.

```bash
python3 path/to/spec-parser/main.py -r -R /tmp/m1 -f path/to/spdx-3-model-extension-definition/model
python ../../tools/validate_declared_extensions.py \
  --context /tmp/m1/spdx-context.jsonld --model /tmp/m1/spdx-model.ttl \
  --location https://example.org/spdx3-ext/model-evaluation/model-evaluation.ttl=model-evaluation.ttl \
  proposed/declared-extension.spdx3.json
```

The hash in the document is the SHA-256 of `model-evaluation.ttl`; update it
when the file changes.

## Tool support matrix

Tested 2026-10-23.

| Tool | Version | Result |
| --- | --- | --- |
| spdx3-validate | 0.0.7 | All 3.0.1 documents pass. Extension constraints not checked (T-2). |
| spdx3-validate | `extension-class-check` branch, `--shacl` | Matches the extension SHACL column above. |
| spdx-python-model | upstream | Cannot write any document: nested objects and value objects are kept as `dict` (T-1). |
| spdx-python-model | shacl2code `fix-extensible-value-objects` branch | Cannot write nested `MetricResult` objects yet ("Unsupported embedded JSON-LD node object"; T-1, fix in progress). |
| tools-java | 2.0.7 | Rejects every document (T-5). |
| tools-java | `support-custom-extensions` branches | All documents round-trip, except `language-tagged-name` (language-tagged strings are rejected with an error). In `shared-by-iri`, the shared node is written inline under the other Relationship: a different JSON layout with the same RDF graph. |

## Findings

Recorded in [examples/FINDINGS.md](../../FINDINGS.md):

- M-1: the `ExtensionDefinition` prototype works end to end (hash,
  namespace coverage, SHACL).
- M-2: sharing an extension by IRI is valid but undefined.
- M-4: only Elements can have extensions.
- T-1: nested custom objects in the Python bindings.
