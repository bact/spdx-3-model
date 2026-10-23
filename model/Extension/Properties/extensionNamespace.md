SPDX-License-Identifier: Community-Spec-1.0

# extensionNamespace

## Summary

Identifies the namespace of the terms defined by an extension.

## Description

The namespace IRI of the classes and properties of an extension, for example
`https://example.org/spdx3-ext/synthetic-data/`. It ends with `/` or `#`.

A class or property IRI in the document that starts with this IRI is defined
by the ExtensionDefinition that has this extensionNamespace. When namespaces
nest, the longest matching extensionNamespace applies. An extension whose
terms are in more than one namespace needs one ExtensionDefinition for each
namespace. An SpdxDocument should not have two ExtensionDefinitions with the
same extensionNamespace.

## Metadata

- name: extensionNamespace
- Nature: DataProperty
- Range: NamespaceIri
