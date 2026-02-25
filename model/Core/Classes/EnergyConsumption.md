SPDX-License-Identifier: Community-Spec-1.0

# EnergyConsumption

## Summary

Core class describing energy consumption for an element and its lifecycle
context.

## Description

This class records an energy measurement together with an optional lifecycle
scope to indicate the phase (for example manufacturing, training, runtime,
transport). The `measure` property uses `/Core/MeasureOfEnergy` (which in turn
uses `quantity` and `unitQUDT`).

## Metadata

- name: EnergyConsumption
- Instantiability: Concrete

## Properties

- measure
  - type: /Core/MeasureOfEnergy
  - minCount: 1
  - maxCount: 1
- lifecycleScope
  - type: /Core/LifecycleScopeType
  - minCount: 0
  - maxCount: 1
- description
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- measurementMethod
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
