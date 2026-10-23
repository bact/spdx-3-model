SPDX-License-Identifier: Community-Spec-1.0

# ModelEvaluation

## Summary

Example SPDX 3 extension recording the results of evaluating an AI model on a
test dataset.

## Description

This namespace is an example of an SPDX 3 extension defined outside of the
SPDX specification, written in the same Markdown format as the SPDX 3 model.

SPDX 3.0 can say that an AI model was tested on a dataset (a `testedOn`
Relationship), and can record metrics of the model (`/AI/AIPackage`
`metric`). It has no structured way to say which metric value was measured on
which test dataset, or to keep the results of several evaluation runs apart.
This extension attaches the results to the `testedOn` Relationship itself.

## Metadata

- id: https://example.org/spdx3-ext/model-evaluation
- name: ModelEvaluation
