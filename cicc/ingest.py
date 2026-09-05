#!/usr/bin/env python3
"""
CICC Intelligence Ingestion Pipeline
=====================================
Phase 1 Scheduler - Fetches and normalizes external intelligence sources.

Sources:
  - CISA KEV (Known Exploited Vulnerabilities) -- JSON, no auth
  - NVD API v2.0 (CVSS/CWE enrichment) -- REST, free API key recommended
  - RSS Feeds (Attack Landscape) -- XML, no auth

Usage:
  python ingest.py                    # Full pipeline run
  python ingest.py --source kev       # KEV only
  python ingest.py --source nvd       # NVD enrichment only  
  python ingest.py --source rss       # RSS feeds only
  python ingest.py --days 7           # Only last 7 days of KEV (default: 30)

Output:
  data_cisa_kev.json     - KEV events with NVD enrichment
  data_rss_feeds.json    - RSS intelligence events
  data_combined.json     - All sources merged and ranked
  pipeline_log.json      - Ingestion metadata and errors

Requirements:
  Python 3.8+, no external packages (uses stdlib only)
"""

import json
import sys
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

# ===================================================================
# CONFIGURATION
# ===================================================================

CONFIG = {
    'output_dir': '.',  # Same directory as the HTML app
    'kev_url': 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',
    'nvd_base_url': 'https://services.nvd.nist.gov/rest/json/cves/2.0',
    'nvd_api_key': '',  # Set via NVD_API_KEY env var for higher rate limits
    'nvd_rate_limit': 6,  # seconds between requests (no key = 5 req/30s)
    'kev_window_days': 30,
    'rss_feeds': [
        {'name': 'The Hacker News', 'url': 'https://feeds.feedburner.com/TheHackersNews', 'category': 'Attack Landscape'},
        {'name': 'BleepingComputer', 'url': 'https://www.bleepingcomputer.com/feed/', 'category': 'Attack Landscape'},
        {'name': 'The Record', 'url': 'https://therecord.media/feed', 'category': 'Attack Landscape'},
        {'name': 'SecurityWeek', 'url': 'https://feeds.feedburner.com/securityweek', 'category': 'Attack Landscape'},
    ],
}

# Technology Watchlist
WATCHLIST = [
    {'id':'TW-001','vendor':'Palo Alto Networks','product':'Palo Alto Networks','aliases':['PAN','Palo Alto','PAN-OS','GlobalProtect']},
    {'id':'TW-002','vendor':'Palo Alto Networks','product':'Palo Alto Networks Firewalls','aliases':['PA Firewall','NGFW']},
    {'id':'TW-003','vendor':'Palo Alto Networks','product':'PAN-OS','aliases':['PAN-OS']},
    {'id':'TW-004','vendor':'SentinelOne','product':'SentinelOne','aliases':['S1','Singularity']},
    {'id':'TW-005','vendor':'Abnormal Security','product':'Abnormal Security','aliases':[]},
    {'id':'TW-006','vendor':'Microsoft','product':'Microsoft','aliases':['MSFT']},
    {'id':'TW-007','vendor':'Microsoft','product':'Microsoft 365','aliases':['M365','Office 365','O365']},
    {'id':'TW-008','vendor':'Microsoft','product':'Microsoft Entra ID','aliases':['Azure AD','AAD','Entra']},
    {'id':'TW-009','vendor':'Microsoft','product':'Microsoft Defender','aliases':['Windows Defender','MDE']},
    {'id':'TW-010','vendor':'Microsoft','product':'Microsoft Purview','aliases':[]},
    {'id':'TW-011','vendor':'Microsoft','product':'Exchange Online','aliases':['EXO','Exchange']},
    {'id':'TW-012','vendor':'Amazon Web Services','product':'AWS','aliases':['Amazon Web Services','AWS']},
]

# ===================================================================
# WATCHLIST CORRELATION
# ===================================================================

def correlate_watchlist(vendor, product, description=''):
    """Determine relationship between an event and our technology watchlist."""
    vendor_lower = (vendor or '').lower()
    product_lower = (product or '').lower()
    desc_lower = (description or '').lower()
    combined = f"{vendor_lower} {product_lower} {desc_lower}"
    
    for tech in WATCHLIST:
        tech_vendor = tech['vendor'].lower()
        tech_product = tech['product'].lower()
        all_terms = [tech_vendor, tech_product] + [a.lower() for a in tech['aliases']]
        
        for term in all_terms:
            if term in vendor_lower or vendor_lower in term:
                return {'relationship': 'DIRECT', 'matched_tech': tech['product'], 'tech_id': tech['id']}
            if term in product_lower or product_lower in term:
                return {'relationship': 'DIRECT', 'matched_tech': tech['product'], 'tech_id': tech['id']}
    
    return {'relationship': 'NONE', 'matched_tech': None, 'tech_id': None}


def calculate_relevance(event):
    """Calculate organizational relevance score (0-100). v3 weights with EPSS."""
    score = 0
    
    # Technology Match (20%)
    rel = event.get('relationship', 'NONE')
    if rel == 'DIRECT': score += 20
    elif rel == 'STRONG': score += 15
    elif rel == 'INDIRECT': score += 8
    
    # Active Exploitation (18%)
    if event.get('activeExploit'): score += 18
    
    # CISA KEV (12%)
    if event.get('kev'): score += 12
    
    # Threat Severity (12%)
    sev = event.get('globalSeverity', '')
    if sev == 'Critical': score += 12
    elif sev == 'High': score += 9
    elif sev == 'Medium': score += 5
    elif sev == 'Low': score += 2
    
    # CVSS (8%)
    cvss = event.get('cvss')
    if cvss:
        if cvss >= 9.0: score += 8
        elif cvss >= 7.0: score += 6
        elif cvss >= 4.0: score += 4
        else: score += 2
    
    # Exploit Availability (7%)
    if event.get('exploitAvail') or event.get('kev'): score += 7
    
    # Product Criticality (6%)
    product_lower = (event.get('product','') or '').lower()
    critical_terms = ['firewall','vpn','authentication','identity','active directory',
                      'exchange','sharepoint','domain controller','vcenter','esxi']
    if any(t in product_lower for t in critical_terms):
        score += 6
    elif rel == 'DIRECT':
        score += 4
    
    # EPSS (5%)
    epss = event.get('epss')
    if epss:
        if epss >= 0.7: score += 5
        elif epss >= 0.3: score += 3
        elif epss >= 0.1: score += 2
        else: score += 1
    
    # Industry Targeting (3%)
    industry = (event.get('industry','') or '').lower()
    if any(t in industry for t in ['healthcare','health','medical','pharma','hospital']):
        score += 3
    
    # Source Confidence (3%)
    conf = event.get('sourceConfidence', 'Medium')
    if conf == 'Very High': score += 3
    elif conf == 'High': score += 2
    elif conf == 'Medium': score += 1
    
    # Intelligence Recency (3%)
    pub = event.get('published', '')
    if pub:
        try:
            pub_date = datetime.strptime(pub[:10], '%Y-%m-%d')
            days = (datetime.now() - pub_date).days
            if days <= 7: score += 3
            elif days <= 14: score += 2
            elif days <= 30: score += 1
        except: pass
    
    # Attack Vector (3%)
    vector = event.get('cvssVector', '')
    if 'AV:N' in vector: score += 3
    elif 'AV:A' in vector: score += 2
    elif 'AV:L' in vector: score += 1
    
    # Ransomware (bonus)
    if event.get('ransomware'): score += 5
    
    return min(100, score)

# ===================================================================
# CISA KEV INGESTION
# ===================================================================

def fetch_kev(days=30):
    """Fetch and normalize CISA KEV catalog."""
    print(f"[KEV] Fetching CISA KEV catalog...")
    
    req = urllib.request.Request(CONFIG['kev_url'], headers={'User-Agent': 'CICC/1.0'})
    response = urllib.request.urlopen(req, timeout=30)
    data = json.loads(response.read().decode('utf-8'))
    
    vulns = data.get('vulnerabilities', [])
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    recent = [v for v in vulns if v.get('dateAdded', '') >= cutoff]
    
    print(f"[KEV] Catalog v{data.get('catalogVersion')} | Total: {len(vulns)} | Last {days}d: {len(recent)}")
    
    events = []
    for v in recent:
        match = correlate_watchlist(v['vendorProject'], v['product'], v.get('shortDescription',''))
        event = {
            'id': f"KEV-{v['cveID']}",
            'title': v['vulnerabilityName'],
            'summary': v['shortDescription'],
            'type': 'Vulnerability',
            'globalSeverity': 'Critical',
            'cve': v['cveID'],
            'kev': True,
            'kevDateAdded': v['dateAdded'],
            'kevDueDate': v.get('dueDate', ''),
            'activeExploit': True,
            'vendor': v['vendorProject'],
            'product': v['product'],
            'requiredAction': v.get('requiredAction', ''),
            'ransomware': v.get('knownRansomwareCampaignUse', 'Unknown') == 'Known',
            'relationship': match['relationship'],
            'techMatch': match['matched_tech'],
            'techId': match['tech_id'],
            'source': 'CISA KEV',
            'sourceConfidence': 'Very High',
            'published': v['dateAdded'],
        }
        events.append(event)
    
    return events, data.get('catalogVersion'), data.get('count')


# ===================================================================
# NVD ENRICHMENT
# ===================================================================

def enrich_nvd(events):
    """Enrich events with NVD CVSS data."""
    api_key = CONFIG.get('nvd_api_key') or os.environ.get('NVD_API_KEY', '')
    rate_limit = 2 if api_key else CONFIG['nvd_rate_limit']
    
    cves = [e['cve'] for e in events if e.get('cve')]
    print(f"[NVD] Enriching {len(cves)} CVEs (rate limit: {rate_limit}s between requests)...")
    
    enriched = 0
    for i, event in enumerate(events):
        cve = event.get('cve')
        if not cve:
            continue
        
        url = f"{CONFIG['nvd_base_url']}?cveId={cve}"
        headers = {'User-Agent': 'CICC/1.0'}
        if api_key:
            headers['apiKey'] = api_key
        
        try:
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode('utf-8'))
            
            vulns = data.get('vulnerabilities', [])
            if vulns:
                cve_item = vulns[0].get('cve', {})
                metrics = cve_item.get('metrics', {})
                
                # Extract CVSS
                if metrics.get('cvssMetricV31'):
                    d = metrics['cvssMetricV31'][0].get('cvssData', {})
                    event['cvss'] = d.get('baseScore')
                    event['cvssVector'] = d.get('vectorString')
                    event['cvssSeverity'] = d.get('baseSeverity')
                
                # Extract CWE
                cwes = []
                for w in cve_item.get('weaknesses', []):
                    for desc in w.get('description', []):
                        val = desc.get('value', '')
                        if val and 'noinfo' not in val:
                            cwes.append(val)
                event['cwes'] = cwes
                
                enriched += 1
            
            if i < len(events) - 1:
                time.sleep(rate_limit)
                
        except Exception as e:
            print(f"[NVD] Error enriching {cve}: {e}")
            if '429' in str(e):
                print(f"[NVD] Rate limited. Waiting 30s...")
                time.sleep(30)
    
    print(f"[NVD] Enriched {enriched}/{len(cves)} CVEs")
    return events


# ===================================================================
# RSS INGESTION
# ===================================================================

def fetch_rss():
    """Fetch and parse RSS feeds."""
    print(f"[RSS] Fetching {len(CONFIG['rss_feeds'])} feeds...")
    
    all_articles = []
    for feed in CONFIG['rss_feeds']:
        try:
            req = urllib.request.Request(feed['url'], headers={'User-Agent': 'CICC/1.0'})
            resp = urllib.request.urlopen(req, timeout=15)
            xml_content = resp.read().decode('utf-8')
            
            root = ET.fromstring(xml_content)
            channel = root.find('channel')
            if channel is None:
                continue
            
            items = channel.findall('item')
            for item in items:
                all_articles.append({
                    'title': item.findtext('title', ''),
                    'link': item.findtext('link', ''),
                    'published': item.findtext('pubDate', ''),
                    'description': (item.findtext('description', '') or '')[:300],
                    'source': feed['name'],
                    'category': feed['category'],
                })
            
            print(f"[RSS] {feed["name"]}: {len(items)} articles")
        except Exception as e:
            print(f"[RSS] {feed["name"]}: FAILED ({e})")
    
    print(f"[RSS] Total articles: {len(all_articles)}")
    return all_articles


# ===================================================================
# MAIN PIPELINE
# ===================================================================

def run_pipeline(sources=None, days=30):
    """Run the full ingestion pipeline."""
    log = {'started': datetime.now().isoformat(), 'sources': {}, 'errors': []}
    
    if sources is None:
        sources = ['kev', 'nvd', 'rss']
    
    output_dir = Path(CONFIG['output_dir'])
    
    # --- CISA KEV ---
    kev_events = []
    if 'kev' in sources:
        try:
            kev_events, version, total = fetch_kev(days)
            log['sources']['kev'] = {'status': 'OK', 'events': len(kev_events), 'version': version, 'total': total}
        except Exception as e:
            log['errors'].append(f"KEV: {e}")
            log['sources']['kev'] = {'status': 'FAILED', 'error': str(e)}
    
    # --- NVD Enrichment ---
    if 'nvd' in sources and kev_events:
        try:
            kev_events = enrich_nvd(kev_events)
            log['sources']['nvd'] = {'status': 'OK', 'enriched': len([e for e in kev_events if e.get('cvss')])}
        except Exception as e:
            log['errors'].append(f"NVD: {e}")
            log['sources']['nvd'] = {'status': 'FAILED', 'error': str(e)}
    
    # --- RSS Feeds ---
    rss_events = []
    if 'rss' in sources:
        try:
            articles = fetch_rss()
            # Normalize articles to events (simplified)
            for art in articles:
                combined = f"{art['title']} {art['description']}".lower()
                cves = re.findall(r'CVE-\d{4}-\d{4,7}', combined, re.IGNORECASE)
                match = correlate_watchlist('', '', combined)
                rss_events.append({
                    'id': f"RSS-{hash(art['link'])%100000:05d}",
                    'title': art['title'],
                    'summary': art['description'],
                    'type': 'Vulnerability' if any(w in combined for w in ['vulnerability','cve-','flaw','exploit']) else 'Campaign' if any(w in combined for w in ['ransomware','breach','malware','attack']) else 'Research',
                    'cves': [c.upper() for c in cves],
                    'source': art['source'],
                    'sourceUrl': art['link'],
                    'published': art['published'],
                    'relationship': match['relationship'],
                    'matchedTech': match['matched_tech'],
                    'sourceConfidence': 'Medium',
                })
            log['sources']['rss'] = {'status': 'OK', 'articles': len(articles), 'events': len(rss_events)}
        except Exception as e:
            log['errors'].append(f"RSS: {e}")
            log['sources']['rss'] = {'status': 'FAILED', 'error': str(e)}
    
    # --- Calculate Relevance ---
    for event in kev_events + rss_events:
        event['orgRelevance'] = calculate_relevance(event)
        s = event['orgRelevance']
        event['relevanceClass'] = 'Critical' if s >= 90 else 'High' if s >= 75 else 'Medium' if s >= 50 else 'Low' if s >= 25 else 'Informational'
    
    # --- Write Output ---
    if kev_events:
        kev_output = {
            'metadata': {'generated': datetime.now().isoformat(), 'source': 'CISA KEV + NVD', 'eventsInWindow': len(kev_events), 'nvdEnriched': True, 'nvdEnrichedCount': len([e for e in kev_events if e.get('cvss')])},
            'summary': {'totalEvents': len(kev_events), 'directMatches': len([e for e in kev_events if e['relationship']=='DIRECT'])},
            'events': sorted(kev_events, key=lambda x: x['orgRelevance'], reverse=True),
        }
        with open(output_dir / 'data_cisa_kev.json', 'w') as f:
            json.dump(kev_output, f, indent=2)
    
    if rss_events:
        rss_output = {
            'metadata': {'generated': datetime.now().isoformat(), 'totalArticles': len(rss_events)},
            'summary': {'totalEvents': len(rss_events), 'directMatches': len([e for e in rss_events if e['relationship']=='DIRECT'])},
            'events': sorted(rss_events, key=lambda x: x['orgRelevance'], reverse=True),
        }
        with open(output_dir / 'data_rss_feeds.json', 'w') as f:
            json.dump(rss_output, f, indent=2)
    
    # --- Pipeline Log ---
    log['completed'] = datetime.now().isoformat()
    log['totalEvents'] = len(kev_events) + len(rss_events)
    with open(output_dir / 'pipeline_log.json', 'w') as f:
        json.dump(log, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"PIPELINE COMPLETE")
    print(f"  KEV Events: {len(kev_events)}")
    print(f"  RSS Events: {len(rss_events)}")
    print(f"  Total: {len(kev_events) + len(rss_events)}")
    print(f"  Errors: {len(log['errors'])}")
    print(f"{'='*50}")




# ===================================================================
# MITRE ATT&CK MAPPING (Phase 2)
# ===================================================================

CWE_TO_ATTACK = {
    'CWE-78': {'techniques': ['T1059'], 'tactic': 'Execution'},
    'CWE-89': {'techniques': ['T1190'], 'tactic': 'Initial Access'},
    'CWE-287': {'techniques': ['T1078'], 'tactic': 'Initial Access'},
    'CWE-415': {'techniques': ['T1203'], 'tactic': 'Execution'},
    'CWE-416': {'techniques': ['T1203'], 'tactic': 'Execution'},
    'CWE-787': {'techniques': ['T1203'], 'tactic': 'Execution'},
    'CWE-1390': {'techniques': ['T1078'], 'tactic': 'Initial Access'},
    'CWE-502': {'techniques': ['T1059'], 'tactic': 'Execution'},
    'CWE-22': {'techniques': ['T1083'], 'tactic': 'Discovery'},
}

def map_mitre(event):
    """Map event to MITRE ATT&CK."""
    tactics = set()
    techniques = []
    for cwe in event.get('cwes', []):
        if cwe in CWE_TO_ATTACK:
            m = CWE_TO_ATTACK[cwe]
            tactics.add(m['tactic'])
            techniques.append({'id': m['techniques'][0], 'tactic': m['tactic']})
    vector = event.get('cvssVector', '') or ''
    if 'AV:N' in vector: tactics.add('Initial Access')
    elif 'AV:L' in vector: tactics.add('Privilege Escalation')
    return {'tactics': sorted(list(tactics)), 'techniques': techniques}


# ===================================================================
# IOC ENRICHMENT (Phase 2) -- abuse.ch APIs (POST)
# ===================================================================

def fetch_iocs(cve_id):
    """Query ThreatFox for IOCs associated with a CVE."""
    import urllib.request
    url = "https://threatfox-api.abuse.ch/api/v1/"
    payload = json.dumps({"query": "search_ioc", "search_term": cve_id}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'CICC/1.0'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        if data.get('query_status') == 'ok':
            return data.get('data', [])
    except Exception as e:
        print(f"  [IOC] ThreatFox error for {cve_id}: {e}")
    return []

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='CICC Intelligence Ingestion Pipeline')
    parser.add_argument('--source', choices=['kev','nvd','rss','all'], default='all')
    parser.add_argument('--days', type=int, default=30)
    args = parser.parse_args()
    
    sources = ['kev','nvd','rss'] if args.source == 'all' else [args.source]
    run_pipeline(sources=sources, days=args.days)
