---
name: run-audit-helper
description: MANDATORY. This skill MUST be used whenever a user asks to generate an audit report or audit scope report. Requires maintaining a "Current State" checklist in every response to ensure Framework and GCS Bucket are both identified.
license: Apache-2.0
---

# Run Audit Helper

**MANDATORY**: Use this skill WHENEVER a user asks to generate an audit report or audit scope report. Do NOT call the generation tools directly without ensuring all parameters (Framework, Scope, GCS Bucket) are valid and confirmed.

## 0. Current State Check (CRITICAL)

At the beginning of **EVERY** response while using this skill, you MUST output a "Current State" block to track progress. This ensures no requirements are forgotten during long conversations.

**Current State:**
*   **Goal:** [Audit Report / Scope Report]
*   **Scope:** [Project/Folder/Org ID] or [Not Set]
*   **Framework:** [Selected Framework] or [Not Set]
*   **GCS Bucket:** [Selected Bucket URI] or [Not Set] (Required for Audit Report, Optional for Scope Report)
*   **Missing:** [List what is still needed]

---

## 1. Identify the Goal

Determine if the user wants a full audit report (`generate_audit_report`) or just a scope report (`generate_audit_scope_report`).

*   **Examples of triggers:**
    *   "Run an audit report for my project"
    *   "Generate a compliance report"
    *   "I need to check compliance for folder X"
    *   "Create an audit scope report"

## 2. Iterative Discovery

Do not proceed to execution until **ALL** required fields in the "Current State" are set.

### If Framework is Missing:
1.  Ensure you have the Organization ID. If not, ask the user for it.
2.  Call `list_frameworks(organization_id=...)` to retrieve available frameworks.
3.  Present the list to the user and ask them to select the appropriate framework.

### If GCS Bucket is Missing (And Goal is Audit Report):
1.  Identify the target scope (Project, Folder, or Organization). If not provided, ask the user for it.
2.  Call `get_resource_enrollment_status(parent=...)` for that scope.
3.  Examine the output for enrolled destinations. Look for fields such as `destinations`, `eligibleDestinations`, or `gcsBuckets`.
    *   These fields will typically contain GCS bucket URIs (e.g., `gs://my-bucket`).
4.  **Present Enrolled Buckets**: Present these buckets to the user and ask them to select one.
    *   **CRITICAL DO NOT USE `gcloud`**: Do NOT use `gcloud storage ls` or similar CLI commands to find buckets. You must ONLY use the `get_resource_enrollment_status` tool to find buckets that are actually enrolled and valid for this operation. Random buckets found via CLI will likely fail the audit generation process.
5.  **Option:** Allow the user to provide a new bucket URI if none of the listed ones are suitable.

## 3. Final Confirmation & Execution

Once the "Missing" list in your Current State check is EMPTY:

1.  Confirm the final details with the user.
2.  Call the appropriate tool:
    *   `generate_audit_report(scope=..., gcs_uri=..., compliance_standard=..., location=...)`
    *   `generate_audit_scope_report(scope=..., compliance_standard=..., location=...)`