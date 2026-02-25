SPDX-License-Identifier: Community-Spec-1.0

# energyConsumption

## Summary

Core property to document energy consumption of an element or activity.

## Description

This property allows authors to record one or more energy consumption
measurements for an element (product, package, service, etc.). Each
consumption entry is represented by a `/Core/EnergyConsumption` instance
that pairs a `/Core/MeasureOfEnergy` with an optional `lifecycleScope` from
`/Core/LifecycleScopeType`.

`/Core/MeasureOfEnergy` uses `quantity` (numeric value) and `unitQUDT` (QUDT
unit identifier). When migrating from older AI-scoped properties, map the
existing `ai_energyQuantity` to `measure.quantity` and `ai_energyUnit` to
`measure.unitQUDT` (see migration guidance).

## Metadata

- name: energyConsumption
- Nature: ObjectProperty
- Range: /Core/EnergyConsumption
