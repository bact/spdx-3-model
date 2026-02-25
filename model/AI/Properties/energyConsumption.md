SPDX-License-Identifier: Community-Spec-1.0

# energyConsumption

## Summary

Energy consumption incurred by an AI model.

**DEPRECATED in SPDX 3.1.** Use `/Core/energyConsumption` instead.

## Description

Energy consumption of an AI model, either known or estimated.

In the absence of direct measurements, an SPDX data creator may choose to
estimate the energy consumption based on information about computational
resources (e.g., number of floating-point operations), training time, and other
relevant training details.

This AI-scoped property is deprecated. Authors should use the Core
`/Core/energyConsumption` property which supports `MeasureOfEnergy` and an
optional `lifecycleScope` for phase-specific measurements.

## Metadata

- name: energyConsumption
- Nature: ObjectProperty
- Range: EnergyConsumption
