SPDX-License-Identifier: Community-Spec-1.0

# finetuningEnergyConsumption

## Summary

Energy consumed when finetuning the AI model that is being used in the AI system.

**DEPRECATED in SPDX 3.1.** Use `/Core/energyConsumption` with `lifecycleScope`
set to `update` or `finetuning` (if `finetuning` is added to
`/Core/LifecycleScopeType`).

## Description

The field specifies the amount of energy consumed when finetuning the AI model
that is being used in the AI system.

This AI-scoped property is deprecated. Migrate entries to `/Core/energyConsumption`
and set `lifecycleScope` appropriately.

## Metadata

- name: finetuningEnergyConsumption
- Nature: ObjectProperty
- Range: EnergyConsumptionDescription
