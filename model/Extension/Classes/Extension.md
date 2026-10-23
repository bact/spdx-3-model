SPDX-License-Identifier: Community-Spec-1.0

# Extension

## Summary

A characterization of some aspect of an Element that is associated with the Element in a generalized fashion.

## Description

An Extension is a characterization of some aspect of an Element that is associated with the Element in a generalized fashion.

Rather than being associated with a particular Element through the typical use of a purpose-specific object property an Extension is associated with the Element it characterizes using a single common generalized object property.

This approach serves multiple purposes:

1. Support profile-based extended characterization of Elements. Enables specification and expression of Element characterization extensions within any profile and namespace of SPDX without requiring changes to other profiles or namespaces and without requiring local subclassing of remote classes (which could inhibit ecosystem interoperability in some cases).

2. Support extension of SPDX by adopting individuals or communities with Element characterization details uniquely specialized to their particular context. Enables adopting individuals or communities to utilize SPDX expressive capabilities along with expressing more arcane Element characterization details specific to them and not appropriate for standardization across SPDX.

3. Support structured capture of expressive solutions for gaps in SPDX coverage from real-world use. Enables adopting individuals or communities to express Element characterization details they require that are not currently defined in SPDX but likely should be. Enables a practical pipeline that:

    - identifies gaps in SPDX that should be filled,
    - expresses solutions to those gaps in a way that allows the identifying adopters to use the extended solutions with SPDX and does not conflict with current SPDX,
    - can be clearly detected among the SPDX content exchange ecosystem,
    - provides a clear and structured definition of gap solution that can be used as submission for revision to SPDX standard

An Extension is not an Element. It has no `spdxId` and no `creationInfo` of
its own: it is a value of the `extension` property of exactly one Element, and
is attributed to that Element's `creationInfo`. An Extension instance should
be a blank node. The same Extension instance shall not be the value of the
`extension` property of more than one Element (the SPDX SHACL shapes do not
check this). To describe something that needs its own identity or
provenance, use an Element (for example an Annotation) instead.

An Element may have any number of extensions, including more than one
instance of the same Extension subclass. Each instance is a separate
characterization of the Element. The definition of an Extension subclass
should state whether more than one instance may be attached to the same
Element, and what that means.

Unless the definition of the Extension subclass says otherwise, consumers
should not merge instances of the same subclass on one Element.

A concrete Extension subclass defined outside of SPDX is identified by the
full IRI of its class, and its properties by their full IRIs.

## Metadata

- name: Extension
- Instantiability: Abstract
