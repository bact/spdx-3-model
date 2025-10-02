SPDX-License-Identifier: Community-Spec-1.0

# hasRAGContext

## Summary

Indicates whether the prompt includes externally retrieved context intended to
ground the model's response in specific facts or knowledge.

`true` if the prompt includes the context, `false` otherwise.

## Description

Specifies whether the Retrieval-Augmented Generation (RAG) technique is
employed during prompt construction. This technique is commonly used to improve
the accuracy and relevance of responses from foundational models by providing
them with up-to-date or domain-specific information.

Allowed values:

- `true`: The prompt includes externally retrieved content.
- `false`: The prompt is constructed directly without retrieval augmentation.

## Metadata

- name: hasRAGContext
- Nature: DataProperty
- Range: xsd:boolean
