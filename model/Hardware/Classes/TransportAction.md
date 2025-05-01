SPDX-License-Identifier: Community-Spec-1.0

# TransportAction

## Summary

The action of product transport.

## Description

Transporting refers to the act of moving people, goods, information, or substances from one location to another.

## Metadata

- name: TransportAction
- SubclassOf: ModifyAction
- Instantiability: Concrete

## Properties

- transportRoute
  - type: xsd:string
  - minCount: 0
- pickupLocation
  - type: /Core/Location
  - minCount: 1
- dropoffLocation
  - type: /Core/Location
  - minCount: 0
