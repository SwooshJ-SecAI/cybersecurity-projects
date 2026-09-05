# Cyber Intelligence Command Center (CICC)

A real-time cyber threat intelligence platform that aggregates, enriches, and scores external threat data against an organization's technology stack to surface actionable risk.

---

## Problem

Security teams face an overwhelming volume of vulnerability disclosures, exploit activity, and threat intelligence from disparate sources. Without a centralized system to correlate these data points against their own infrastructure, analysts spend hours manually triaging CVEs, reading advisories, and determining organizational relevance. Most threat feeds generate noise rather than signal.

The CICC eliminates this gap by automating the ingestion, enrichment, scoring, and presentation of external cyber intelligence -- turning raw feeds into prioritized, actionable briefings.

---

## Architecture

```
EXTERNAL SOURCES                    ENRICHMENT PIPELINE                 OUTPUT
+-----------------+                 +---------------------+             +------------------+
| CISA KEV Feed   |--+              |                     |             | Dashboard        |
| NVD/CVE Data    |  |   Download   |  Parse & Normalize  |   Score    | (index.html)     |
| EPSS Scores     |--+-->  & Cache ->|  Enrich Against     |-->Against ->|                  |
| RSS Feed 1..5   |  |   (ingest.py)|  Technology Stack    |   Org     | Executive Brief  |
| IOC Sources     |--+              |                     |   Stack    | (briefing.html)  |
+-----------------+                 +---------------------+             +------------------+
                                            |                                   |
                                    +-------v--------+                  +-------v--------+
                                    | Technology     |                  | Threat Map     |
                                    | Watchlist      |                  | (threat_map.svg)|
                                    | (CSV)          |                  +----------------+
                                    +----------------+
```

### Data Flow

1. **Ingest** -- `ingest.py` fetches live data from CISA KEV, NVD, EPSS, and 5 RSS threat intelligence feeds
2. **Parse** -- Raw data is normalized into consistent JSON structures (`data_*.json`)
3. **Enrich** -- Each CVE/advisory is matched against the technology watchlist to determine organizational relevance
4. **Score** -- EPSS probability scores, CVSS severity, and KEV status are combined into a composite risk score
5. **Present** -- Results are rendered in an interactive dashboard (`index.html`) and executive briefings

---

## File Inventory

| File | Description |
|---|---|
| `index.html` | Interactive CICC dashboard -- main situational awareness interface with sortable tables, risk charts, and drill-down views |
| `ingest.py` | Data ingestion pipeline -- fetches, parses, and caches data from all external intelligence sources |
| `cicc_executive_briefing.html` | Executive-level threat briefing -- formatted for leadership consumption with key findings and risk posture summary |
| `cicc_executive_summary.html` | Condensed executive summary -- single-page overview of current threat landscape |
| `data_cisa_kev.json` | Cached CISA Known Exploited Vulnerabilities catalog (sample data) |
| `data_epss.json` | Exploit Prediction Scoring System data for tracked CVEs (sample data) |
| `data_iocs.json` | Indicators of Compromise aggregated from RSS feeds (sample data) |
| `data_rss_feeds.json` | Parsed threat intelligence articles from security RSS feeds (sample data) |
| `threat_map.svg` | Visual threat landscape map -- SVG visualization of attack surface and threat vectors |
| `example_technology_watchlist.csv` | Template technology watchlist -- customize with your organization's stack for relevance scoring |

---

## How to Use

### Quick Start

1. Clone this repository
2. Edit `example_technology_watchlist.csv` with your organization's technology stack
3. Run `ingest.py` to fetch current threat intelligence data
4. Open `index.html` in a browser to view the dashboard

### Customization

- **Technology Watchlist** -- The watchlist drives relevance scoring. Each row should contain a vendor, product, category, version, deployment type, and criticality rating. CVEs and advisories are matched against this list to filter noise.
- **RSS Feeds** -- The ingestion pipeline is configured with 5 default security RSS feeds. Modify the feed URLs in `ingest.py` to add or replace sources.
- **Scoring Weights** -- The composite risk score combines EPSS probability, CVSS base score, and KEV status. Adjust weights in the scoring function to match your risk appetite.

### Data Refresh

Run the ingestion pipeline on a schedule (daily recommended) to keep intelligence current:

```bash
python ingest.py
```

The pipeline caches results to `data_*.json` files, which the dashboard reads on load.

---

## Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![CISA](https://img.shields.io/badge/CISA%20KEV-005288?style=flat&logoColor=white)
![NVD](https://img.shields.io/badge/NVD-003366?style=flat&logoColor=white)
![EPSS](https://img.shields.io/badge/EPSS-FF6600?style=flat&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-ED1C24?style=flat&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![SVG](https://img.shields.io/badge/SVG-FFB13B?style=flat&logo=svg&logoColor=black)
![JSON](https://img.shields.io/badge/JSON-000000?style=flat&logo=json&logoColor=white)

---

## Built With

Built with [Amazon Quick](https://github.com/SwooshJ-SecAI) as an integrated intelligence platform combining automated data ingestion, AI-powered analysis, and interactive visualization.

---

*Part of the [SwooshJ-SecAI](https://github.com/SwooshJ-SecAI) security and AI engineering portfolio.*
