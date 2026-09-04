# Third-Party Risk Assessor

> Evaluates third-party applications and vendors against the organization' 10-category security assessment framework.

## Problem It Solves

Evaluates third-party applications and vendors against the organization' 10-category security assessment framework. Operates under a spec-driven design with a strict document hierarchy: Methodology Guide (reasoning authority), Operational Guide (workflow phases with quality gates), and Reference Questionnaire (output structure). Produces audit-ready assessment packages including completed questionnaire, executive scorecard, and vendor gap questionnaire. Aligned with SOC 2 Type II audit scope.

## How It Works

- Operates as a conversational AI agent with domain-specific knowledge
- Accepts natural language queries and returns structured, actionable guidance
- Integrates with enterprise security and IT infrastructure

## Key Capabilities

- Completed Questionnaire (mapped to Reference Questionnaire structure)
- Executive Scorecard (one-page decision summary)
- Vendor Gap Questionnaire (only if items remain unresolved)
- Never assign a score of 4 (Strong) without Tier 1 or Tier 2 evidence.
- Never assign a score above 2 (Weak) based solely on vendor assertions.
- Always apply override conditions before finalizing the overall rating.
- Always flag red flag indicators immediately when identified, regardless of assessment phase.
- If information is publicly available, find it.

## Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-2C2D72?style=flat&logoColor=white)
![AI/ML](https://img.shields.io/badge/AI%2FML-FF6F00?style=flat&logoColor=white)

## Built With

Built with [Amazon Quick](https://github.com/SwooshJ-SecAI) as a custom AI agent.

---
*Part of the [SwooshJ-SecAI](https://github.com/SwooshJ-SecAI) security and AI engineering portfolio.*
