SPDX-License-Identifier: Community-Spec-1.0

# CreateAction

## Summary

Products are created using the Creation Action.

## Description

To create a product you use the Creation Action.

Relationship:

For each `CreateAction` there is at least one `/Core/Relationship` class or subclass with the relationshipType of 'hasOutput’ on the from and a `/Core/Element` class or subclass on the to.

## Metadata

- name: CreateAction
- SubclassOf: /Core/Action
- Instantiability: Abstract

## External properties restrictions

- /Core/Action/actionStartTime
  - minCount: 1
