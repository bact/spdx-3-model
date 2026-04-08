SPDX-License-Identifier: Community-Spec-1.0

# inferenceEnergyConsumption

## Summary

Energy consumed during inference time by an AI model
that is being used in the AI system.

**DEPRECATED in SPDX 3.1.** Use `/Core/energyConsumption` with `lifecycleScope`
set to `runtime` or `inference` (if `inference` is added to
`/Core/LifecycleScopeType`).

## Description

The field specifies the amount of energy consumed during inference time by an
AI model that is being used in the AI system.

This AI-scoped property is deprecated. Migrate entries to `/Core/energyConsumption`
and set `lifecycleScope` to the appropriate phase.

## Metadata

- name: inferenceEnergyConsumption
- Nature: ObjectProperty
- Range: EnergyConsumptionDescription
