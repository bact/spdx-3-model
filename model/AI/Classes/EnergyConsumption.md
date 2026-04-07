SPDX-License-Identifier: Community-Spec-1.0

# EnergyConsumption

## Summary

A class for describing the energy consumption incurred by an AI model in
different stages of its lifecycle.

**DEPRECATED in SPDX 3.1.**
Use `/Core/EnergyConsumption` instead.

## Description

A class to denote the known or estimated energy consumption of an AI model
during its training, fine-tuning, and inference stages.

This class is deprecated.
Migrate to `/Core/EnergyConsumption` for each consumption measurement.

*Example*

```json
{
  "type": "EnergyConsumption",
  "measure": {
    "type": "MeasureOfEnergy",
    "quantity": "36.5",
    "unitQUDT": "http://qudt.org/vocab/unit/KiloWattHour"
  },
  "lifecycleScope": "training"
}
```

## Metadata

- name: EnergyConsumption
- Instantiability: Concrete

## Properties

- finetuningEnergyConsumption
  - type: EnergyConsumptionDescription
- inferenceEnergyConsumption
  - type: EnergyConsumptionDescription
- trainingEnergyConsumption
  - type: EnergyConsumptionDescription
