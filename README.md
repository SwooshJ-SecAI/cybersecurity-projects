# Cybersecurity Projects

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Security](https://img.shields.io/badge/Domain-Cybersecurity-blue?style=flat-square)
![Automation](https://img.shields.io/badge/Focus-Automation-green?style=flat-square)

Production-grade cybersecurity tools, threat intelligence pipelines, compliance automation, and ITSM integrations. Each project addresses a real-world security operations challenge with working code, architecture documentation, and deployment guidance.

Built with [Amazon Quick](https://amazon.com/quick).

---

## Description

This repository contains cybersecurity engineering projects developed to solve operational security problems at enterprise scale. The work spans threat intelligence collection and scoring, vulnerability management, compliance policy generation, ITSM ticket automation, and vendor-specific security tool integration.

Every project in this repository originated from production use cases and reflects practical security engineering rather than theoretical exercises.

## Projects

### Cyber Intelligence Command Center (CICC)

An external threat intelligence aggregation platform that pulls live data from CISA KEV, NVD, EPSS, and multiple RSS attack landscape feeds. Enriches and scores events against an organizational technology watchlist, producing prioritized intelligence briefs and situational awareness reports.

**Key capabilities:**
- Automated data ingestion from five external intelligence sources
- CVSS and EPSS-based vulnerability scoring and prioritization
- Technology watchlist matching for organizational relevance
- Situational report generation (SITREP, morning standup briefs)
- Historical trend analysis and threat actor tracking

### Vulnerability Report Summarizer

Transforms raw vulnerability scan output from Nessus, Qualys, OWASP ZAP, and similar tools into executive-ready security reports. Scores findings by CVSS, maps to MITRE ATT&CK where applicable, and produces both technical and executive summaries with prioritized remediation plans.

### Compliance Automation Framework

Generates draft compliance policies for SOC 2 Type I/II, ISO 27001, and HIPAA. Produces evidence collection checklists, control mapping matrices, and gap analysis reports from existing documentation. Designed to accelerate audit preparation from weeks to hours.

### Freshservice ITSM Integration

Full Freshservice ITSM integration pipeline covering ticket creation, closure, querying, updating, notes, reassignment, escalation, asset management, agent and group listing, change requests, problems, and releases. Five composable Python modules provide complete API surface coverage.

### Security Tool Agent Builder

Framework for building vendor-specific security tool SME agents with comprehensive knowledge bases. Produces specialized agents that help navigate, query, triage, and remediate across security platforms including Arctic Wolf, SentinelOne, Palo Alto, Darktrace, SecurityScorecard, Freshservice, and Microsoft Purview.

## Repository Structure

```
cybersecurity-projects/
|-- cicc/                        # Cyber Intelligence Command Center
|   |-- README.md
|-- vulnerability-scanner/       # Vulnerability report summarizer
|   |-- README.md
|-- compliance-automation/       # Compliance policy and audit automation
|   |-- README.md
|-- freshservice-integration/    # Freshservice ITSM pipeline
|   |-- README.md
|-- security-agents/             # Security tool agent builder
|   |-- README.md
|-- .gitignore
|-- README.md
```

## Technology Stack

| Component          | Technology                                    |
|--------------------|-----------------------------------------------|
| Language           | Python 3.10+                                  |
| Cloud              | AWS                                           |
| Intelligence Feeds | CISA KEV, NVD, EPSS, RSS                      |
| ITSM               | Freshservice API                              |
| Frameworks         | SOC 2, ISO 27001, HIPAA, MITRE ATT&CK        |
| Platform           | Amazon Quick                                  |

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/ajohnson/cybersecurity-projects.git
   cd cybersecurity-projects
   ```
2. Navigate to the project directory of interest
3. Follow the project-specific README for setup and configuration
4. Review architecture documentation before modifying pipelines

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**Author:** Antonio Johnson | Security Engineer II / Enterprise AI Engineer