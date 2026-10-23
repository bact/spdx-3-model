SPDX-License-Identifier: Community-Spec-1.0

# EvaluationExtension

## Summary

Results of one evaluation of an AI model on the dataset(s) of a `testedOn`
Relationship.

## Description

An EvaluationExtension is attached to a `/Core/Relationship` of type
`testedOn`, from an `/AI/AIPackage` to one or more `/Dataset/DatasetPackage`,
using `/Core/extension`. It holds the metrics measured in one evaluation run.

A Relationship may have more than one EvaluationExtension, one for each
evaluation run. Each one is a separate run: consumers should not merge their
results.

## Metadata

- name: EvaluationExtension
- SubclassOf: /Extension/Extension
- Instantiability: Concrete

## Properties

- metricResult
  - type: MetricResult
  - minCount: 1
