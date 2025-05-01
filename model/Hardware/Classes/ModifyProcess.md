SPDX-License-Identifier: Community-Spec-1.0

# ModifyProcess

## Summary

Modify process changes, transports or stores a product.

## Description

Modify processes interact with a product based on a need such as transport, change or storage. Specific attributes are associated with Modify Classes to track relevant information related to product interactions.

Relationship:

For each `ModifyProcess` there is at least one `/Core/Relationship` class or subclass with the relationshipType of 'hasOutput’ on the from and a `/Core/Element` class or subclass on the to.

For each `ModifyProcess` there is at least one `/Core/Relationship` class or subclass with the relationshipType of 'hasInput’ on the from and a `/Core/Element` class or subclass on the to.

## Metadata

- name: ModifyProcess
- SubclassOf: /Core/DefinedProcess
- Instantiability: Abstract

## External properties restrictions

- /Core/Element/description
  - minCount: 1
