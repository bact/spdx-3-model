SPDX-License-Identifier: Community-Spec-1.0

# SyntheticData: an example SPDX 3 extension

A small extension that uses the SPDX 3 `Extension` mechanism to record
**how the content of a dataset was generated**: by humans, by a machine
(synthetic data), or a mix of both.

It has two purposes:

1. Show how to define and use an SPDX 3 extension.
2. Serve as a **test corpus** for SPDX tools. Do tools really support
   extensions? Does the Extension design in the SPDX 3 model have gaps?
   See [Findings](#findings) and [examples/FINDINGS.md](../../FINDINGS.md).

## Use case

Datasets used to train or evaluate AI models are increasingly generated, in
whole or in part, by other AI models (synthetic data, distillation).
Knowing this matters for model quality ("model collapse"), for evaluation
integrity, and for compliance with the terms of use of the generating model.

SPDX 3.0 can say that an `ai_AIPackage` `generates` a `dataset_DatasetPackage`,
but it cannot characterize the dataset itself as human-generated,
machine-generated, or mixed, nor say how much of it is synthetic.
`dataset_DatasetType` has no such entry.

## Definitions (5)

Namespace: `https://example.org/spdx3-ext/synthetic-data/`

| Definition | Kind | Range / values | Cardinality | What it exercises in tools |
| --- | --- | --- | --- | --- |
| `SyntheticDataExtension` | Class, subclass of `/Extension/Extension` | | | custom extension type |
| `generationMethod` | Object property | `DataGenerationMethodType` | 1..1 | IRI value (vocabulary entry) |
| `DataGenerationMethodType` | Vocabulary | `humanGenerated`, `machineGenerated`, `mixed`, `noAssertion` | | vocabulary outside SPDX |
| `syntheticFraction` | Data property | `xsd:decimal`, 0 to 1 | 0..1 | typed literal |
| `generatorModel` | Object property | `/AI/AIPackage` | 0..* | reference from an extension to an SPDX Element |

Files:

- [`model/SyntheticData/`](model/SyntheticData/): the definitions in the SPDX 3
  model Markdown format. This is the form one would submit to SPDX if the
  extension proved generally useful.
- [`synthetic-data.ttl`](synthetic-data.ttl): OWL ontology and SHACL shapes for
  the extension, so its constraints can be checked by machine.

## Using the extension in SPDX 3 JSON-LD

The SPDX JSON schema requires `@context` to be exactly
`https://spdx.org/rdf/3.0.1/spdx-context.jsonld`, so an extension cannot add
its own prefixes. Therefore:

- `type` and the property keys are full IRIs.
- An IRI value (a vocabulary entry or an Element reference) is written as
  `{"@id": "..."}`.
- A typed literal is written as `{"@value": "...", "@type": "..."}`.
- The extension object is inlined in the Element's `extension` array.
  The JSON schema does not allow it at the top level of `@graph`.

```json
"extension": [
  {
    "type": "https://example.org/spdx3-ext/synthetic-data/SyntheticDataExtension",
    "https://example.org/spdx3-ext/synthetic-data/generationMethod": {
      "@id": "https://example.org/spdx3-ext/synthetic-data/DataGenerationMethodType/mixed"
    },
    "https://example.org/spdx3-ext/synthetic-data/syntheticFraction": {
      "@value": "0.35",
      "@type": "http://www.w3.org/2001/XMLSchema#decimal"
    },
    "https://example.org/spdx3-ext/synthetic-data/generatorModel": {
      "@id": "https://example.org/spdx/model/teacher-llm"
    }
  }
]
```

## Test documents

All documents use SPDX 3.0.1, the latest version supported by
`spdx3-validate`.

| File | Purpose | `spdx3-validate` | Extension SHACL |
| --- | --- | --- | --- |
| [`documents/valid-minimal.spdx3.json`](documents/valid-minimal.spdx3.json) | Required property only; blank-node extension | pass | pass |
| [`documents/valid-full.spdx3.json`](documents/valid-full.spdx3.json) | All properties, reference to an `ai_AIPackage`, a second extension (`CdxPropertiesExtension`) on the same Element, plus a core `generates` Relationship | pass | pass |
| [`documents/valid-iri-node.spdx3.json`](documents/valid-iri-node.spdx3.json) | Extension node identified by an IRI instead of a blank node | pass | pass |
| [`documents/valid-ext-invalid.spdx3.json`](documents/valid-ext-invalid.spdx3.json) | Valid SPDX that breaks the extension: no `generationMethod`, `syntheticFraction` 1.5, `generatorModel` pointing at a Person | **pass** | fail (3 violations) |
| [`known-issues/profile-conformance-extension.spdx3.json`](known-issues/profile-conformance-extension.spdx3.json) | Declares `profileConformance: "extension"` | **fail** | n/a |
| [`known-issues/plain-scalar-values.spdx3.json`](known-issues/plain-scalar-values.spdx3.json) | Extension values written as plain JSON strings and numbers | pass | fail (6 violations) |

### How to validate

```bash
spdx3-validate -s 3.0.1 -j documents/valid-full.spdx3.json
```

```bash
pyshacl -s synthetic-data.ttl -e synthetic-data.ttl -df json-ld documents/valid-full.spdx3.json
```

`spdx3-validate` checks the document against the SPDX model only. It never
loads `synthetic-data.ttl`, so extension constraints have to be checked
separately (second command).

## Tool support matrix

Tested 2026-10-23.

| Tool | Version | Reads custom extension | Writes it back | Notes |
| --- | --- | --- | --- | --- |
| spdx3-validate | 0.0.7 | yes | n/a | Accepts any `type` IRI. Does not and cannot check extension constraints. |
| spdx-python-model, `v3_0_1` bindings | `3d24398` (source) | yes | **no** for `{"@id"}` / `{"@value"}` values | Serializer raises `TypeError: Unsupported serialized type <class 'dict'>`. Plain scalars round-trip, but a JSON number comes back as a string (`0.35` becomes `"0.35"`). The `v3_1` bindings share the same code. |
| spdx-tools-java | | not tested | | |
| SPDX Online Tools | | not tested | | |
| Pitloom (`loom fragment validate`) | | not tested | | |

## Findings

Flaws found with this example are recorded, with repros and proposed fixes,
in [examples/FINDINGS.md](../../FINDINGS.md):

- S-1: `profileConformance: "extension"` expands to the `Core/extension`
  property, so no valid JSON document can claim the Extension profile.
  The same name collision also hits `createdBy` and `requirementUID` in 3.1-dev.
- S-2: extension values need JSON-LD value objects (`{"@id"}`, `{"@value"}`).
- M-1: no way to declare which extensions a document uses.
- M-2: extension objects cannot stand alone.
- M-3: SHACL for `extension` is a deny-list.
- T-1: spdx-python-model cannot write extension value objects.
- T-2: spdx3-validate cannot check extension constraints.
