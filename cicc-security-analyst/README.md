# CICC Security Analyst

> Conversational cyber intelligence analyst for the organization.

## Problem It Solves

Conversational cyber intelligence analyst for the organization. Answers stakeholder questions about security posture, vulnerabilities, threat landscape, and organizational risk using live intelligence data from the CICC pipeline. Automatically refreshes stale data before responding. Produces on-demand briefings, risk summaries, and compliance snapshots for audiences from SOC analysts to executives.

## How It Works

- **Step 1: Fetch Sources (parallel)**: Fetch all 6 sources simultaneously:
- **Step 2: Filter KEV to 30-day window**: Filter vulnerabilities where dateAdded is within the last 30 days from today.
- **Step 3: Match against Technology Watchlist**: For each KEV entry, check vendorProject + product against the watchlist using word-boundary regex. Classify as DIRECT, STRONG, INDIRECT, SOURCE ONLY, or NONE.
- **Step 4: Fetch NVD CVSS (rate-limited)**: For each KEV CVE, fetch CVSS from https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={CVE}
- **Step 5: Fetch EPSS (single batch)**: Fetch all EPSS scores in one call: https://api.first.org/data/v1/epss?cve={comma-separated CVEs}

## Key Capabilities

- data_cisa_kev.json -- KEV events with NVD/EPSS enrichment, watchlist matching, relevance scoring, corroboration
- data_rss_feeds.json -- Classified RSS articles from attack landscape feeds
- **Step 1: Fetch Sources (parallel)**
- **Step 2: Filter KEV to 30-day window**
- **Step 3: Match against Technology Watchlist**
- **Step 4: Fetch NVD CVSS (rate-limited)**
- **Step 5: Fetch EPSS (single batch)**
- **Step 6: Enrich Events**

## Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-ED1C24?style=flat&logoColor=white)
![Security](https://img.shields.io/badge/Security-2C2D72?style=flat&logoColor=white)
![AI/ML](https://img.shields.io/badge/AI%2FML-FF6F00?style=flat&logoColor=white)

## Built With

Built with [Amazon Quick](https://github.com/SwooshJ-SecAI) as a custom AI agent.

---
*Part of the [SwooshJ-SecAI](https://github.com/SwooshJ-SecAI) security and AI engineering portfolio.*
