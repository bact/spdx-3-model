SPDX-License-Identifier: Community-Spec-1.0

# trainingEnergyConsumption

## Summary

Energy consumed when training the AI model that is being used in the AI system.

**DEPRECATED in SPDX 3.1.** Use `/Core/energyConsumption` with `lifecycleScope`
set to `training`.

## Description

The field specifies the amount of energy consumed when training the AI model
that is being used in the AI system.

This AI-scoped property is deprecated. Migrate entries to `/Core/energyConsumption`
and set `lifecycleScope` to `training` (or to an extended token if the
`LifecycleScopeType` vocabulary is updated).

## Metadata

- name: trainingEnergyConsumption
- Nature: ObjectProperty
- Range: EnergyConsumptionDescription
