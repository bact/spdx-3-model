SPDX-License-Identifier: Community-Spec-1.0

# ModalityType

## Summary

A controlled vocabulary used to classify the nature of the data channel
(or sensory type) for content or interaction within a system.

## Description

The ModalityType defines a standardized classification for the distinct data
channels or sensory types through which information is communicated, perceived,
or processed by agents and software.

This vocabulary enables system components to describe the specific modality or
form in which information is exchanged, serving functions such as:

- Human-computer interaction (HCI): Defining the sensory channels for input and
  output.
- Foundation models: Specifying the nature of input data and the expected
  output.
- Data classification: Categorizing data and collections of data based on
  data's inherent form.

## Metadata

- name: ModalityType

## Entries

- audioSpeech: Spoken language captured as audio data (e.g., voice commands, recorded dialog).
- audioNonSpeech: Non-speech sound (e.g., music, environmental sounds, audio alerts).
- code: A sequence of characters governed by formal rules intended for instructing a machine or defining data structure.
- geometry2d: Two-dimensional spatial data (e.g., floor plans, maps, blueprints).
- geometry3d: Three-dimensional data (e.g., LiDAR scans, point clouds, meshes, CAD models).
- gesturePose: Human body movement, hand gestures, facial expressions, or full-body pose estimation.
- hapticTactile: Touch, force, or tactile feedback data (e.g., vibrations, surface pressure, grip data).
- image: Still visual data (e.g., photographs, drawings, diagrams, charts).
- other: Any other modality not defined in this list.
- tabular: Structured data in rows and columns (e.g. spreadsheets, relational databases).
- text: A sequence of characters intended to convey meaning in a natural human language.
- timeseries: Data ordered by time (e.g., sensor logs, stock prices, telemetry).
- video: Temporal visual data (sequences of still visual data), which may associated time-synchronized data such as audio tracks or transcriptions.
