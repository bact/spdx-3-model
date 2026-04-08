SPDX-License-Identifier: Community-Spec-1.0

# EnergyConsumption

## Summary

Core class describing energy consumption for an element and its lifecycle
context.

## Description

This class records an energy measurement together with an optional lifecycle
scope to indicate the phase (for example manufacturing, training, runtime,
transport).

The `measure` property shall hold an `/Core/UnitOfMeasure` object
with the object's `unitQUDT` property be one of the energy units.

## Metadata

- name: EnergyConsumption
- Instantiability: Concrete

## Properties

- description
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- lifecycleScope
  - type: /Core/LifecycleScopeType
  - minCount: 0
  - maxCount: 1
- measure
  - type: /Core/UnitOfMeasure
  - minCount: 1
  - maxCount: 1
- measurementCertainty
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- measurementMethod
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
