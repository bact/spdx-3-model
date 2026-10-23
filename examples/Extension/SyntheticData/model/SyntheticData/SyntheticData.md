SPDX-License-Identifier: Community-Spec-1.0

# SyntheticData

## Summary

Example SPDX 3 extension describing how the content of a dataset was
generated.

## Description

This namespace is an example of an SPDX 3 extension defined outside of the
SPDX specification. It is written in the same Markdown format as the SPDX 3
model, so that it could be submitted as a candidate addition to SPDX
(see "Support structured capture of expressive solutions for gaps in SPDX
coverage" in `/Extension/Extension`).

Datasets used to train or evaluate AI models are increasingly produced, in
whole or in part, by other AI models (synthetic data, distillation). Knowing
this matters for model quality (model collapse), for evaluation integrity, and
for compliance with the terms of use of the generating model. SPDX 3.0 can
express that an AI package `generates` a dataset, but cannot characterize the
dataset itself as human-generated, machine-generated, or mixed, nor how much
of it is synthetic.

## Metadata

- id: https://example.org/spdx3-ext/synthetic-data/
- name: SyntheticData
