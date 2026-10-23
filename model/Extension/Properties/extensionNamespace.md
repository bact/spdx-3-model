SPDX-License-Identifier: Community-Spec-1.0

# extensionNamespace

## Summary

Identifies the namespace of the terms defined by an extension.

## Description

The namespace IRI of the classes and properties of an extension, for example
`https://example.org/spdx3-ext/synthetic-data/`. It shall end with `/` or
`#`, so that it cannot be the start of an IRI in an unrelated namespace.

An Extension in the document whose type IRI is in this namespace (starts with
this IRI) is defined by the ExtensionDefinition that has this
extensionNamespace. An extension whose terms are in more than one namespace
needs one ExtensionDefinition for each namespace.

## Metadata

- name: extensionNamespace
- Nature: DataProperty
- Range: xsd:anyURI
