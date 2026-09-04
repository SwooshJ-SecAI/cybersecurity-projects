# SOC 2 Audit Agent

> AI-powered internal audit assistant for SOC 2 Type II compliance.

## Problem It Solves

AI-powered internal audit assistant for SOC 2 Type II compliance. Operates under a spec-driven architecture with a 6-phase lifecycle (Planning, Collection, Review, Testing, Findings, Reporting), explicit quality gates between phases, 5-dimension evidence scoring methodology, mandatory 7-element finding format, and defined boundaries with adjacent agents (Evidence Copilot, TPRM, Quarterly Audit). Grounded in the organization' 98-control environment and 2026 DRL from RSM.

## How It Works

- **Phase 1: PLANNING**: Activities: Read the current DRL from SharePoint. Generate risk-ranked audit plan, map controls to TSC, recommend schedule based on control frequency and risk, identify control dependencies, create walkthrough agendas, review prior-year findings.
- **Phase 2: EVIDENCE COLLECTION**: Activities: Generate evidence request communications, define acceptance criteria per control type, recommend sampling approach, create Freshservice tickets directly via the REST API (ONLY if gate met -- see Ticket Generation Authority below).
- **Phase 3: EVIDENCE REVIEW**: Activities: Score evidence quality (0-100 using 5-dimension rubric per Methodology Guide), identify gaps, flag red flags, recommend additional evidence when score below 65.
- **Phase 4: CONTROL TESTING**: Activities: Generate testing procedures per AICPA standards (Methodology Guide Section 2), apply sampling guidance, execute by control type, classify results, document exceptions with root cause.
- **Phase 5: FINDINGS GENERATION**: Activities: Draft findings using mandatory 7-element format (Methodology Guide Section 4), calculate severity (Methodology Guide Section 6), assign root cause (Methodology Guide Section 5), generate remediation recommendations.

## Key Capabilities

- **Executive / Final Oversight -- Tom Balloch (DRL "Owner").** Ultimately answerable, provides final sign-off. Not the day-to-day coordinator.
- **Evidence Contributors -- Infrastructure / Security / Ops personnel.** Pull and submit evidence; responsibilities overlap and rotate.
- SOC 2 Evidence Copilot (that agent is the frontend -- a reference and help tool for evidence submitters; separate concern)
- Third-Party Risk Assessor (separate operational agent in its own lane)
- Quarterly Audit Assistant (separate operational agent in its own lane)
- **Phase 1: PLANNING**
- **Phase 2: EVIDENCE COLLECTION**
- **Phase 3: EVIDENCE REVIEW**

## Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![SOC 2](https://img.shields.io/badge/SOC%202-00599C?style=flat&logoColor=white)
![AI/ML](https://img.shields.io/badge/AI%2FML-FF6F00?style=flat&logoColor=white)

## Built With

Built with [Amazon Quick](https://github.com/SwooshJ-SecAI) as a custom AI agent.

---
*Part of the [SwooshJ-SecAI](https://github.com/SwooshJ-SecAI) security and AI engineering portfolio.*
