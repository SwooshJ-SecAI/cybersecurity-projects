# CICC — Design Decisions

This document records the architectural choices behind the Cyber Intelligence Command Center, the trade-offs weighed at each decision point, and the lessons learned building and operating the pipeline. It is written for engineers who want to understand *why* the system is shaped the way it is, not just how to run it.

---

## Why Aggregate Multiple Intelligence Sources

The single most consequential decision was to aggregate four distinct intelligence sources rather than standardize on one.

### The sources and what each contributes

- **CISA KEV (Known Exploited Vulnerabilities)** — the authoritative signal that a vulnerability is being exploited in the wild right now. KEV is small, high-confidence, and action-oriented. If a CVE is on the KEV list, it deserves attention regardless of any other score.
- **NVD (National Vulnerability Database)** — the comprehensive backbone. NVD provides CVSS base scores, affected product configurations (CPE), and canonical descriptions. It is complete but slow to update and noisy on its own.
- **EPSS (Exploit Prediction Scoring System)** — a probabilistic forward-looking signal. EPSS estimates the likelihood that a vulnerability will be exploited in the next 30 days. It fills the gap between "theoretically severe" (CVSS) and "confirmed exploited" (KEV).
- **RSS threat feeds** — the narrative layer. Vendor advisories, security research blogs, and news feeds surface context that structured databases miss: campaign attribution, exploitation techniques, and emerging threats that have not yet been assigned a CVE.

### The rationale

No single source answers the question a security team actually asks: *"Of everything disclosed this week, what should we care about?"* CVSS alone over-prioritizes — a 9.8 on a product not deployed is noise. KEV alone under-covers — it only lists confirmed exploitation, missing the leading edge. EPSS alone lacks the deployment context to be actionable.

Combining them produces a composite signal that is far more useful than any input in isolation. A vulnerability that is on KEV, has a high EPSS score, carries a high CVSS rating, *and* affects something on the organization's watchlist is unambiguous. The aggregation is what turns four noisy feeds into one prioritized queue.

### The cost

Aggregation is not free. Each source has its own format, update cadence, authentication model, and failure mode. The pipeline must normalize four schemas into one, handle partial failures gracefully (one feed down should not blank the dashboard), and reconcile identifier mismatches across sources. That complexity was accepted deliberately because the alternative — a single-source view — is not decision-grade.

---

## Why Score Against a Technology Watchlist Instead of All CVEs

The second defining decision was to filter and score every disclosure against an explicit technology watchlist rather than presenting the full CVE firehose.

### The problem with showing everything

There are tens of thousands of CVEs published per year. A dashboard that shows all of them is a dashboard nobody reads. The volume itself is the enemy of action. Analysts do not need to know that a vulnerability exists in a product the organization has never deployed.

### The watchlist as a relevance filter

The watchlist is a structured inventory of the organization's technology stack — vendor, product, category, version, deployment type, and a criticality rating per entry. Every incoming disclosure is matched against this list. A CVE that touches a watchlist product is enriched and scored; one that does not is deprioritized or dropped.

This inverts the default posture. Instead of "here is everything, go find what matters," the system says "here is what matters to *you*, ranked." The watchlist is the mechanism that makes the difference.

### The trade-off

The watchlist introduces a maintenance dependency and a blind-spot risk. If the watchlist is stale, the system will miss relevant disclosures for newly deployed technology. If it is incomplete, coverage gaps appear silently. This was accepted as a worthwhile trade because a maintained watchlist is a far smaller burden than manually triaging the full CVE stream, and because watchlist maintenance is a discrete, delegable task with a clear owner.

The template watchlist shipped in this repository (`example_technology_watchlist.csv`) documents the expected schema so the relevance-scoring behavior is reproducible without exposing any specific organization's inventory.

---

## The Enrichment Pipeline Design

The pipeline follows a deliberate five-stage flow: **download → parse → enrich → score → write**.

### Stage 1: Download and cache

`ingest.py` fetches from each source and caches raw responses locally before any processing. Caching first — rather than processing inline — means a downstream parsing bug does not require re-hitting rate-limited APIs, and it makes the pipeline debuggable: the raw input is always available for inspection.

### Stage 2: Parse and normalize

Each source is normalized into a consistent internal JSON structure (`data_*.json`). This is where four schemas collapse into one. Normalizing early means every downstream stage operates on a uniform shape, and adding a fifth source later only requires writing one new parser, not touching the scoring logic.

### Stage 3: Enrich against the watchlist

Each normalized disclosure is matched against the technology watchlist. Matches are annotated with the affected product's criticality and deployment context. This is the stage that attaches organizational meaning to a generic disclosure.

### Stage 4: Score

A composite risk score combines EPSS probability, CVSS base score, and KEV status. The weighting is intentionally a single, adjustable function rather than a hard-coded formula scattered through the code — risk appetite varies by organization, and the scoring weights are the natural place to express it.

### Stage 5: Write

Results are written back to the `data_*.json` files that the dashboard reads on load. Decoupling the ingestion pipeline from the presentation layer via flat files means the dashboard has no runtime dependency on the pipeline being live — it renders whatever the last successful run produced.

### Why this ordering matters

Each stage produces an inspectable artifact. If the dashboard looks wrong, an engineer can walk backward: is the written data wrong (stage 5), the score wrong (stage 4), the enrichment wrong (stage 3), the parse wrong (stage 2), or the source data itself wrong (stage 1)? The staged design makes failures localizable instead of mysterious.

---

## Trade-offs

### Freshness vs. completeness

Running the pipeline more frequently keeps intelligence current but increases API load and the chance of hitting rate limits. Running it less frequently is gentler on sources but risks acting on stale data. A daily refresh was chosen as the default balance — frequent enough that KEV additions are caught within a day, infrequent enough to stay well within rate limits. Organizations with higher tempo can shorten the interval by adjusting the schedule.

### Automation vs. manual review

The pipeline automates ingestion, enrichment, and scoring, but it deliberately stops short of automated remediation or ticket creation from within CICC itself. The system produces a prioritized view; a human decides what to act on. This boundary was drawn intentionally: automated scoring is trustworthy because it is deterministic and inspectable, but automated *action* on external intelligence carries a false-positive risk that warrants a human in the loop.

### Flat files vs. a database

Caching to JSON files rather than a database keeps the system portable, inspectable, and dependency-light. The cost is that it does not scale to millions of records or support complex historical queries. For the scale this system targets — a curated watchlist and a rolling window of current disclosures — flat files are the right call. A database would be premature complexity.

---

## Lessons Learned

### API rate limits are a first-class design constraint

Early iterations hit NVD rate limits during development by re-fetching on every run. The cache-first design was a direct response. The lesson generalizes: when building against public intelligence APIs, treat the rate limit as a hard constraint from day one, not an afterthought. Cache aggressively, back off politely, and never make the same request twice if the previous answer is still valid.

### Feed formats are inconsistent and change without notice

The four sources disagree on nearly everything: date formats, CVE identifier casing, how severity is expressed, and how missing data is represented. RSS feeds in particular are only loosely standardized in practice. The normalization stage had to be defensive — assume any field can be missing, malformed, or newly renamed. Parsing that trusts the source format will break; parsing that validates and defaults survives.

### EPSS scores are easy to misinterpret

EPSS produces a probability (0 to 1) that a vulnerability will be exploited in a 30-day window. It is tempting to treat it like a severity score, but it is not — a low-CVSS vulnerability can carry a high EPSS score if it is trivially exploitable and widely targeted, and a critical-CVSS vulnerability can carry a low EPSS score if exploitation is impractical. The scoring function keeps EPSS and CVSS as separate inputs precisely because they measure different things. Conflating them produces misleading priorities.

### Partial failure handling determines whether the tool gets used

The first version treated any source failure as a fatal error, which meant a single flaky feed blanked the entire dashboard. Users stopped trusting it. Redesigning so that each source fails independently — a down feed produces a visible "stale" indicator rather than an empty screen — was what made the tool dependable enough to check every morning. Reliability, not features, drives adoption for an operational tool.
