SPDX-License-Identifier: Community-Spec-1.0

# Prompt

## Summary

Specifies the content of a prompt and its associated information.

## Description

Specifies the content of a prompt and its associated information.

A prompt is the input or instruction given to a foundation model, including
a language model, to guide it in generating a specific response or action.

The `contentIdentifier` property identifies the prompt's content(s).

## Metadata

- name: Prompt
- SubclassOf: /Software/SoftwareArtifact
- Instantiability: Concrete

## Properties

- /Core/inLanguage
  - type: /Core/LanguageTag
  - minCount: 0
- /Core/modality
  - type: /Core/Modality
  - minCount: 0
- /Dataset/dataCollectionProcess
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- /Dataset/dataPreprocessing
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- /Dataset/hasSensitivePersonalInformation
  - type: /Core/PresenceType
  - minCount: 0
  - maxCount: 1
- isContextAugmented
  - type: xsd:boolean
  - minCount: 0
  - maxCount: 1

## External properties restrictions

- /Software/SoftwareArtifact/contentIdentifier
  - type: /Software/ContentIdentifier
  - minCount: 1
