SPDX-License-Identifier: Community-Spec-1.0

# ActionEventData

## Summary

Action event data refers to the additional information captured when an action event occurs.

## Description

Action event data refers to the additional information captured when an action event occurs. It can include details about the event, what happened, when it happened, and what data was involved.

Relationship:

For each `ActionEventData` there is only one `/Core/Relationship` class or subclass with the relationshipType of 'contains’ on the to and a `/Core/Action` class or subclass on the from.

## Metadata

- name: ActionEventData
- SubclassOf: /Core/Artifact
- Instantiability: Concrete

## Properties

- userData
  - type: xsd:string
  - minCount: 0
