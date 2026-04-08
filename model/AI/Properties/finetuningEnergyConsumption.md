SPDX-License-Identifier: Community-Spec-1.0

# finetuningEnergyConsumption

## Summary

Energy consumed when finetuning the AI model that is
being used in the AI system.

**DEPRECATED in SPDX 3.1.**
Use `/Core/energyConsumption` with `lifecycleScope` set to `update`.

## Description

The field specifies the amount of energy consumed when finetuning the AI model
that is being used in the AI system.

This property is deprecated.
Migrate to `/Core/energyConsumption` and set `lifecycleScope` appropriately.

## Metadata

- name: finetuningEnergyConsumption
- Nature: ObjectProperty
- Range: EnergyConsumptionDescription
