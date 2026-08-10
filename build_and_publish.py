from __future__ import annotations

import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
BASE = "https://api.gitbook.com/v1"
ORG_ID = "2XFwdcndEPA4ImZSPBqU"
SITE_TITLE = "Syndio Knowledge Base"
SITE_BASENAME = "syndio-knowledge-base"
REPO_OWNER = "gitbook-demo-sites"
REPO = "syndio-demo-site-20260810"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO}.git"
RAW = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main"


SPACES = [
    {
        "key": "HOME",
        "sentinel": "XSPACE_HOME",
        "folder": "home",
        "title": "Home",
        "icon": "house",
        "path": "home",
        "description": "External knowledge-base front door for Syndio customers.",
    },
    {
        "key": "HELP",
        "sentinel": "XSPACE_HELP",
        "folder": "platform-help",
        "title": "Platform Help",
        "icon": "circle-question",
        "path": "platform-help",
        "description": "Customer-facing setup, pay equity, decisions, AI, and integration help.",
    },
    {
        "key": "TRUST",
        "sentinel": "XSPACE_TRUST",
        "folder": "trust-releases",
        "title": "Trust & Releases",
        "icon": "shield-check",
        "path": "trust-releases",
        "description": "Security, compliance, transparency-readiness, FAQ, and release notes.",
    },
]


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + "\n", encoding="utf-8")


def api(method: str, path: str, body: Any | None = None, expected: tuple[int, ...] = (200, 201, 204)) -> tuple[int, Any]:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {os.environ['GITBOOK_TOKEN']}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            text = resp.read().decode()
            payload = json.loads(text) if text else None
            if resp.status not in expected:
                raise RuntimeError(f"{method} {path} returned {resp.status}: {text}")
            return resp.status, payload
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"{method} {path} returned {exc.code}: {detail}") from exc


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, check=check)


def fm(description: str, icon: str, *, wide: bool = False, cover: str | None = None) -> str:
    lines = ["---", f"description: {json.dumps(description)}", f"icon: {icon}"]
    if cover:
        lines.extend([f"cover: {cover}", "coverY: 0"])
    if wide:
        lines.extend(
            [
                "layout:",
                "  width: wide",
                "  cover:",
                "    visible: true",
                "    size: hero",
                "  title:",
                "    visible: true",
                "  description:",
                "    visible: true",
                "  tableOfContents:",
                "    visible: false",
                "  outline:",
                "    visible: false",
                "  pagination:",
                "    visible: false",
            ]
        )
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def gitbook_yaml() -> str:
    return """
root: ./
structure:
  readme: README.md
  summary: SUMMARY.md
"""


def vars_yaml() -> str:
    return """
support_email: support@syndio.example
trust_center: https://trust.synd.io
login_url: https://auth.synd.io
demo_note: "Representative demo content only"
"""


def wordmark_svg(fill: str, subtitle: str = "") -> str:
    sub = f'<text x="14" y="52" fill="{fill}" opacity="0.72" font-family="Arial, Helvetica, sans-serif" font-size="13">{subtitle}</text>' if subtitle else ""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="64" viewBox="0 0 300 64" role="img" aria-labelledby="title">
  <title id="title">Syndio Knowledge Base</title>
  <rect width="300" height="64" rx="14" fill="none"/>
  <text x="10" y="41" fill="{fill}" font-family="Instrument Sans, Arial, Helvetica, sans-serif" font-size="43" font-weight="800" letter-spacing="1">SYNDIO</text>
  <circle cx="207" cy="27" r="7" fill="#01AB01"/>
  {sub}
</svg>
"""


def cover_svg() -> str:
    return """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 720" role="img" aria-labelledby="title desc">
  <title id="title">Syndio knowledge base cover</title>
  <desc id="desc">A pay decision knowledge base with equity, decision, trust, and AI guidance cards.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#015559"/>
      <stop offset="0.54" stop-color="#008489"/>
      <stop offset="1" stop-color="#D8F4F6"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="720" fill="url(#bg)"/>
  <path d="M116 545C262 346 462 277 706 338c259 65 408 10 538-146 61-73 121-114 203-129" fill="none" stroke="#01AB01" stroke-width="28" stroke-linecap="round" opacity=".82"/>
  <g transform="translate(130 122)">
    <rect width="590" height="370" rx="32" fill="#1F1E1D" opacity=".92"/>
    <text x="54" y="94" fill="#FFFFFF" font-family="Instrument Sans, Arial, Helvetica, sans-serif" font-size="48" font-weight="800">Every pay decision,</text>
    <text x="54" y="150" fill="#FFFFFF" font-family="Instrument Sans, Arial, Helvetica, sans-serif" font-size="48" font-weight="800">guided.</text>
    <text x="56" y="213" fill="#D8F4F6" font-family="Instrument Sans, Arial, Helvetica, sans-serif" font-size="23">Customer knowledge for pay equity,</text>
    <text x="56" y="248" fill="#D8F4F6" font-family="Instrument Sans, Arial, Helvetica, sans-serif" font-size="23">decision governance, AI, and trust.</text>
    <rect x="56" y="298" width="172" height="46" rx="23" fill="#01AB01"/>
    <rect x="250" y="298" width="190" height="46" rx="23" fill="#D8F4F6"/>
    <text x="86" y="327" fill="#102020" font-family="Instrument Sans, Arial, Helvetica, sans-serif" font-size="17" font-weight="700">Start here</text>
    <text x="283" y="327" fill="#015559" font-family="Instrument Sans, Arial, Helvetica, sans-serif" font-size="17" font-weight="700">Search answers</text>
  </g>
  <g transform="translate(860 140)">
    <rect width="520" height="390" rx="34" fill="#FFFFFF" opacity=".96"/>
    <rect x="46" y="46" width="250" height="18" rx="9" fill="#015559"/>
    <rect x="46" y="88" width="420" height="12" rx="6" fill="#D8F4F6"/>
    <rect x="46" y="126" width="350" height="12" rx="6" fill="#D8F4F6"/>
    <rect x="46" y="188" width="124" height="112" rx="20" fill="#EFFAFB"/>
    <rect x="198" y="188" width="124" height="112" rx="20" fill="#F4FFF4"/>
    <rect x="350" y="188" width="124" height="112" rx="20" fill="#F6F5FF"/>
    <circle cx="108" cy="238" r="21" fill="#008489"/>
    <circle cx="260" cy="238" r="21" fill="#01AB01"/>
    <circle cx="412" cy="238" r="21" fill="#260E3C"/>
  </g>
</svg>
"""


def card(icon: str, title: str, desc: str, href: str) -> str:
    return f'<tr><td><h3><i class="fa-{icon}"></i></h3></td><td><strong>{title}</strong></td><td>{desc}</td><td><a href="{href}">{title}</a></td></tr>'


def scaffold() -> None:
    write("README.md", f"# {REPO}\n\nSource for the Syndio GitBook demo site. Each top-level folder maps to one GitBook space.\n")
    write(".gitignore", ".DS_Store\nThumbs.db\n*.swp\n*.swo\n.idea/\n.vscode/\n__pycache__/\n")
    write("assets/syndio-wordmark-light.svg", wordmark_svg("#FFFFFF", "knowledge base"))
    write("assets/syndio-wordmark-dark.svg", wordmark_svg("#1F1E1D", "knowledge base"))
    write("assets/syndio-cover.svg", cover_svg())
    for item in SPACES:
        write(f"{item['folder']}/.gitbook.yaml", gitbook_yaml())
        write(f"{item['folder']}/.gitbook/vars.yaml", vars_yaml())

    write(
        "home/README.md",
        fm("A Syndio-styled external knowledge-base homepage for customer education and support.", "house", wide=True, cover="../assets/syndio-cover.svg")
        + f"""
# Syndio Knowledge Base

Everything customers need to set up pay equity analysis, govern high-stakes pay decisions, and understand the trust model behind Syndio.

{{% hint style="info" icon="circle-info" %}}
This is first-draft demo content extrapolated from Syndio's public marketing site. It is not official Syndio documentation.
{{% endhint %}}

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
{card("rocket", "Start here", "Set up access, invite teams, and prepare the data foundation for your first pay equity review.", "https://app.gitbook.com/s/XSPACE_HELP/getting-started")}
{card("scale-balanced", "Pay equity foundation", "Run analysis, review drivers, and prepare defensible reporting workflows for global teams.", "https://app.gitbook.com/s/XSPACE_HELP/essentials/pay-equity-analysis")}
{card("route", "Govern pay decisions", "Guide offers, promotions, merit changes, and transfers before decisions create downstream risk.", "https://app.gitbook.com/s/XSPACE_HELP/decisions/offer-governance")}
{card("shield-check", "Trust & releases", "Security, compliance, transparency readiness, AI governance, and product update notes.", "https://app.gitbook.com/s/XSPACE_TRUST/")}
</tbody></table>

{{% columns %}}
{{% column width="50%" %}}
## Built around customer jobs

The site is organized for compensation leaders, HR operations, talent teams, legal partners, and admins who need a reliable answer while a pay decision is moving.
{{% endcolumn %}}

{{% column width="50%" %}}
## Built for Syndio customers

The front door gives customers a branded hero, path cards, strong top navigation, AI-ready content, and a clear sign-in action in the header.
{{% endcolumn %}}
{{% endcolumns %}}
""",
    )
    write(
        "home/SUMMARY.md",
        """
# Table of contents

* [Syndio Knowledge Base](README.md)
* [Customer journeys](customer-journeys.md)
* [Demo review notes](demo-review-notes.md)
""",
    )
    write(
        "home/customer-journeys.md",
        fm("Suggested reader journeys through the demo knowledge base.", "route")
        + """
# Customer journeys

Use these paths to demo how a customer would move from question to action.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><i class="fa-user-tie"></i></td><td><strong>Comp leader</strong></td><td>Prepare analysis, inspect risk drivers, and approve governed decisions.</td><td><a href="https://app.gitbook.com/s/XSPACE_HELP/essentials/pay-equity-analysis">Comp leader</a></td></tr>
<tr><td><i class="fa-briefcase"></i></td><td><strong>Talent partner</strong></td><td>Submit an offer decision, interpret guidance, and understand escalations.</td><td><a href="https://app.gitbook.com/s/XSPACE_HELP/decisions/offer-governance">Talent partner</a></td></tr>
<tr><td><i class="fa-gavel"></i></td><td><strong>Legal partner</strong></td><td>Review defensibility, audit trail requirements, and pay transparency readiness.</td><td><a href="https://app.gitbook.com/s/XSPACE_TRUST/transparency-compliance">Legal partner</a></td></tr>
<tr><td><i class="fa-gears"></i></td><td><strong>Admin</strong></td><td>Manage roles, data imports, integrations, and workspace controls.</td><td><a href="https://app.gitbook.com/s/XSPACE_HELP/admin/roles-and-permissions">Admin</a></td></tr>
</tbody></table>
""",
    )
    write(
        "home/demo-review-notes.md",
        fm("Assumptions and review notes for the Syndio demo draft.", "clipboard-check")
        + """
# Demo review notes

## Assumptions

- The demo is for an external-facing customer knowledge base, not an internal employee handbook.
- Content is intentionally representative and should be replaced with product-accurate help-center material later.
- The top-right `Login` button points to `https://auth.synd.io`.
- The site uses share-link visibility for review.

## Feedback areas

- Confirm whether the main customer paths should prioritize compensation leaders or product admins.
- Replace dummy workflow names with real Syndio product terms where needed.
- Add real screenshots or short product clips if Syndio wants the homepage to feel closer to production.
""",
    )

    write(
        "platform-help/README.md",
        fm("Customer-facing setup and product help for Syndio.", "circle-question")
        + f"""
# Platform Help

Set up Syndio, prepare compensation data, run pay equity workflows, guide pay decisions, and connect the platform to the systems where decisions happen.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
{card("rocket", "Getting started", "Access, workspace setup, launch checklist, and first analysis preparation.", "getting-started.md")}
{card("database", "Data Hub", "Import employee, job, pay, and decision data with clear validation rules.", "data-hub/import-compensation-data.md")}
{card("scale-balanced", "Essentials", "Pay equity analysis, pay gap reporting, and global transparency preparation.", "essentials/pay-equity-analysis.md")}
{card("route", "Decisions", "Offer, promotion, merit, and transfer decision guidance in real time.", "decisions/offer-governance.md")}
{card("sparkles", "Syndi AI", "Use AI-generated explanations while keeping human review and policy context in control.", "syndi-ai/answer-governance.md")}
{card("plug", "Integrations", "Connect HRIS, ATS, compensation planning, and analytics systems.", "integrations/systems-overview.md")}
</tbody></table>
""",
    )
    write(
        "platform-help/SUMMARY.md",
        """
# Table of contents

* [Platform Help](README.md)
* [Getting started](getting-started.md)

## Data foundation

* [Import compensation data](data-hub/import-compensation-data.md)
* [Resolve data quality issues](data-hub/data-quality.md)

## Essentials

* [Run pay equity analysis](essentials/pay-equity-analysis.md)
* [Prepare pay gap reporting](essentials/pay-gap-reporting.md)

## Decisions

* [Govern offer decisions](decisions/offer-governance.md)
* [Review promotion and merit guidance](decisions/promotion-merit-guidance.md)

## AI and administration

* [Syndi AI answer governance](syndi-ai/answer-governance.md)
* [Roles and permissions](admin/roles-and-permissions.md)
* [Systems overview](integrations/systems-overview.md)
""",
    )
    write(
        "platform-help/getting-started.md",
        fm("Launch checklist for a new Syndio workspace.", "rocket")
        + """
# Getting started

Use this checklist to move from workspace access to a first governed pay workflow.

{% stepper %}
{% step %}
### Confirm workspace access

Sign in through <code class="expression">space.vars.login_url</code>, verify your role, and confirm the correct business units are visible.
{% endstep %}

{% step %}
### Prepare source data

Identify HRIS, compensation planning, ATS, market data, and policy sources. Agree which system is authoritative for employee, job, pay, and decision records.
{% endstep %}

{% step %}
### Run the first validation

Upload or sync source files into Data Hub, resolve required-field issues, and review the data-quality summary with the compensation owner.
{% endstep %}

{% step %}
### Activate workflows

Start with pay equity analysis, then extend into offer, promotion, merit, or transfer guidance when the policy and market-data inputs are ready.
{% endstep %}
{% endstepper %}

{% hint style="success" icon="lightbulb" %}
Start narrow. A single job family or region is enough to validate data, permissions, and review flow before rolling out across the organization.
{% endhint %}
""",
    )
    write(
        "platform-help/data-hub/import-compensation-data.md",
        fm("Representative Data Hub import workflow.", "database")
        + """
# Import compensation data

Data Hub brings employee, job, pay, and decision inputs into one governed foundation for analysis and recommendations.

```mermaid
flowchart LR
    HRIS[HRIS employee data] --> DH[Data Hub]
    ATS[ATS offer data] --> DH
    Market[Market data] --> DH
    Policy[Pay policies] --> DH
    DH --> Validate[Validation and mapping]
    Validate --> Essentials[Essentials analysis]
    Validate --> Decisions[Decision guidance]
```

## Required data families

| Data family | Examples | Review owner |
| --- | --- | --- |
| Employee | Worker ID, location, manager, job family | HR operations |
| Job | Level, role, function, grade, FLSA status | Compensation |
| Pay | Base, bonus, currency, effective date | Total rewards |
| Decisions | Offer, promotion, merit, transfer request | Talent and managers |

{% hint style="warning" icon="triangle-exclamation" %}
Do not use free-text job titles as the only grouping field. Map them to a normalized job architecture before running analysis.
{% endhint %}
""",
    )
    write(
        "platform-help/data-hub/data-quality.md",
        fm("How to resolve common data validation issues.", "list-check")
        + """
# Resolve data quality issues

Syndio flags missing values, outliers, mismatched currencies, and inconsistent job mappings before data is used in analysis or decisions.

| Issue | Why it matters | Typical resolution |
| --- | --- | --- |
| Missing level | Employees may be compared against the wrong peer group. | Map to job architecture or exclude from a scoped run. |
| Stale pay date | Current compensation may not reflect the decision being reviewed. | Refresh from payroll or compensation planning. |
| Currency mismatch | Spend and risk calculations can be distorted. | Confirm exchange-rate date and source. |
| Unmapped manager | Approval path and accountability may be incomplete. | Sync manager hierarchy from HRIS. |

<details>
<summary>When to exclude records</summary>

Exclude a record only when the issue cannot be resolved before the analysis deadline and the exclusion rationale is documented for review.
</details>
""",
    )
    write(
        "platform-help/essentials/pay-equity-analysis.md",
        fm("Representative workflow for pay equity analysis.", "scale-balanced")
        + """
# Run pay equity analysis

Essentials gives compensation and legal teams a defensible view of pay equity across countries, job groups, and populations.

{% columns %}
{% column width="50%" %}
## What the analysis answers

- Where statistically significant gaps appear.
- Which drivers explain pay differences.
- Which groups require remediation planning.
- Which records require additional review.
{% endcolumn %}

{% column width="50%" %}
{% hint style="info" icon="gavel" %}
Legal review should confirm scope, privilege assumptions, remediation notes, and external reporting language before broader distribution.
{% endhint %}
{% endcolumn %}
{% endcolumns %}

## Analysis stages

```mermaid
flowchart TD
    Scope[Define scope] --> Validate[Validate data]
    Validate --> Model[Run analysis]
    Model --> Explain[Review drivers]
    Explain --> Remediate[Plan remediation]
    Remediate --> Report[Prepare reporting]
```
""",
    )
    write(
        "platform-help/essentials/pay-gap-reporting.md",
        fm("Representative pay transparency and reporting workflow.", "file-invoice")
        + """
# Prepare pay gap reporting

Use reporting workflows to prepare jurisdiction-specific outputs, review right-to-information readiness, and maintain the evidence trail behind published numbers.

## Reporting checklist

- Confirm reporting entities and employee populations.
- Validate compensation elements included in each jurisdiction.
- Review draft metrics with legal and compensation owners.
- Store assumptions, exclusions, and remediation plans with the final report.

{% hint style="success" icon="shield-check" %}
Keep published reports and internal analysis connected. Readers need concise public language, while legal and compensation teams need the underlying assumptions preserved.
{% endhint %}
""",
    )
    write(
        "platform-help/decisions/offer-governance.md",
        fm("How talent teams can govern offer decisions in Syndio.", "route")
        + """
# Govern offer decisions

Decisions helps talent and compensation teams check offers against policy, market data, internal equity, and budget impact before the offer is approved.

{% stepper %}
{% step %}
### Submit the proposed offer

Enter candidate location, role, level, offer amount, variable pay, and hiring manager context.
{% endstep %}

{% step %}
### Review the guidance

Syndio returns policy fit, equity signal, market range, budget impact, and explainable recommendation notes.
{% endstep %}

{% step %}
### Escalate if needed

If the recommendation requires review, route to compensation or legal with the context attached.
{% endstep %}

{% step %}
### Record the decision

Save final approval, rationale, and any exception reason so the decision can be defended later.
{% endstep %}
{% endstepper %}
""",
    )
    write(
        "platform-help/decisions/promotion-merit-guidance.md",
        fm("Representative promotion and merit review flow.", "people-arrows")
        + """
# Review promotion and merit guidance

Promotion and merit decisions should be checked before they create structural pay drift.

| Signal | What to review | Example action |
| --- | --- | --- |
| Internal equity | Similar employees in the same role and level | Adjust recommendation or document rationale. |
| Compression | Relationship to manager and peer pay | Review scope, tenure, and recent movements. |
| Budget | Team and department impact | Route for finance approval if threshold is exceeded. |
| Policy | Promotion, merit, and exception rules | Add exception note or request compensation review. |

{% hint style="info" icon="sparkles" %}
Use Syndi AI explanations as a drafting aid, then have the compensation owner confirm the final rationale.
{% endhint %}
""",
    )
    write(
        "platform-help/syndi-ai/answer-governance.md",
        fm("Representative governance model for Syndi AI answers.", "sparkles")
        + """
# Syndi AI answer governance

Syndi AI should help users understand the reasoning behind a pay recommendation without replacing the human decision owner.

## Answer contract

| Question type | Syndi can answer | Escalate when |
| --- | --- | --- |
| Policy fit | Which rule influenced the guidance | The policy source is missing or conflicting. |
| Equity signal | Why a proposed amount is high or low | A protected-class review is required. |
| Market context | How the amount compares with range | Market data is stale or unavailable. |
| Audit trail | What rationale was recorded | Legal privilege or litigation hold applies. |

{% hint style="warning" icon="circle-exclamation" %}
Syndi does not make pay decisions. It explains signals and guidance so accountable humans can decide with context.
{% endhint %}
""",
    )
    write(
        "platform-help/admin/roles-and-permissions.md",
        fm("Workspace roles and permission patterns.", "users-gear")
        + """
# Roles and permissions

Assign roles by job responsibility and review access before each analysis cycle.

| Role | Typical user | Access pattern |
| --- | --- | --- |
| Workspace admin | HRIS or compensation systems owner | Manage workspace settings, imports, and users. |
| Compensation owner | Total rewards leader | Configure analysis scope, policies, and review decisions. |
| Legal reviewer | Employment counsel | Review privileged analysis and reporting outputs. |
| Talent partner | Recruiting or HRBP user | Submit and review guided decisions. |
| Executive viewer | CHRO, CFO, board delegate | View approved summaries and dashboards. |

<details>
<summary>Recommended review cadence</summary>

Review access at launch, before each annual pay cycle, after major reorgs, and whenever privileged analysis is opened to a broader group.
</details>
""",
    )
    write(
        "platform-help/integrations/systems-overview.md",
        fm("Representative integration overview for Syndio.", "plug")
        + """
# Systems overview

Syndio sits between systems of record and the teams making pay decisions.

```mermaid
flowchart LR
    Workday[HRIS] --> Syndio
    ATS[ATS] --> Syndio
    Market[Market data] --> Syndio
    Comp[Comp planning] --> Syndio
    Syndio --> BI[Analytics and reporting]
    Syndio --> Audit[Decision audit trail]
```

## Integration principles

- Keep employee, job, and pay data anchored to systems of record.
- Sync decision events close to the moment the decision is made.
- Preserve mapping rules, timestamps, and import results for auditability.
- Separate configuration access from day-to-day decision review access.
""",
    )

    write(
        "trust-releases/README.md",
        fm("Trust, compliance, transparency, FAQ, and release-note content.", "shield-check")
        + f"""
# Trust & Releases

Security, compliance, AI governance, transparency readiness, and product updates for Syndio customers.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
{card("shield-halved", "Security model", "How customer data, integrations, access, and audit trails are protected.", "security-model.md")}
{card("globe", "Transparency compliance", "How teams prepare for pay transparency obligations and right-to-information workflows.", "transparency-compliance.md")}
{card("clock-rotate-left", "Release notes", "Representative product updates using GitBook's native updates block.", "release-notes.md")}
{card("circle-question", "FAQ", "Short answers for common customer and executive stakeholder questions.", "faq.md")}
</tbody></table>
""",
    )
    write(
        "trust-releases/SUMMARY.md",
        """
# Table of contents

* [Trust & Releases](README.md)
* [Security model](security-model.md)
* [Transparency compliance](transparency-compliance.md)
* [Release notes](release-notes.md)
* [FAQ](faq.md)
""",
    )
    write(
        "trust-releases/security-model.md",
        fm("Representative security and trust model for Syndio customers.", "shield-halved")
        + """
# Security model

Syndio handles sensitive compensation and workforce data, so customer controls need to be explicit and easy to audit.

## Control areas

| Area | Customer question | Demo answer |
| --- | --- | --- |
| Access | Who can see analysis and decision records? | Role-based access separates admins, compensation owners, legal reviewers, and viewers. |
| Data | How are imports validated? | Data Hub records mappings, validation results, and exceptions. |
| AI | Can AI explain a decision without deciding? | Syndi AI provides reasoning and context, with human ownership preserved. |
| Audit | Can we defend a decision later? | Final rationale, approver, timestamp, and exception notes are retained. |

{% hint style="info" icon="lock" %}
For production use, link this page to Syndio's live trust center at <code class="expression">space.vars.trust_center</code>.
{% endhint %}
""",
    )
    write(
        "trust-releases/transparency-compliance.md",
        fm("Representative compliance guidance for pay transparency readiness.", "globe")
        + """
# Transparency compliance

Pay transparency readiness combines accurate data, repeatable analysis, approved language, and a durable evidence trail.

```mermaid
flowchart TD
    Obligation[Identify jurisdiction obligation] --> Population[Confirm employee population]
    Population --> Metrics[Prepare metrics]
    Metrics --> Review[Legal and compensation review]
    Review --> Publish[Publish or respond]
    Publish --> Evidence[Store evidence trail]
```

## What to document

- Reporting entity and jurisdiction.
- Population, exclusions, and compensation elements.
- Analysis date and data snapshot.
- Approved external language.
- Remediation actions and owners.
""",
    )
    write(
        "trust-releases/release-notes.md",
        fm("Representative release notes for the Syndio demo.", "clock-rotate-left", wide=True)
        + """
# Release notes

{% updates format="full" %}
{% update date="2026-08-10" tags="ai,decisions" %}
## Explainable guidance for governed pay decisions

Added clearer rationale summaries for offer, promotion, merit, and transfer recommendations.
{% endupdate %}

{% update date="2026-07-22" tags="data,admin" %}
## Data Hub validation summary

Admins can now review required-field coverage, mapping issues, and currency mismatches before launching an analysis.
{% endupdate %}

{% update date="2026-06-18" tags="compliance" %}
## Pay transparency readiness workflow

Added jurisdiction-level task tracking and evidence notes for right-to-information preparation.
{% endupdate %}
{% endupdates %}
""",
    )
    write(
        "trust-releases/.gitbook/tags.yaml",
        """
- tag: ai
  label: AI
  icon: sparkles
- tag: decisions
  label: Decisions
  icon: route
- tag: data
  label: Data
  icon: database
- tag: admin
  label: Admin
  icon: users-gear
- tag: compliance
  label: Compliance
  icon: scale-balanced
""",
    )
    write(
        "trust-releases/faq.md",
        fm("Common customer questions for the Syndio knowledge base.", "circle-question")
        + """
# FAQ

<details>
<summary>Is Syndio only for annual pay equity analysis?</summary>

No. This demo frames Syndio as a continuous governance layer: pay equity analysis through Essentials, real-time decision guidance through Decisions, and explainability through Syndi AI.
</details>

<details>
<summary>Who owns a guided pay decision?</summary>

The accountable business, talent, compensation, or legal owner still owns the decision. Syndio provides context, guardrails, recommendations, and the audit trail.
</details>

<details>
<summary>Can customers use Syndio for EU Pay Transparency readiness?</summary>

The demo includes representative workflows for pay gap reporting, right-to-information preparation, evidence retention, and approved review paths.
</details>

<details>
<summary>Where should users sign in?</summary>

Use <code class="expression">space.vars.login_url</code>. The demo site's header also includes a Login button.
</details>
""",
    )


def ensure_repo() -> None:
    if not (ROOT / ".git").exists():
        run(["git", "init"])
        run(["git", "branch", "-M", "main"], check=False)
    remotes = subprocess.run(["git", "remote"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    if "origin" not in remotes:
        repo_check = subprocess.run(["gh", "repo", "view", f"{REPO_OWNER}/{REPO}"], cwd=ROOT, capture_output=True, text=True)
        if repo_check.returncode != 0:
            run(["gh", "repo", "create", f"{REPO_OWNER}/{REPO}", "--public", "--description", "Syndio GitBook demo site source", "--source", ".", "--remote", "origin"])
        else:
            run(["git", "remote", "add", "origin", REPO_URL])
    git_commit_push("Build Syndio demo site content")


def git_commit_push(message: str) -> None:
    run(["git", "add", "."])
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode != 0:
        run(["git", "commit", "-m", message])
    run(["git", "push", "-u", "origin", "main"])


def create_site() -> dict[str, Any]:
    created_path = ROOT / "gitbook-created.json"
    if created_path.exists():
        return json.loads(created_path.read_text(encoding="utf-8"))
    _, site = api("POST", f"/orgs/{ORG_ID}/sites", {"type": "ultimate", "title": SITE_TITLE, "visibility": "share-link"})
    site_id = site["id"]
    api("PATCH", f"/orgs/{ORG_ID}/sites/{site_id}", {"title": SITE_TITLE, "visibility": "share-link", "basename": SITE_BASENAME})
    created: dict[str, Any] = {"org": ORG_ID, "site": site_id, "spaces": {}, "sections": {}, "site_spaces": {}, "site_object": site}
    for item in SPACES:
        _, space = api("POST", f"/orgs/{ORG_ID}/spaces", {"title": item["title"], "empty": True, "editMode": "live"})
        space_id = space["id"]
        created["spaces"][item["key"]] = space_id
        _, section = api(
            "POST",
            f"/orgs/{ORG_ID}/sites/{site_id}/sections",
            {"spaceId": space_id, "title": item["title"], "icon": item["icon"], "draft": False},
        )
        section_id = section["id"]
        site_space_id = section["siteSpaces"][0]["id"]
        created["sections"][item["key"]] = section_id
        created["site_spaces"][item["key"]] = site_space_id
        api(
            "PATCH",
            f"/orgs/{ORG_ID}/sites/{site_id}/sections/{section_id}",
            {"path": item["path"], "description": item["description"], "draft": False, "defaultSiteSpace": site_space_id},
        )
    api("PATCH", f"/orgs/{ORG_ID}/sites/{site_id}", {"defaultSiteSection": created["sections"]["HOME"], "defaultSiteSpace": created["site_spaces"]["HOME"]})
    write("gitbook-created.json", json.dumps(created, indent=2))
    return created


def replace_sentinels(space_ids: dict[str, str]) -> None:
    replacements = {item["sentinel"]: space_ids[item["key"]] for item in SPACES}
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")


def import_spaces(created: dict[str, Any]) -> dict[str, Any]:
    imports: dict[str, Any] = {}
    for item in SPACES:
        status, _ = api(
            "POST",
            f"/spaces/{created['spaces'][item['key']]}/git/import",
            {
                "url": REPO_URL,
                "ref": "refs/heads/main",
                "repoProjectDirectory": item["folder"],
                "repoTreeURL": f"https://github.com/{REPO_OWNER}/{REPO}/tree/main",
                "repoCommitURL": f"https://github.com/{REPO_OWNER}/{REPO}/commit",
                "force": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            expected=(204,),
        )
        imports[item["key"]] = {"status": status, "space": created["spaces"][item["key"]], "folder": item["folder"]}
    write("gitbook-import-results.json", json.dumps(imports, indent=2))
    return imports


def customization_payload(created: dict[str, Any], share_url: str) -> dict[str, Any]:
    logo_light = f"{RAW}/assets/syndio-wordmark-dark.svg?v=2"
    logo_dark = f"{RAW}/assets/syndio-wordmark-light.svg?v=2"
    cover = f"{RAW}/assets/syndio-cover.svg"
    favicon = "https://synd.io/wp-content/uploads/2026/05/cropped-ms-icon-310x310-1-32x32.png"
    return {
        "title": SITE_TITLE,
        "localizedTitle": {},
        "internationalization": {"locale": "en"},
        "styling": {
            "theme": "clean",
            "primaryColor": {"light": "#01AB01", "dark": "#5BEB5B"},
            "infoColor": {"light": "#008489", "dark": "#66D9DE"},
            "successColor": {"light": "#01AB01", "dark": "#5BEB5B"},
            "warningColor": {"light": "#DD6420", "dark": "#FFAD7A"},
            "dangerColor": {"light": "#B42318", "dark": "#F97066"},
            "tint": {"color": {"light": "#D8F4F6", "dark": "#1F1E1D"}},
            "corners": "rounded",
            "depth": "flat",
            "links": "accent",
            "font": "ABCFavorit",
            "monospaceFont": "DMMono",
            "icons": "regular",
            "background": "plain",
            "sidebar": {"background": "filled", "list": "line"},
            "codeTheme": {
                "default": {"light": "default-light", "dark": "default-dark"},
                "openapi": {"light": "default-light", "dark": "default-dark"},
            },
            "search": "prominent",
        },
        "favicon": {"icon": {"light": favicon, "dark": favicon}},
        "header": {
            "preset": "default",
            "logo": {"light": logo_light, "dark": logo_dark},
            "links": [
                {"title": "Platform Help", "to": {"kind": "space", "space": created["spaces"]["HELP"]}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Trust & Releases", "to": {"kind": "space", "space": created["spaces"]["TRUST"]}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Syndio", "to": {"kind": "url", "url": "https://synd.io/"}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Login", "to": {"kind": "url", "url": "https://auth.synd.io"}, "style": "button-primary", "links": [], "localizedTitle": {}},
            ],
        },
        "footer": {
            "logo": {"light": logo_light, "dark": logo_dark},
            "groups": [
                {
                    "title": "Demo sections",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Home", "to": {"kind": "space", "space": created["spaces"]["HOME"]}, "localizedTitle": {}},
                        {"title": "Platform Help", "to": {"kind": "space", "space": created["spaces"]["HELP"]}, "localizedTitle": {}},
                        {"title": "Trust & Releases", "to": {"kind": "space", "space": created["spaces"]["TRUST"]}, "localizedTitle": {}},
                    ],
                },
                {
                    "title": "Sources",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Syndio homepage", "to": {"kind": "url", "url": "https://synd.io/"}, "localizedTitle": {}},
                        {"title": "Syndio login", "to": {"kind": "url", "url": "https://auth.synd.io"}, "localizedTitle": {}},
                        {"title": "Source repo", "to": {"kind": "url", "url": f"https://github.com/{REPO_OWNER}/{REPO}"}, "localizedTitle": {}},
                    ],
                },
            ],
            "copyright": "Syndio Knowledge Base demo - representative content for GitBook review.",
        },
        "themes": {"default": "light", "toggeable": True},
        "pdf": {"enabled": True},
        "feedback": {"enabled": True},
        "ai": {
            "mode": "assistant",
            "suggestions": [
                "How do I prepare data for pay equity analysis?",
                "How should a talent partner review offer guidance?",
                "What does Syndi AI explain and what needs human review?",
                "How do we prepare for pay transparency reporting?",
            ],
        },
        "advancedCustomization": {"enabled": True},
        "trademark": {"enabled": True},
        "externalLinks": {"target": "blank"},
        "pagination": {"enabled": True},
        "pageActions": {"externalAI": True, "markdown": True, "mcp": True, "items": ["assistant", "markdown", "external-ai", "mcp", "pdf"]},
        "git": {"showEditLink": False},
        "privacyPolicy": {"url": "https://synd.io/privacy-policy/"},
        "socialPreview": {"url": cover},
        "socialAccounts": [{"platform": "linkedin", "handle": "company/syndio", "display": {"footer": True, "header": False}}],
        "insights": {"trackingCookie": True},
        "announcement": {"enabled": True, "message": "First-draft Syndio knowledge-base demo with representative content.", "style": "info"},
    }


def apply_customization(created: dict[str, Any], share_url: str) -> None:
    _, customized = api("PUT", f"/orgs/{ORG_ID}/sites/{created['site']}/customization", customization_payload(created, share_url))
    write("gitbook-customization-result.json", json.dumps(customized, indent=2))


def main() -> None:
    if "GITBOOK_TOKEN" not in os.environ:
        raise SystemExit("GITBOOK_TOKEN is required")
    scaffold()
    ensure_repo()
    created = create_site()
    replace_sentinels(created["spaces"])
    git_commit_push("Resolve Syndio GitBook space links")
    imports = import_spaces(created)
    publish_status, publish = api("POST", f"/orgs/{ORG_ID}/sites/{created['site']}/publish", expected=(200, 201, 202, 204))
    share_status, share = api("POST", f"/orgs/{ORG_ID}/sites/{created['site']}/share-links", {"name": "Syndio demo review"})
    share_url = share["urls"]["published"]
    apply_customization(created, share_url)
    final = {
        "publish_status": publish_status,
        "publish": publish,
        "share_status": share_status,
        "share": share,
        "published_url": share_url,
        "app_url": publish["urls"]["app"],
        "preview_url": publish["urls"]["preview"],
        "repo": f"https://github.com/{REPO_OWNER}/{REPO}",
        "created": created,
        "imports": imports,
    }
    write("publish-result.json", json.dumps(final, indent=2))
    git_commit_push("Add Syndio GitBook publish artifacts")
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()
