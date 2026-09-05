# Security Investigation Copilot Agent [LABs]

> Evidence-driven Security Investigation Copilot for Security Analysts, Security Engineers, Incident Responders, Threat Hunters, Detection Engineers, and SOC personnel.

## Architecture

![Architecture diagram](./architecture.svg)

*System-model diagram showing the agent's workflow, data flow, and supporting infrastructure.*

## Problem It Solves

Evidence-driven Security Investigation Copilot for Security Analysts, Security Engineers, Incident Responders, Threat Hunters, Detection Engineers, and SOC personnel. Structures investigations from incomplete alerts, validates detections, separates FACT/HYPOTHESIS/UNKNOWN/RECOMMENDATION, correlates telemetry, reconstructs timelines, maps supported behavior to MITRE ATT&CK, reassesses risk, and produces a standardized Security Investigation Report. Now includes the organization technology environment context (22 vendor families across Tier 1 and Tier 2) for asset criticality assessment.

## How It Works

- **Tier 1 -- Critical Infrastructure**: | Vendor | Products | Category |
- **Tier 2 -- Business Operations**: | Vendor | Products | Category |
- **CICC Intelligence Data**: External cyber intelligence data (CISA KEV, NVD, EPSS, RSS threat feeds) is maintained by the CICC Intelligence Refresh agent. During investigations involving CVEs or known exploited vulnerabilities, reference this data for organizational relevance scoring and threat context.

## Key Capabilities

- FACT — directly supported by provided evidence.
- HYPOTHESIS — plausible explanation requiring validation.
- UNKNOWN — required information that is unavailable.
- RECOMMENDATION — proposed investigation or defensive action (never a completed action).
- Never fabricate logs, timestamps, usernames, IP addresses, hashes, domains, URLs, processes, MITRE techniques, business impact, containment actions, or investigation results.
- Do NOT classify an alert as a confirmed incident unless the available evidence supports that conclusion.
- Mark missing intake fields as UNKNOWN rather than inferring them.
- Evidence before opinion: no confirmed compromise without supporting evidence.

## Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-ED1C24?style=flat&logoColor=white)
![Security](https://img.shields.io/badge/Security-2C2D72?style=flat&logoColor=white)
![AI/ML](https://img.shields.io/badge/AI%2FML-FF6F00?style=flat&logoColor=white)

## Built With

Built with [Amazon Quick](https://github.com/SwooshJ-SecAI) as a custom AI agent.

---
*Part of the [SwooshJ-SecAI](https://github.com/SwooshJ-SecAI) security and AI engineering portfolio.*
