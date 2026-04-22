SPDX-License-Identifier: Community-Spec-1.0

# itemCount

## Summary

Number of discrete items in a software artifact.

## Description

itemCount records the number of discrete items in a software artifact,
such as images, records, data samples, or files.

Items need not correspond to individual files.
They may be stored in a database, embedded in a container format,
or represented as encoded binaries within a single file.

The unit of count (e.g., images, records, files) is not encoded in this
property. If the unit is not apparent from context, it shall be noted in
the `description` property of the element.

## Metadata

- name: itemCount
- Nature: DataProperty
- Range: xsd:nonNegativeInteger
