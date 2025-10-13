SPDX-License-Identifier: Community-Spec-1.0

# DatasetType

## Summary

Enumeration of dataset types.

## Description

Describes the different structures or kinds of data within a given dataset.

A dataset can have multiple data types.
Even a single data point can have multiple data types.
For example, a labeled image could also be considered categorical.

## Metadata

- name: DatasetType

## Entries

- audio: Audio-based data. If known, use the more specific audioNonSpeech or audioSpeech.
- audioNonSpeech: Non-speech sounds (e.g., music, environmental sounds, audio alerts).
- audioSpeech: Spoken language captured as audio data (e.g., voice commands, recorded dialogue).
- categorical: Data classified into a discrete number of categories (e.g., car models).
- code: A sequence of characters governed by formal rules, intended for instructing a machine or defining a data structure.
- geometry2d: Two-dimensional spatial data (e.g., floor plans, maps, blueprints).
- geometry3d: Three-dimensional data (e.g., point clouds, meshes, CAD models).
- graph: Data in the form of a graph where entries are related to each other through edges (e.g., social networks).
- image: Still images (e.g., pictures of animals, paintings).
- noAssertion: The data type is not known or cannot be reasonably determined, or the creator has made no attempt to determine this field, or the creator has intentionally provided no information (no meaning should be implied by doing so).
- numeric: Data consisting only of numeric entries.
- other: Data of a type not included in this list.
- sensor: Data recorded from a physical sensor (e.g., thermometer readings).
- structured: Data stored in a tabular format or retrieved from a relational database.
- syntactic: Data that describes the syntax or semantics of a language or text (e.g., parse trees).
- text: Unstructured text data (e.g., books, Wikipedia articles, transcripts).
- timeseries: Data ordered by time (e.g., stock prices, time sheets).
- timestamp: Data where each entry is recorded with a timestamp, but not necessarily ordered or at specific intervals.
- video: Video-based data (e.g., movie clips).
