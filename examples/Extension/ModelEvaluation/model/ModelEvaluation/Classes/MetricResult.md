SPDX-License-Identifier: Community-Spec-1.0

# MetricResult

## Summary

The value of one metric measured in an evaluation.

## Description

A MetricResult is a structured value inside an EvaluationExtension. It is not
an Extension and not an Element: it has no identity of its own and is not
used outside an EvaluationExtension.

## Metadata

- name: MetricResult
- SubclassOf: none
- Instantiability: Concrete

## Properties

- metricName
  - type: xsd:string
  - minCount: 1
  - maxCount: 1
- metricValue
  - type: xsd:decimal
  - minCount: 1
  - maxCount: 1
