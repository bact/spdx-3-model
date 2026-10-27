SPDX-License-Identifier: Community-Spec-1.0

# Annotation

## Summary

An assertion made in relation to an Element.

## Description

An Annotation is an assertion made in relation to an Element.
It records the view of its author (the annotator) about the Element,
for example the result of a review.

An Annotation is not for describing the characteristics of the Element itself.
Use the properties of the Element for that,
or an extension when no property fits.
To state how the Element relates to other Elements, use a Relationship.

The `contentType` property describes the format of the `statement` property.

## Metadata

- name: Annotation
- SubclassOf: Element
- Instantiability: Concrete

## Properties

- annotationType
  - type: AnnotationType
  - minCount: 1
  - maxCount: 1
- contentType
  - type: MediaType
  - minCount: 0
  - maxCount: 1
- statement
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- subject
  - type: Element
  - minCount: 1
  - maxCount: 1
