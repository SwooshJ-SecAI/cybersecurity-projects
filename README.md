# Cybersecurity Projects

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white)
![Splunk](https://img.shields.io/badge/Splunk-000000?style=flat&logo=splunk&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-ED1C24?style=flat&logoColor=white)
![CISA KEV](https://img.shields.io/badge/CISA%20KEV-005288?style=flat&logoColor=white)

Security tooling, threat intelligence platforms, and a catalog of vendor-specific AI agents for security operations.

---

## Overview

This repository collects production-tested security engineering work spanning three areas: a real-time threat intelligence platform, a fleet of vendor-specific security operations agents, and vulnerability reporting tooling. The emphasis is on turning manual, repetitive security workflows into automated systems that surface signal instead of noise.

**What's inside:**

- **11 security AI agents** — see the [Agent Catalog](./AGENTS.md)
- **Reusable AI skills** — see the [amazon-quick-skills](https://github.com/SwooshJ-SecAI/amazon-quick-skills) repository
- **CICC threat intelligence platform** — full ingestion, enrichment, and scoring pipeline

---

## Structure

### [cicc/](./cicc/)
The Cyber Intelligence Command Center — a real-time threat intelligence platform that aggregates CISA KEV, NVD, EPSS, and RSS feeds, enriches disclosures against a technology watchlist, and scores them into prioritized, actionable briefings. Includes the ingestion pipeline, interactive dashboard, executive briefings, and a [design decisions](./cicc/DESIGN_DECISIONS.md) write-up.

### [security-agents/](./security-agents/)
Seven vendor-specific subject matter expert agents covering the operational security stack: Splunk, Arctic Wolf, Microsoft Purview, SecurityScorecard, Darktrace, Palo Alto Networks, and SentinelOne. Each agent carries its own knowledge base (operational reference, query language guide, remediation playbooks). See the [design decisions](./security-agents/DESIGN_DECISIONS.md) for the architecture rationale.

### [vulnerability-scanner/](./vulnerability-scanner/)
Vulnerability report summarization — transforms raw scan output (Nessus, Qualys, ZAP) into executive-ready reports with CVSS scoring and MITRE ATT&CK mapping.

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
