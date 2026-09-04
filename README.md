# Cybersecurity Projects

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white)
![Splunk](https://img.shields.io/badge/Splunk-000000?style=flat&logo=splunk&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-ED1C24?style=flat&logoColor=white)
![CISA KEV](https://img.shields.io/badge/CISA%20KEV-005288?style=flat&logoColor=white)

Security tooling, threat intelligence platforms, compliance automation, and a catalog of vendor-specific AI agents for security operations.

---

## Overview

This repository collects production-tested security engineering work spanning four areas: a real-time threat intelligence platform, a fleet of vendor-specific security operations agents, compliance automation tooling, and supporting integrations. The emphasis is on turning manual, repetitive security workflows into automated systems that surface signal instead of noise.

**What's inside:**

- **15 security AI agents** — see the [Agent Catalog](./AGENTS.md)
- **17 reusable AI skills** — see the [amazon-quick-skills](https://github.com/SwooshJ-SecAI/amazon-quick-skills) repository
- **CICC threat intelligence platform** — full ingestion, enrichment, and scoring pipeline

---

## Structure

### [cicc/](./cicc/)
The Cyber Intelligence Command Center — a real-time threat intelligence platform that aggregates CISA KEV, NVD, EPSS, and RSS feeds, enriches disclosures against a technology watchlist, and scores them into prioritized, actionable briefings. Includes the ingestion pipeline, interactive dashboard, executive briefings, and a [design decisions](./cicc/DESIGN_DECISIONS.md) write-up.

### [security-agents/](./security-agents/)
Eight vendor-specific subject matter expert agents covering the operational security stack: Splunk, Arctic Wolf, Microsoft Purview, Freshservice ITSM, SecurityScorecard, Darktrace, Palo Alto Networks, and SentinelOne. Each agent carries its own knowledge base (operational reference, query language guide, remediation playbooks). See the [design decisions](./security-agents/DESIGN_DECISIONS.md) for the architecture rationale.

### [compliance-automation/](./compliance-automation/)
SOC 2, ISO 27001, and HIPAA compliance tooling — evidence collection, control-to-evidence mapping, quarterly audit comparison, and audit-ready reporting. Includes three compliance agents and a [design decisions](./compliance-automation/DESIGN_DECISIONS.md) write-up.

### [vulnerability-scanner/](./vulnerability-scanner/)
Vulnerability report summarization — transforms raw scan output (Nessus, Qualys, ZAP) into executive-ready reports with CVSS scoring and MITRE ATT&CK mapping.

### [freshservice-integration/](./freshservice-integration/)
ITSM automation — end-to-end ticket creation, intelligent routing, and stakeholder notification against a Freshservice instance.

---

## Getting Started

Each subfolder is self-contained with its own README. Start with the [CICC platform](./cicc/) for the most complete end-to-end example, or browse the [Agent Catalog](./AGENTS.md) to see the full range of security operations agents.

---

## Built With

Built with [Amazon Quick](https://github.com/SwooshJ-SecAI). Agents, skills, and automation pipelines were developed on the Amazon Quick platform and sanitized for public release.

---

## License

MIT

---

*Part of the [SwooshJ-SecAI](https://github.com/SwooshJ-SecAI) security and AI engineering portfolio.*
