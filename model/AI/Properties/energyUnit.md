SPDX-License-Identifier: Community-Spec-1.0

# energyUnit

## Summary

Unit in which energy is measured.

**DEPRECATED in SPDX 3.1.**
Use `/Core/MeasureOfEnergy.unitQUDT` instead.

## Description

Provides the unit information of the energy.

This AI-scoped property referenced an `EnergyUnitType` token. Migrate to
QUDT `unitQUDT` values in `/Core/MeasureOfEnergy.unitQUDT`. If the AI token is
`other`, record a concrete QUDT URI or provide a textual note in
`/Core/EnergyConsumption.description`.

## Metadata

- name: energyUnit
- Nature: ObjectProperty
- Range: EnergyUnitType
