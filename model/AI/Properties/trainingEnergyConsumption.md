SPDX-License-Identifier: Community-Spec-1.0

# trainingEnergyConsumption

## Summary

Energy consumed when training the AI model that is
being used in the AI system.

**DEPRECATED in SPDX 3.1.**
Use `/Core/energyConsumption` instead.

## Description

The field specifies the amount of energy consumed when training the AI model
that is being used in the AI system.

This property is deprecated.
Migrate to `/Core/energyConsumption` and set `lifecycleScope` appropriately.

## Metadata

- name: trainingEnergyConsumption
- Nature: ObjectProperty
- Range: EnergyConsumptionDescription
