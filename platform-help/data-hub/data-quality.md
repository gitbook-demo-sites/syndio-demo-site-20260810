---
description: "How to resolve common data validation issues."
icon: list-check
---


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
