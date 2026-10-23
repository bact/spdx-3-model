SPDX-License-Identifier: Community-Spec-1.0

# SyntheticDataExtension

## Summary

Describes how the content of a dataset was generated.

## Description

A SyntheticDataExtension characterizes the origin of the content of a
dataset: whether it was produced by humans, by a machine (synthetic data), or
both; what fraction of it is synthetic; and which AI model(s) produced the
synthetic part.

It is intended to be attached to a `/Dataset/DatasetPackage` using
`/Core/extension`.

## Metadata

- name: SyntheticDataExtension
- SubclassOf: /Extension/Extension
- Instantiability: Concrete

## Properties

- generationMethod
  - type: DataGenerationMethodType
  - minCount: 1
  - maxCount: 1
- syntheticFraction
  - type: xsd:decimal
  - minCount: 0
  - maxCount: 1
- generatorModel
  - type: /AI/AIPackage
  - minCount: 0
