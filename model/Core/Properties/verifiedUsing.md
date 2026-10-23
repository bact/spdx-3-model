SPDX-License-Identifier: Community-Spec-1.0

# verifiedUsing

## Summary

Provides an IntegrityMethod with which the integrity of an Element, or of
another resource, can be asserted.

## Description

A verifiedUsing provides an IntegrityMethod with which the integrity of an
Element can be asserted. When used in an ExternalMap or an
ExtensionDefinition, it asserts the integrity of the external Element or of
the extension definition.

Please note that different profiles may also provide additional methods for
verifying the integrity of specific subclasses of Elements.

## Metadata

- name: verifiedUsing
- Nature: ObjectProperty
- Range: IntegrityMethod
