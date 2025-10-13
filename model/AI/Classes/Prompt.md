SPDX-License-Identifier: Community-Spec-1.0

# Prompt

## Summary

Specifies a prompt content and its associated information.

## Description

Specifies a prompt content and its associated information.

A prompt is the input text or instruction given to an AI model to initiate and
guide its generated output.

The `contentIdentifier` property identifies the prompt's content(s).

When `isContextAugmented` is set to `true`, a Relationship of type `usesTool`
can be optionally used to describe the augmentation mechanism or tool employed.
For example, referencing a Retrieval-Augmented Generation tool.

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
- promptPattern
  - type: xsd:string
  - minCount: 0

## External properties restrictions

- /Software/SoftwareArtifact/contentIdentifier
  - type: /Software/ContentIdentifier
  - minCount: 1
