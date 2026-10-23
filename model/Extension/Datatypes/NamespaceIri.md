SPDX-License-Identifier: Community-Spec-1.0

# NamespaceIri

## Summary

An IRI that is a namespace: it ends with `/` or `#`.

## Description

A NamespaceIri is the common start of the IRIs of a set of terms. It ends
with `/` or `#`, so that it is not a prefix of a sibling namespace (for
example, `https://example.org/ext/` is not a prefix of
`https://example.org/ext-v2/`).

## Metadata

- name: NamespaceIri
- SubclassOf: xsd:anyURI

## Format

- pattern: ^.*[/#]$
