SPDX-License-Identifier: Community-Spec-1.0

# StateProcess

## Summary

This is the state of an affected element.

## Description

The state of a specific element is defined in this class. The state of an object refers to the set of attributes, properties, or data that define the object's condition at a specific moment in time.

Relationship:

For each `StateProcess` there is at least one `/Core/Relationship` class or subclass with the relationshipType of 'contains’ on the from and a `Requirement` class or subclass on the to.

## Metadata

- name: StateProcess
- SubclassOf: UseProcess
- Instantiability: Concrete
