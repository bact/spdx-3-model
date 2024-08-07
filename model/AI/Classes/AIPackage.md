SPDX-License-Identifier: Community-Spec-1.0

# AIPackage

## Summary

Specifies an AI package and its associated information.

## Description

Metadata information that can be added to a package to describe an AI application or trained AI model.

## Metadata

- name: AIPackage
- SubclassOf: /Software/Package
- Instantiability: Concrete

## Properties

- autonomyType
  - type: /Core/PresenceType
  - minCount: 0
  - maxCount: 1
- domain
  - type: xsd:string
  - minCount: 0
- energyConsumption
  - type: EnergyConsumption
  - minCount: 0
  - maxCount: 1
- hyperparameter
  - type: /Core/DictionaryEntry
  - minCount: 0
- informationAboutApplication
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- informationAboutTraining
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- limitation
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- metric
  - type: /Core/DictionaryEntry
  - minCount: 0
- metricDecisionThreshold
  - type: /Core/DictionaryEntry
  - minCount: 0
- modelDataPreprocessing
  - type: xsd:string
  - minCount: 0
- modelExplainability
  - type: xsd:string
  - minCount: 0
- safetyRiskAssessment
  - type: SafetyRiskAssessmentType
  - minCount: 0
  - maxCount: 1
- standardCompliance
  - type: xsd:string
  - minCount: 0
- typeOfModel
  - type: xsd:string
  - minCount: 0
- useSensitivePersonalInformation
  - type: /Core/PresenceType
  - minCount: 0
  - maxCount: 1

## External properties restrictions

- /Core/Artifact/releaseTime
  - minCount: 1
- /Core/Artifact/suppliedBy
  - minCount: 1
- /Software/Package/downloadLocation
  - minCount: 1
- /Software/Package/packageVersion
  - minCount: 1
- /Software/SoftwareArtifact/primaryPurpose
  - minCount: 1
