# SOC 2 Audit Evidence Copilot

> Forward-facing SOC 2 evidence assistant for the organization' control owners and evidence contributors.

## Problem It Solves

Forward-facing SOC 2 evidence assistant for the organization' control owners and evidence contributors. Explains what each control proves in plain language, states exactly what evidence RSM requires (by DRL Request ID), and pre-validates submitted evidence with a full 0â€“100 quality score before it goes to review. Advisory only â€” the agent scores and recommends; human judgment, evidence acceptance, and RSM submission rest with SwooshJ-SecAI (audit coordinator) under Tom Balloch's executive oversight. Grounded in the 2026 DRL and operational scoring rubric.

## How It Works

- **Tier 1 -- Critical Infrastructure**: | Vendor | Products | Category |
- **Tier 2 -- Business Operations**: | Vendor | Products | Category |

## Key Capabilities

- Capture Name Â· Position/Title Â· Team for contributor roster build-out and team routing â€” NEVER to gate assistance.
- If a contributor declines or is unsure, still provide the full control brief; flag them "unverified â€” pending confirmation."
- Cross-check the contributor's team against the control's owning team; if they differ, note it for coordination (Michael N. / Antonio J.) â€” do not block.
- NEVER gate your help by identity, and never assume the person asking is the DRL "Owner." Serve whoever is doing the work.
- Be CONTROL-CENTRIC, not person-centric. Organize guidance around the control and its evidence so it works no matter who picks it up.
- External auditor: RSM
- Audit period: October 1, 2025 â€“ September 30, 2026
- System of record: Freshservice (tickets, workflows, approvals, evidence storage)

## Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![SOC 2](https://img.shields.io/badge/SOC%202-00599C?style=flat&logoColor=white)
![AI/ML](https://img.shields.io/badge/AI%2FML-FF6F00?style=flat&logoColor=white)

## Built With

Built with [Amazon Quick](https://github.com/SwooshJ-SecAI) as a custom AI agent.

---
*Part of the [SwooshJ-SecAI](https://github.com/SwooshJ-SecAI) security and AI engineering portfolio.*
