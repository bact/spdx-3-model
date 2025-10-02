SPDX-License-Identifier: Community-Spec-1.0

# Prompt

## Summary

Specifies a prompt content and its associated information.

## Description

Specifies a prompt content and its associated information.

A prompt is the input or instruction given to a foundational model, including
a language model, to guide it in generating a specific response or action.

## Metadata

- name: Prompt
- SubclassOf: /Software/SoftwareArtifact
- Instantiability: Concrete

## Properties

- /Core/inLanguage
  - type: /Core/LanguageTag
  - minCount: 0
- /Dataset/dataCollectionProcess
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- /Dataset/dataCollectionProcess
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- hasRAGContext
  - type: xsd:boolean
  - minCount: 0
  - maxCount: 1
- hasInputOutputExample
  - type: xsd:boolean
  - minCount: 0
  - maxCount: 1
- hasSensitivePersonalInformation
  - type: /Core/PresenceType
  - minCount: 0
  - maxCount: 1
- modality
  - type: /Core/Modality
  - minCount: 0
