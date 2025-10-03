SPDX-License-Identifier: Community-Spec-1.0

# AIAgent

## Summary

An AI agent.

## Description

An AI agent is a software agent that uses artificial intelligence techniques
to guide its behavior. It typically incorporates a perception-action cycle,
utilizing models and heuristics to perform goal-directed activities.

An AI agent's actions can involve varying degrees of automation or human
oversight.

The following relationship types are also used to describe an AIAgent's
interactions:

- invokedBy: Describes a relationship from any Element back to the Agent that
  initiated its use or execution. (e.g., a Package is invokedby an AIAgent;
  an AIAgent is invokedBy a Person).
- usesTool: Describes a relationship from an AIAgent to an Element that
  functions as an external tool to extend the agent's capabilities.

## Metadata

- name: AIAgent
- SubclassOf: /Core/Agent
- Instantiability: Concrete

## Properties

- /Core/suppliedBy
  - type: /Core/Agent
  - minCount: 0
- automationLevel
  - type: AutomationLevel
  - minCount: 0
  - maxCount: 1
