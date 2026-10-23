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

`locationHint` and `verifiedUsing` are used as in ExternalMap: where to
retrieve the definition, and how to verify that the retrieved definition is
the one the document was written against.

## Metadata

- name: ExtensionDefinition
- SubclassOf: none
- Instantiability: Concrete

## Properties

- extensionNamespace
  - type: xsd:anyURI
  - minCount: 1
  - maxCount: 1
- /Core/locationHint
  - type: xsd:anyURI
  - maxCount: 1
- /Core/verifiedUsing
  - type: /Core/IntegrityMethod
