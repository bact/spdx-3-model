SPDX-License-Identifier: Community-Spec-1.0

# DeliverableFacts

## Summary

A deliverable is a part of a product. The deliverable facts shall collect metadata that typically cannot be derived from the repository content.

## Description

The deliverable facts are collected and update in all deliverable lifecycle phases. So data could already collected in the architecture/design phase and then be updated along the furter development. The data might be needed to take design decisions and configure the environment. By having the structured explicit documentation, unnecessary iterations may be avoided.

## Metadata

- name: DeliverableFacts
- SubclassOf: tbd
- Instantiability: Concrete

## Properties

- programmingLanguage
  - type: programmingLanguageType
  - minCount: 1
  - maxCount: n

- dependencyManager
  - type: dependencyManagerType
  - minCount: 1
  - maxCount: n

- packageManager
  - type: packageManagerType
  - minCount: 1
  - maxCount: n

- environmentFramework
  - type: environmentFrameworkType
  - minCount: 1
  - maxCount: n

- applicationCategory
  - type: applicationCategoryType
  - minCount: 1
  - maxCount: 1

- applicationType
  - type: applicationTypeType
  - minCount: 1
  - maxCount: 1

- distributionMethod
  - type: distributionMethodType
  - minCount: 1
  - maxCount: n

- operatingSystem
  - type: operatingSystemType
  - minCount: 1
  - maxCount: 1
- consistsOf
  - type: Artifact
  - minCount: 1

- developedBy
  - type: Agent
  - minCount: 1
  - maxCount: n

- contact
  - type: Agent
  - minCount: 1
  - maxCount: n

- linkToArchitecture
  - type: xsd:anyURI
  - minCount: 1
  - maxCount: 1

- osmConcept
  - type: xsd:anyURI
  - minCount: 1
  - maxCount: 1

- fossComplianceBundleStorage
  - type: fossComplianceBundleStorageType
  - minCount: 1
  - maxCount: 1

- reviews
  - type: xsd:anyURI
  - minCount: 1
  - maxCount: n

- comment
  - type: xsd:string
  - maxCount: 1

- supplierDeliverableFacts
  - type: Delivery
  - minCount: 0
  - maxCount: n
