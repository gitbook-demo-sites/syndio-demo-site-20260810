---
description: "Representative governance model for Syndi AI answers."
icon: sparkles
---


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
