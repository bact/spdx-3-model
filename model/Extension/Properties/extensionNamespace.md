SPDX-License-Identifier: Community-Spec-1.0

# extensionNamespace

## Summary

Identifies the namespace of the terms defined by an extension.

## Description

The IRI that the classes and properties of an extension start with, for
example `https://example.org/spdx3-ext/synthetic-data/`.

An Extension in the document whose type IRI starts with this namespace is
defined by the ExtensionDefinition that has this extensionNamespace.

## Metadata

- name: extensionNamespace
- Nature: DataProperty
- Range: xsd:anyURI
