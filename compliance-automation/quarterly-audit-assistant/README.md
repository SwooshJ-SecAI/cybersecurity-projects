# Quarterly Audit Assistant

> Compares quarterly audit documents side-by-side, matching records by email address (with fallback to account name) to identify additions, removals, and changes between quarters.

## Problem It Solves

Compares quarterly audit documents side-by-side, matching records by email address (with fallback to account name) to identify additions, removals, and changes between quarters. Posts findings as a note on the current quarter's audit ticket. Supports follow-up validation against User AD Reports, On-Boarding, Off-Boarding, and Freshservice tickets when the user provides supporting documentation.

## How It Works

- **Freshservice Configuration**: Domain: example-company.freshservice.com
- **Workflow Integration**: When the agent creates audit tickets via the Freshservice API, it MUST include the tag `quarterly-audit-assistant` in the tags array. This tag triggers the "SOC Quarterly Audits - IT 2.0" workflow (active version ID: 20000536082), which initiates the 4-level approval chain automatically.
- **Freshservice Views**: The agent uses four Freshservice ticket views as data sources:
- **Audit Ticket Subject Pattern**: All audit tickets follow this naming convention:
- **Phase 1 -- Compare and Document**: **Purpose:** Pull the previous quarter's data from its Freshservice ticket, compare against the current quarter, and post findings as a note on the current audit ticket.

## Key Capabilities

- **Freshservice Configuration**
- Domain: example-company.freshservice.com
- API: REST v2 (Basic Auth)
- API Key: swSe1ytzE2GyVeq9R3lm
- Default Requester: SwooshJ-SecAI@example-company.com
- **Workflow Integration**
- **Freshservice Views**
- **Audit Ticket Subject Pattern**

## Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Freshservice](https://img.shields.io/badge/Freshservice-0F4C81?style=flat&logoColor=white)
![SOC 2](https://img.shields.io/badge/SOC%202-00599C?style=flat&logoColor=white)

## Built With

Built with [Amazon Quick](https://github.com/SwooshJ-SecAI) as a custom AI agent.

---
*Part of the [SwooshJ-SecAI](https://github.com/SwooshJ-SecAI) security and AI engineering portfolio.*
