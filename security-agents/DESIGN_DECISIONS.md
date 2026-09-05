# Security Tool SME Agents — Design Decisions

This document explains why the security operations agents were built as seven separate vendor-specific specialists rather than one general-purpose security assistant, how their knowledge bases are structured, and what was learned building and maintaining a fleet of them.

---

## Why Vendor-Specific SME Agents Instead of One General Agent

The core decision was to build seven narrow, deep agents — one each for Splunk, Arctic Wolf, Microsoft Purview, SecurityScorecard, Darktrace, Palo Alto Networks, and SentinelOne — rather than a single broad security agent that tries to cover everything.

### The problem with a single general agent

A general security agent sounds appealing: one interface, one place to ask questions. In practice it fails on depth. Each security platform has its own query language, its own console workflows, its own alert semantics, and its own remediation patterns. A generalist agent produces plausible-sounding but shallow answers — it knows *about* Splunk SPL, but it cannot write a correct, optimized, non-obvious SPL query the way a specialist can. For operational security work, shallow is worse than useless: it is confidently wrong at the exact moment precision matters.

### The specialist advantage

A vendor-specific agent can hold the entire operational surface of one platform in its knowledge base — the query language down to edge-case syntax, the console navigation, the alert taxonomy, the tuning procedures, and the vendor's specific remediation guidance. When an analyst asks the Splunk agent to explain a notable event or tune a noisy correlation search, it answers with the precision of someone who has that console open right now. That depth is only possible because the agent's scope is deliberately narrow.

### The rationale in one sentence

Security operations rewards depth over breadth, so the fleet was optimized for depth — seven specialists that are each authoritative in their domain, rather than one generalist that is mediocre everywhere.

---

## Knowledge Base Architecture

Every agent in the fleet is backed by a consistent three-part knowledge base. This uniformity is what makes the fleet maintainable despite covering seven very different platforms.

### 1. Operational knowledge

The day-to-day reference: what the platform does, how its major features work, how alerts and events are structured, and how an analyst actually uses it. This is the "how the tool behaves" layer — the context an agent needs to interpret what a user is describing.

### 2. Query language reference

Each platform has a distinct query or policy language — SPL for Splunk, DVQL for SentinelOne, Data Explorer syntax for Arctic Wolf, PAN-OS constructs for Palo Alto, and so on. This layer captures the syntax, common patterns, functions, and the non-obvious gotchas that separate a query that runs from a query that runs correctly and efficiently. It is the layer most responsible for the specialist's precision.

### 3. Remediation playbooks

The action layer: given a finding, what are the concrete steps to investigate and resolve it? Playbooks cover tuning procedures, response workflows, escalation paths, and the vendor-specific mechanics of implementing a fix. This is what makes the agent useful beyond explanation — it moves the analyst from "what is this" to "what do I do."

### Why the three-part split works

Separating operational knowledge, query language, and remediation keeps each concern independently updatable. When a vendor changes its query syntax, only the query reference needs revision. When a remediation procedure changes, only the playbook layer changes. The consistent structure across all seven agents also means the pattern is teachable and reproducible — an eighth agent for a new platform follows the same template.

---

## Programmatic Agent Generation

The fleet is not seven hand-built one-offs. A builder pattern generates each agent from the same structural template, populating the three knowledge base layers per vendor. This was a deliberate choice with significant consequences.

### The benefit

Generating agents from a common template guarantees consistency — every agent has the same knowledge structure, the same interaction patterns, and the same quality bar. It also makes the fleet extensible: adding a new vendor SME is a matter of supplying the vendor's operational knowledge, query reference, and playbooks, not architecting a new agent from scratch. The marginal cost of the eighth, ninth, or tenth agent is low precisely because the pattern is programmatic.

### The trade-off

A templated approach can produce agents that feel uniform when a platform genuinely warrants a different shape. The mitigation is that the template defines structure, not content — the depth and specificity live in the per-vendor knowledge, which is free to be as idiosyncratic as the platform requires.

---

## Trade-offs

### Depth vs. breadth

The fleet chose depth. The consequence is that a question spanning multiple platforms requires consulting multiple agents rather than one. This was accepted because cross-platform questions are the minority, and because the depth on single-platform questions — the majority of operational work — is dramatically better. Breadth is recoverable by consulting several specialists; depth is not recoverable from a generalist.

### The maintenance burden of seven agents

Seven agents mean seven knowledge bases to keep current as vendors ship changes. This is a real, ongoing cost. It was judged acceptable for two reasons: the three-part knowledge structure localizes most updates to a single layer, and the value of accurate, deep guidance in daily security operations justifies the upkeep. A fleet that is out of date is a liability, so maintenance is treated as a first-class responsibility, not an afterthought.

### Uniform interface vs. platform-native fidelity

Presenting seven agents through a consistent interface aids usability but can slightly abstract away platform-native quirks. The knowledge base layers counter this by preserving vendor-specific detail even when the interface is uniform.

---

## Lessons Learned

### Vendor documentation has gaps, and the gaps are where value lives

Official vendor documentation reliably covers the happy path and reliably omits the operational reality — the tuning tricks, the query patterns that actually perform, the undocumented console behaviors. The most valuable knowledge in each agent is precisely the material that is not in the vendor's docs. Building these agents meant capturing operational know-how, not transcribing manuals.

### Query languages differ more than expected

The seven platforms' query and policy languages are conceptually similar but syntactically incompatible in ways that trip up anyone moving between them. A pattern that is idiomatic in one language is an error in another. Keeping the query reference as a distinct, per-agent layer was essential — there is no shared query knowledge to factor out, because the languages genuinely do not share it.

### Consistency of structure is what makes a fleet maintainable

The single most important lesson is that a fleet of specialists is only sustainable if they share a rigid structural template. Without the consistent three-part knowledge base, seven agents would be seven separate maintenance problems. With it, they are one pattern applied seven times — and the eighth is cheap.

### Narrow scope is a feature, not a limitation

It is tempting to let a well-performing agent expand its scope. Resisting that — keeping each agent tightly bounded to its platform — is what preserves the depth that makes it valuable. Scope discipline is an ongoing design choice, not a one-time decision.
