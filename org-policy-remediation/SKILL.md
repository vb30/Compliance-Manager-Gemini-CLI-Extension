---
name: org-policy-violation-remediation
description: MANDATORY. This skill MUST be used whenever a user asks to fix an organization policy violation or when a violation is identified as an org policy violation.
license: Apache-2.0
---

# Org Policy Violation Remediation

**MANDATORY**: Use this skill WHENEVER a user asks to fix a violation and it is identified as an organization policy violation, or when they directly ask to fix an organization policy violation. Do NOT call remediation tools or execute commands directly without presenting the impact summary and obtaining confirmation.

## 1. Get Violation Details
First, use the `get_violation` tool to retrieve the details of the violation.
Extract the constraint name (e.g., `constraints/gcp.restrictServiceUsage`) and any remediation steps.

### 2. Analyze Current State and Affected Resources
Before applying any fix, you MUST understand the current policy and what resources are currently in use within the scope.

**2a. Check Current Policy State**
Run the following command to see the existing organization policy:
`gcloud org-policies describe[Constraint_Name] --[folder|project|organization]=[ID]`
*(Note: Strip the `constraints/` prefix from the constraint name if necessary).*
*Analysis:* Compare the current policy with the required remediation to determine the exact delta.

**2b. Search Affected Resources (Tailored by Constraint)**
Use Cloud Asset Inventory (CAIS) to assess the footprint. To prevent output truncation on large environments, use the `--limit=100` flag, but ensure you retrieve the `location`, `assetType`, and `name`.

*   **If `constraints/gcp.resourceLocations`:**
    *   *Command:* `gcloud asset search-all-resources --scope=[Scope] --format="table(location, assetType, name)" --limit=100`
    *   *Analysis:* Identify resources located outside the proposed allowed locations. You MUST extract 2-3 specific examples (Name and Asset Type) of these non-compliant resources to show the user.
*   **If `constraints/gcp.restrictServiceUsage`:**
    *   *Command:* `gcloud asset search-all-resources --scope=[Scope] --format="table(assetType, name)" --limit=50` (to sample existing resources) AND `gcloud services list --project=[Project_ID] --enabled` (if single project).
    *   *Analysis:* Extract examples of existing assets to show the user what *might* break if their underlying APIs are restricted. Emphasize that impact ultimately depends on runtime API calls.
*   **If restricting specific resource configurations:**
    *   *Command:* `gcloud asset search-all-resources --scope=[Scope] --asset-types="[Specific_Asset_Type]" --format="table(name, location)" --limit=50`
    *   *Analysis:* Extract 2-3 examples of the specific resources (e.g., SQL instances, VMs) that currently exist and will be flagged as non-compliant.

### 3. STRICT REQUIREMENT: Present Summary and Impact Analysis FIRST
You MUST output a detailed impact summary using the exact format below. Populate it using your actual findings from Step 2. Do not proceed to any execution tools until this summary is printed and approved.

"Here's a summary of the impact of applying the Organization Policy update for **[Constraint Name]**:

To address the Organization Policy violation, we will be updating the [Constraint Name] policy to explicitly [explain the change].

**Key Impacts:**
* **[Location/Service/Configuration] Restrictions:** [Explain the core restriction.]
* **Immediate Effect:** The policy change will take effect almost immediately after application (typically within minutes).
* **Future Operations & Resource Creation:**[Explain what will be blocked.]
* **Potential for Service Disruption:** [Explain risks to automation/pipelines.]
* **Existing Resources:**[CRITICAL: Inject findings from Step 2b here. State the locations/configurations currently in use. **Crucially, provide 2-3 concrete examples of affected resources (e.g., "Compute Instance: 'my-instance-1' in asia-east1")** so the user understands the real-world impact. If the CAIS command hit the 100 limit, mention that there are additional resources not listed.]

**Compliant Values to be Allowed:**
* [Value 1]
* [Value 2]

It is crucial to review the applications and workloads running in the affected scope to ensure they do not depend on any configurations absent from this list before applying this policy."

## 4. Show Remediation Steps & Commands
Clearly list the exact steps you will take if the user approves. Show the specific `gcloud` commands and the contents of any configuration files (e.g., YAML) you plan to create to fix the violation. Do NOT create the files yet.

## 5. Ask for Confirmation AND STOP
Ask the user for explicit permission to proceed with the execution. 

**CRITICAL INSTRUCTION: You MUST STOP HERE and wait for the user's reply. Do NOT use any file writing tools (like WriteFile) and do NOT execute any shell commands to apply the policy. You must WAIT for the user to explicitly confirm (e.g., "yes" or "proceed").**

## 6. Execute Remediation (ONLY AFTER CONFIRMATION)
If, and ONLY if, the user explicitly confirms they want to proceed, you may then invoke the necessary tools to write the configuration files and execute the `gcloud` commands to apply the policy.
---