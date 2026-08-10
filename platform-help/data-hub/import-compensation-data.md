---
description: "Representative Data Hub import workflow."
icon: database
---


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
