SPDX-License-Identifier: Community-Spec-1.0

# SupplierDeliverableFacts

## Summary

Relevant metadata for a deliverable from a supplier used in own deliverable.

## Description

The supplier relation can vary according to the terms and conditions agreed between customer and supplier. Based on that some of the necessary metadata may be provided in different ways. The details may be described in the defined fields. For Open Source components the information may be derived from the Open Source license and context and thus this factsheet is only relevant in a commercial supplier-customer-relationship.

## Metadata

- name: SupplierDeliverableFacts
- SubclassOf: tbd
- Instantiability: Concrete

## Properties

- supplierName
  - type: Agent
  - minCount: 1
- deliverableFromSupplier
  - type: Artifact
  - minCount: 1
- fossTermsTowardsSupplier
  - type: Artifact
  - maxCount: 1
- distributionTermsFromSupplier
  - type: Artifact
  - maxCount: 1
- fossComplianceBundleConsumption
  - type: fossComplianceBundleProvisionType
  - minCount: 1
- supplierFossContact
  - type: Agent
  - minCount: 1