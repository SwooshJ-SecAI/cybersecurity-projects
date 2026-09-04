# Cyber Intelligence Command Center (CICC)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Threat Intel](https://img.shields.io/badge/Domain-Threat%20Intelligence-red?style=flat-square)

An external threat intelligence aggregation and scoring platform. Ingests live data from CISA KEV, NVD, EPSS, and five RSS attack landscape feeds, enriches events against an organizational technology watchlist, and produces prioritized intelligence products.

Built with [Amazon Quick](https://amazon.com/quick).

---

## Features

- Automated data pipeline: CISA KEV, NVD, EPSS, RSS feed ingestion
- CVSS and EPSS-based vulnerability scoring with organizational relevance weighting
- Technology watchlist matching for enterprise-specific threat prioritization
- Situational report generation: SITREP, morning standup briefs, posture assessments
- Conversational analyst interface for ad-hoc security posture queries
- Historical trend analysis and threat actor attribution tracking

## Directory Structure

```
cicc/
|-- data/                # Intelligence data files (JSON)
|-- pipelines/           # Data ingestion and enrichment scripts
|-- reports/             # Generated intelligence products
|-- config/              # Watchlist and source configuration
|-- README.md
```

## Status

Active development. See project-specific documentation for current capabilities and roadmap.

## Getting Started

Refer to the parent repository [cybersecurity-projects](../) for general setup instructions. Project-specific configuration is documented in this directory as development progresses.

## License

This project is licensed under the MIT License. See [LICENSE](../../LICENSE) for details.

---

**Author:** Antonio Johnson | Security Engineer II / Enterprise AI Engineer