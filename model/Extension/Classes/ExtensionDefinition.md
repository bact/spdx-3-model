SPDX-License-Identifier: Community-Spec-1.0

# ExtensionDefinition

## Summary

Identifies the definition of an extension used in an SpdxDocument.

## Description

An ExtensionDefinition declares that an SpdxDocument uses classes and
properties from an extension, identifies the extension by the IRI of its
namespace, and optionally tells where to retrieve the definition of the
extension (for example an OWL ontology and SHACL shapes) and how to verify its
integrity.

Consumers can use this information to discover the extensions a document
relies on without inspecting every Element. Validators can retrieve the
definition, verify it, and check the extension data in the document against
it, in addition to the SPDX model.

The definition is a single resource, for example one Turtle file with the
OWL ontology and the SHACL shapes of the extension. `locationHint` tells
where to retrieve it, and `verifiedUsing` applies to the exact bytes
retrieved from `locationHint`, so that a consumer can check that it has the
definition the document was written against.

## Metadata

- name: ExtensionDefinition
- SubclassOf: none
- Instantiability: Concrete

## Properties

- extensionNamespace
  - type: NamespaceIri
  - minCount: 1
  - maxCount: 1
- /Core/locationHint
  - type: xsd:anyURI
  - maxCount: 1
- /Core/verifiedUsing
  - type: /Core/IntegrityMethod
