SPDX-License-Identifier: Community-Spec-1.0

# energyQuantity

## Summary

Energy quantity.

**DEPRECATED in SPDX 3.1.**
Use `/Core/MeasureOfEnergy` (property `quantity`) instead.

## Description

Provides the quantity information of the energy.

This AI-scoped data property is deprecated. When migrating, place the numeric
value into `/Core/MeasureOfEnergy.quantity` and use `/Core/MeasureOfEnergy.unitQUDT`
for the corresponding unit.

## Metadata

- name: energyQuantity
- Nature: DataProperty
- Range: xsd:decimal
