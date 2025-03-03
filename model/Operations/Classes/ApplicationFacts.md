SPDX-License-Identifier: Community-Spec-1.0

# ApplicationFacts

## Summary

The Application facts summarize the business context metadata of an application. An application may consist of one to n deliverables.

## Description

The Application Facts are collected all along the product lifecyle and contents may be updated when the product reaches a new phase.

## Metadata

- name: ApplicationFacts
- SubclassOf: tbd
- Instantiability: Concrete

## Properties

- productOwner
  - type: /Core/Person
  - minCount: 0
  - maxCount: 1
- documentationLink
  - type: xsd:anyURI
  - minCount: 1
  - maxCount: 1
- productAccessURL
  - type: xsd:anyURI
  - maxCount: 1
- commentComment
  - type: xsd:string
  - maxCount: 1
- distributedDeliverables
  - type: Artifact
  - minCount: 1
  - maxCount: n
- technicalDeploymnent
  - type: deploymentType
  - minCount: 1
  - maxCount: 1
- contact
  - type: Agent
  - minCount: 1
  - maxCount: 1
- scope
  - type: scopeType
  - minCount: 1
  - maxCount: 1
- relationType
  - type: relationTypeType
  - minCount: 1
  - maxCount: 1
- supplyChainContext
  - type: supplyChainContextType
  - minCount: 1
  - maxCount: 1
- releaseCycles
  - type: releaseCyclesType
  - minCount: 1
  - maxCount: 1
- fossComplianceBundleProvision
  - type: fossComplianceBundleProvisionType
  - minCount: 1
  - maxCount: 1
- contractSetup
  - type: contractSetupType
  - minCount: 1
  - maxCount: 1
- fossTermsTowardsCustomer
  - type: Artifact
  - maxCount: 1
- distributionTermsTowardsCustomer
  - type: Artifact
  - maxCount: 1
- customerFossContact
  - type: Agent
  - maxCount: 1
