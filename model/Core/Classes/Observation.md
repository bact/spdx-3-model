SPDX-License-Identifier: Community-Spec-1.0

# Observation

## Summary

An act of carrying out a procedure to measure, estimate, or calculate
the value of a property of an Element.

## Description

The `Observation` class models the temporal event of quantifying a metric.

The entity being measured (the feature of interest) is linked to the
`Observation` via incoming relationships of type "hasInput".

The quantitative output of the measurement is captured via the `hasResult`
property.

## Metadata

- name: Observation
- SubclassOf: Action
- Instantiability: Concrete

## Properties

- marginOfError
  - type: xsd:string
  - minCount: 0
- observationType
  - type: ObservationType
  - minCount: 0
- observedProperty
  - type: anyURI
  - minCount: 1
  - maxCount: 1
- observedValue
  - type: UnitOfMeasure
  - minCount: 1
  - maxCount: 1
