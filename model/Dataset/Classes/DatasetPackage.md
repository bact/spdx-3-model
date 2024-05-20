SPDX-License-Identifier: Community-Spec-1.0

# DatasetPackage

## Summary

Specifies a data package and its associated information.

## Description

Metadata information that can be added to a dataset that may be used in a
software or to train/test an AI package.

**Syntax**

```json
{
  "@type": "DatasetPackage",
  "@id": "urn:spdx.dev:dspkg-1",
  "builtTime": "2024-04-24T11:22:05Z",
  "originatedBy": "",
  "releaseTime": "2024-05-18T14:53:12Z",
  "software_downloadLocation": "",
  "software_primaryPurpose": "Carbon dioxide levels in the atmosphere",
  "dataset_anonymizationMethodUsed": "",
  "dataset_confidentialityLevel": "amber",
  "dataset_dataCollectionProcess": "",
  "dataset_dataPreprocessing": "",
  "dataset_datasetAvailability": "",
  "dataset_datasetNoise": "",
  "dataset_datasetSize": "128000",
  "dataset_datasetType": "sensor",
  "dataset_datasetType": "structured",
  "dataset_datasetUpdateMechanism": "",
  "dataset_hasSensitivePersonalInformation": "no",
  "dataset_intendedUse": "",
  "dataset_knownBias": "",
  "dataset_sensor": {
    "co2_sensor": "K30 (030-8-0006)"
  }
}
```

## Metadata

- name: DatasetPackage
- SubclassOf: /Software/Package
- Instantiability: Concrete

## Properties

- anonymizationMethodUsed
  - type: xsd:string
  - minCount: 0
- confidentialityLevel
  - type: ConfidentialityLevelType
  - minCount: 0
  - maxCount: 1
- dataCollectionProcess
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- dataPreprocessing
  - type: xsd:string
  - minCount: 0
- datasetAvailability
  - type: DatasetAvailabilityType
  - minCount: 0
  - maxCount: 1
- datasetNoise
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- datasetSize
  - type: xsd:nonNegativeInteger
  - minCount: 0
  - maxCount: 1
- datasetType
  - type: DatasetType
  - minCount: 1
- datasetUpdateMechanism
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- hasSensitivePersonalInformation
  - type: /Core/PresenceType
  - minCount: 0
  - maxCount: 1
- intendedUse
  - type: xsd:string
  - minCount: 0
  - maxCount: 1
- knownBias
  - type: xsd:string
  - minCount: 0
- sensor
  - type: /Core/DictionaryEntry
  - minCount: 0

## External properties restrictions

- /Core/Artifact/builtTime
  - minCount: 1
  - maxCount: 1
- /Core/Artifact/originatedBy
  - minCount: 1
  - maxCount: 1
- /Core/Artifact/releaseTime
  - minCount: 1
  - maxCount: 1
- /Software/Package/downloadLocation
  - minCount: 1
  - maxCount: 1
- /Software/SoftwareArtifact/primaryPurpose
  - minCount: 1
  - maxCount: 1
