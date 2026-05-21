SPDX-License-Identifier: Community-Spec-1.0

# additionalInformation

## Summary

Additional relevant information for an element when a standard property is
unavailable.

## Description

This property provides additional information to an element.
The additional information is structured as a key-value pair.
It is used to extend the element's description with domain-specific or
context-dependent information that is not explicitly covered by other standard
properties.

An `additionalInformationSpecificaiton` can be provided for the interpretation
of the key and/or its values.

*Usage guidance:*

This property is intended strictly for domain-specific, custom, or experimental
metadata that cannot be represented by any other standardized property within
the SPDX 3 specification.
Implementers should not use this property if an explicit, dedicated property
exists elsewhere in the specification to represent the target data.
Overuse of this property reduces semantic interoperability and should be
avoided.

## Metadata

- name: additionalInformation
- Nature: ObjectProperty
- Range: DictionaryEntry
