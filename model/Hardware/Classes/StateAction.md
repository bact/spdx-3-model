SPDX-License-Identifier: Community-Spec-1.0

# StateAction

## Summary

This is the state of an affected element.

## Description

The state of a specific element is defined in this class. The state of an object refers to the set of attributes, properties, or data that define the object's condition at a specific moment in time.

## Metadata

- name: StateAction
- SubclassOf: UseAction
- Instantiability: Concrete

## Properties

- objectState
  - type: xsd:string
  - minCount: 1
  - maxCount: 1

## External properties restrictions

- /Core/Element/description
  - minCount: 1
