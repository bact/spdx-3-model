SPDX-License-Identifier: Community-Spec-1.0

# Energy consumption migration guidance

## Purpose

This note describes how to migrate AI-scoped energy consumption data to the
new Core representation introduced in SPDX 3.1.

## Mapping summary

- AI old structure:

  - `ai_energyQuantity` (numeric) and `ai_energyUnit` (token from
    `ai:EnergyUnitType`) stored in `ai_EnergyConsumptionDescription`.
  - Stage-specific properties: `ai_trainingEnergyConsumption`,
    `ai_inferenceEnergyConsumption`, `ai_finetuningEnergyConsumption`.

- New Core structure:

  - `/Core/energyConsumption` : range `/Core/EnergyConsumption`.
  - `/Core/EnergyConsumption.measure` : type `/Core/MeasureOfEnergy`.
    - `measure.quantity` (xsd:decimal) ← `ai_energyQuantity`.
    - `measure.unitQUDT` (QUDT URI) ← map from `ai_energyUnit` token.
  - `/Core/EnergyConsumption.lifecycleScope` : `/Core/LifecycleScopeType`
    (optional) — use to indicate training, runtime/inference, finetuning, etc.

## Lifecycle scope mapping (recommendation)

- `ai_trainingEnergyConsumption` → `lifecycleScope=training`.
- `ai_inferenceEnergyConsumption` → `lifecycleScope=runtime` (or add
  `inference` to `LifecycleScopeType` if exact naming preferred).
- `ai_finetuningEnergyConsumption` → `lifecycleScope=update` (or add
  `finetuning` to `LifecycleScopeType`).

If preserving exact original stage names is required for round-tripping,
consider extending `/Core/LifecycleScopeType` with `training`, `inference`,
`finetuning` entries.

## Unit mapping examples

Recommended QUDT URIs for common AI energy units:

- `kilowattHour` → `http://qudt.org/vocab/unit/KiloWattHour`
- `megajoule` → `http://qudt.org/vocab/unit/MegaJoule`

If the AI token is `other`, record a concrete QUDT URI in
`measure.unitQUDT` or include a textual note in
`/Core/EnergyConsumption.description`.

## Example conversion

See `serialization/jsonld/examples/ai-energy-migration.jsonld` for a
before/after JSON-LD example.

## Notes

- The Core representation intentionally groups `measure` and
  `lifecycleScope` in a small class to make the association explicit and to
  allow multiple, stage-specific measurements on the same element.
- Tooling migrating old AI data should perform unit-token → QUDT mapping and
  set `lifecycleScope` according to the mapping above.
