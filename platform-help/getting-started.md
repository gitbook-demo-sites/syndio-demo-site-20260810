---
description: "Launch checklist for a new Syndio workspace."
icon: rocket
---


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
