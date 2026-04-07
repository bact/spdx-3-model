SPDX-License-Identifier: Community-Spec-1.0

# EnergyConsumptionDescription

## Summary

The class that helps note down the quantity of energy consumption and the unit
used for measurement.

**DEPRECATED in SPDX 3.1.**
Use `/Core/EnergyConsumption` instead.

## Description

This class is designed to store energy consumption data, including the quantity
and the unit of measurement.

The `energyQuantity` property stores the amount of energy consumed,
and the `energyUnit` property stores the unit used for measurement.

For example, 0.042 kilowatt-hour of energy will have `0.042` as a value for
property `energyQuantity`, and `"kilowattHour"` as a value for property
`energyUnit`.

*Migration guidance*

Migrate instances to `/Core/energyConsumption` by placing the numeric value in
`measure.quantity` and mapping the unit token to a QUDT `unitQUDT` value.
If the AI token is `other`, record a concrete QUDT URI or include a note in
`/Core/EnergyConsumption.description`.

*Example (migrated)*

```json
{
  "type": "EnergyConsumption",
  "measure": {
    "type": "MeasureOfEnergy",
    "quantity": "0.042",
    "unitQUDT": "http://qudt.org/vocab/unit/KiloWattHour"
  },
  "lifecycleScope": "runtime"
}
```

## Metadata

- name: EnergyConsumptionDescription
- Instantiability: Concrete

## Properties

- energyQuantity
  - type: xsd:decimal
  - minCount: 1
  - maxCount: 1
- energyUnit
  - type: EnergyUnitType
  - minCount: 1
  - maxCount: 1
