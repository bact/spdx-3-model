SPDX-License-Identifier: Community-Spec-1.0

# reasoningtPattern

## Summary

Identifies the structured reasoning strategy used within a prompt to guide
a foundation model toward a desired output.

## Description

A free-form text describing the structured strategy or thinking process the foundation model (e.g., a large language model) is intended to follow.

This strategy defines the specific technique used to enhance the model's problem-solving effectiveness (e.g., sequential steps, branching exploration, or consensus checking).

Examples of possible values:

- `simple`: Direct instructions; no explicit multi-step reasoning required.
- `chain-of-thought`: Explicit, sequential, step-by-step reasoning.
- `tree-of-thought`: Explores and evaluates multiple branching reasoning paths.
- `self-consistency`: Generates multiple paths and selects the consensual answer.
- `checklists` - Uses a structured list of criteria to ensure completeness.

## Metadata

- name: reasoningtPattern
- Nature: DataProperty
- Range: xsd:string
