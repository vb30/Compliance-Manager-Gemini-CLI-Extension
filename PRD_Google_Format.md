# Google Cloud Mini-PRD: Compliance Manager Gemini CLI Extension

---

## Table of Contents
1. [1-Pager Justification](#1-pager-justification)
2. [P0: Context, Executive Summary, & Vision](#p0-context-executive-summary--vision)
3. [P0: Critical User Journeys (CUJs)](#p0-critical-user-journeys-cujs)

---

## Useful Information

**Status:** Draft  
**Last Updated:** 2025-01-27  
**Authors:** Varun Bhardwaj  
**Collaborators:** TBD  

### Links to Other Materials
- **GitHub Repository:** https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension
- **MCP Server Repository:** https://github.com/vb30/Compliance-Manager-MCP-Server
- **User Guide:** [README.md](./README.md)
- **Technical Documentation:** [GEMINI.md](./GEMINI.md)
- **Installation Guide:** [install.sh](./install.sh)

### Approval Log
| Role | Username | Date |
|------|----------|------|
| Product Lead | TBD | yyyy-mm-dd |
| Eng Lead | TBD | yyyy-mm-dd |

---

## 1-Pager Justification

This PRD is required to enter the **Concept phase** of the Product Lifecycle (PLC). The goal is to provide explanation of the overall goals, value proposition, and user journeys that the Compliance Manager Gemini CLI Extension will cover.

The extension enables developers, security engineers, and compliance officers to manage Google Cloud compliance frameworks and controls through natural language conversations with Gemini CLI, eliminating the complexity of console navigation and manual API interactions.

---

## P0: Context, Executive Summary, & Vision

### What are we building?

A **Gemini CLI extension** that provides a Model Context Protocol (MCP) server for **Google Cloud Compliance Manager** (part of Security Command Center Enterprise). This extension enables users to manage compliance frameworks, cloud controls, and deployments through natural language conversations directly from the command line.

### Who are we building it for?

**Primary Users:**
- **Security Engineers** - Need to deploy and manage compliance frameworks across GCP organizations
- **DevOps/Platform Engineers** - Want to integrate compliance into infrastructure-as-code workflows
- **Compliance Officers** - Monitor compliance posture and create custom frameworks for regulatory requirements

**User Profiles:**
- Technical users comfortable with CLI tools
- GCP users with Security Command Center Enterprise tier
- Organizations requiring compliance management at scale
- Teams seeking to automate compliance workflows

### Why are we building it?

**Current Pain Points:**
1. **Complexity Barrier** - Managing compliance frameworks requires deep knowledge of Security Command Center console navigation and complex API interactions
2. **Context Switching** - Security teams must switch between CLI development workflows and web console for compliance tasks
3. **Custom Control Creation** - Building custom compliance controls requires understanding CEL (Common Expression Language) syntax and Cloud Asset Inventory schemas
4. **Deployment Friction** - Deploying frameworks involves multiple console clicks, form submissions, and manual tracking

**Value Proposition:**
- **Natural Language Interface** - Manage compliance through conversational AI instead of complex console navigation
- **Developer-First** - Integrate compliance into existing CLI workflows without context switching
- **AI-Assisted Control Creation** - Generate CEL expressions with AI guidance, no CEL expertise required
- **Comprehensive Coverage** - Full lifecycle management of frameworks, controls, and deployments
- **Enterprise-Ready** - Built on Google Cloud Compliance Manager with enterprise-grade security

### Goals & Results

**Goals:**
1. Reduce time to deploy compliance frameworks by 70% compared to console-based workflows
2. Enable non-CEL experts to create custom cloud controls with >95% success rate
3. Increase compliance framework adoption by 50% within 6 months
4. Achieve 4.5/5 user satisfaction rating

**Results:**
- Users can discover, create, and deploy compliance frameworks in <10 minutes
- Custom cloud controls can be created through natural language without CEL knowledge
- Framework deployments are trackable and monitorable from the CLI
- Compliance management is integrated into developer workflows

**Timeline:**
- **Phase 1 (Current):** Core functionality - framework and control management, deployments
- **Phase 2 (3-6 months):** Compliance reporting, framework templates, bulk operations
- **Phase 3 (6-12 months):** IaC integration, CI/CD integration, collaboration features

**Cost:**
- Development: Open source, community-driven
- Infrastructure: Leverages existing GCP Compliance Manager (requires SCC Enterprise tier)
- Maintenance: Minimal - uses stable GCP APIs and MCP protocol

**Critical Assumptions:**
1. Users have Security Command Center Enterprise tier enabled
2. Users are comfortable with CLI-based workflows
3. Gemini CLI adoption continues to grow
4. Compliance Manager API remains stable
5. MCP protocol remains backward compatible

---

## P0: Critical User Journeys (CUJs)

### CUJ 1: Discover and Explore Compliance Frameworks

**User Goal:** Understand what compliance frameworks are available and which one to use for my organization

**User Role:** Security Engineer (new to Compliance Manager)

**Prerequisites:**
- Gemini CLI installed and authenticated
- Compliance Manager enabled in GCP organization
- User has IAM role<> or higher
- Organization ID known

**Journey Steps:**

| Step | User Story | Features Enabling This Step | API/CLI/GUI |
|------|------------|------------------------------|-------------|
| 1 | As a security engineer, I want to see all available compliance frameworks | `list_frameworks` tool, natural language query processing | CLI (Gemini) |
| 2 | As a security engineer, I want to understand what each framework covers | `get_framework` tool, framework detail display | CLI (Gemini) |
| 3 | As a security engineer, I want to see which controls are in a framework | Framework control mapping display, control details | CLI (Gemini) |
| 4 | As a security engineer, I want to filter frameworks by type (built-in vs custom) | Framework filtering, categorization | CLI (Gemini) |
| 5 | As a security engineer, I want to understand regulatory mappings | Regulatory control mapping display | CLI (Gemini) |

**Example Conversation Flow:**
```
User: "What compliance frameworks are available in my organization 123456789012?"

Gemini: [Calls list_frameworks tool]
"I found 15 compliance frameworks in your organization:

Built-in Frameworks:
- CIS Google Cloud Platform Foundation Benchmark v1.3.0
- NIST Cybersecurity Framework (CSF)
- FedRAMP Moderate Baseline
- PCI-DSS v3.2.1
- ISO 27001:2013
...

Custom Frameworks:
- company-security-baseline
- eu-data-residency-v1

Would you like details on any specific framework?"

User: "Tell me about the CIS framework"

Gemini: [Calls get_framework tool]
"The CIS Google Cloud Platform Foundation Benchmark v1.3.0 includes:
- 67 cloud controls covering identity, networking, logging, and storage
- Mapped to CIS regulatory controls
- Focuses on security best practices for GCP

Key control areas:
- Identity and Access Management (14 controls)
- Logging and Monitoring (12 controls)
- Networking (18 controls)
- VM Security (10 controls)
- Storage Security (13 controls)

Would you like to deploy this framework or see specific controls?"
```

**Success Criteria:**
- User can list all frameworks in < 5 seconds
- User understands framework purpose and coverage
- User can identify appropriate framework for their needs
- Framework details are comprehensive and readable

**Metrics:**
- Time to first framework list: < 5 seconds
- Framework detail retrieval: < 3 seconds
- User comprehension rate: > 90%
- Task completion rate: > 95%

**Integration Points:**
- **GCP Products:** Security Command Center, Compliance Manager API
- **Dependencies:** Gemini CLI, MCP protocol, google-cloud-cloudsecuritycompliance library
---

### CUJ 2: Create a Custom Cloud Control with AI Assistance

**User Goal:** Create a custom compliance control to check for specific security requirements without knowing CEL syntax

**User Role:** Security Engineer (experienced with GCP, new to CEL)

**Prerequisites:**
- User has <> role
- Understanding of the security requirement to enforce
- Knowledge of target resource type (e.g., Compute Engine, Cloud Storage)

**Journey Steps:**

| Step | User Story | Features Enabling This Step | API/CLI/GUI |
|------|------------|------------------------------|-------------|
| 1 | As a security engineer, I want to describe my security requirement in natural language | Natural language processing, requirement understanding | CLI (Gemini) |
| 2 | As a security engineer, I want AI to suggest the appropriate CEL expression | CEL expression generation, resource type detection | CLI (Gemini) |
| 3 | As a security engineer, I want to review and confirm the control configuration | Control preview, configuration display | CLI (Gemini) |
| 4 | As a security engineer, I want to create the control with appropriate severity | `create_cloud_control` tool, severity selection | CLI (Gemini) |
| 5 | As a security engineer, I want confirmation that the control was created successfully | Control creation confirmation, validation | CLI (Gemini) |

**Example Conversation Flow:**
```
User: "I need to create a control that checks if all Compute Engine VMs have Secure Boot enabled"

Gemini: "I'll help you create a custom cloud control for VM Secure Boot.

For this control, I'll use:
- Resource type: compute.googleapis.com/Instance
- CEL expression: has(resource.data.shieldedInstanceConfig) && 
                  resource.data.shieldedInstanceConfig.enableSecureBoot
- This checks if VMs have Secure Boot enabled in their shielded instance config

What severity should this be?
- CRITICAL: For critical security requirements
- HIGH: For important security controls
- MEDIUM: For recommended practices
- LOW: For informational checks"

User: "Make it HIGH severity"

Gemini: [Calls create_cloud_control tool]
"✓ Created custom cloud control 'require-secure-boot'

Details:
- Display Name: Require Secure Boot on VMs
- Resource Type: compute.googleapis.com/Instance
- Severity: HIGH
- CEL Expression: has(resource.data.shieldedInstanceConfig) && 
                  resource.data.shieldedInstanceConfig.enableSecureBoot

This control will check all Compute Engine instances and create HIGH severity 
findings for VMs without Secure Boot enabled.

Next steps:
- Add this to a custom framework, or
- Deploy it directly to your resources

What would you like to do?"
```

**Success Criteria:**
- User can create control without knowing CEL syntax
- AI suggests accurate CEL expressions (>90% accuracy)
- Control is created successfully on first attempt (>95% success rate)
- User understands what the control does and how it works

**Metrics:**
- Control creation success rate: > 95%
- Time to create control: < 2 minutes
- CEL expression accuracy: > 90%
- User satisfaction with AI assistance: 4.5/5

**Integration Points:**
- **GCP Products:** Cloud Asset Inventory (for resource schemas), Compliance Manager API
- **Dependencies:** Gemini LLM (for CEL generation), MCP protocol

---

### CUJ 3: Deploy a Compliance Framework to Production

**User Goal:** Apply a compliance framework to a production project to enable continuous monitoring

**User Role:** DevOps Engineer (deploying infrastructure with compliance requirements)

**Prerequisites:**
- User has <> role
- Target project exists and is accessible
- Framework to deploy is identified (e.g., NIST, CIS, custom framework)
- User understands deployment implications

**Journey Steps:**

| Step | User Story | Features Enabling This Step | API/CLI/GUI |
|------|------------|------------------------------|-------------|
| 1 | As a DevOps engineer, I want to specify which framework to deploy | Framework selection, natural language parsing | CLI (Gemini) |
| 2 | As a DevOps engineer, I want to specify the target resource (project/folder/org) | Resource specification, validation | CLI (Gemini) |
| 3 | As a DevOps engineer, I want to review deployment details before proceeding | Deployment preview, confirmation prompt | CLI (Gemini) |
| 4 | As a DevOps engineer, I want to initiate the deployment | `create_framework_deployment` tool | CLI (Gemini) |
| 5 | As a DevOps engineer, I want to monitor deployment progress | Operation tracking, status updates | CLI (Gemini) |
| 6 | As a DevOps engineer, I want confirmation when deployment is complete | Deployment completion notification, details | CLI (Gemini) |

**Example Conversation Flow:**
```
User: "Deploy the NIST framework to project my-prod-project"

Gemini: "I'll deploy the NIST Cybersecurity Framework to project 'my-prod-project'.

Deployment Details:
- Framework: NIST Cybersecurity Framework (CSF)
- Target: projects/my-prod-project
- Controls: 98 cloud controls will be activated
- Impact: Continuous monitoring will begin, findings will be generated

This will:
✓ Enable continuous monitoring of NIST controls
✓ Generate findings for non-compliant resources
✓ Create a framework deployment that can be tracked in SCC

Proceed with deployment? (yes/no)"

User: "yes"

Gemini: [Calls create_framework_deployment tool]
"✓ Framework deployment initiated

Operation ID: operations/abc123def456...
Status: IN_PROGRESS
Target: projects/my-prod-project
Framework: NIST CSF

This may take a few minutes. I'll check the status for you...

[After polling]

✓ Deployment complete!

The NIST Cybersecurity Framework is now active on project 'my-prod-project'.

Summary:
- 98 cloud controls activated
- Monitoring started at: 2025-01-27 10:30:00 UTC
- View findings in Security Command Center: 
  https://console.cloud.google.com/security/command-center

Would you like to:
- View deployment details
- List active controls
- Check for existing findings"
```

**Success Criteria:**
- Deployment completes successfully (>98% success rate)
- User receives clear status updates during deployment
- User understands what was deployed and where
- Deployment is trackable and verifiable in SCC
- User knows how to access findings

**Metrics:**
- Deployment success rate: > 98%
- Time to deployment completion: < 5 minutes
- User clarity on deployment status: 4.5/5
- Time savings vs console: > 70%

**Integration Points:**
- **GCP Products:** Security Command Center (for findings), Compliance Manager API, Cloud Resource Manager (for resource validation)
- **Dependencies:** Long-running operation handling, MCP protocol

---

### CUJ 4: Create and Deploy a Custom Compliance Framework

**User Goal:** Build a custom compliance framework combining multiple controls for company-specific regulatory requirements

**User Role:** Compliance Officer (defining organizational security policies)

**Prerequisites:**
- User has <> role
- Understanding of required compliance controls
- Target resources for deployment identified
- Knowledge of regulatory requirements to meet

**Journey Steps:**

| Step | User Story | Features Enabling This Step | API/CLI/GUI |
|------|------------|------------------------------|-------------|
| 1 | As a compliance officer, I want to describe my compliance requirements | Natural language requirement processing | CLI (Gemini) |
| 2 | As a compliance officer, I want to discover relevant existing controls | `list_cloud_controls` tool, filtering, search | CLI (Gemini) |
| 3 | As a compliance officer, I want to create custom controls for gaps | `create_cloud_control` tool, CEL assistance | CLI (Gemini) |
| 4 | As a compliance officer, I want to combine controls into a framework | `create_framework` tool, control selection | CLI (Gemini) |
| 5 | As a compliance officer, I want to deploy the framework to my organization | `create_framework_deployment` tool | CLI (Gemini) |
| 6 | As a compliance officer, I want to verify the framework is active | `get_framework_deployment` tool, status checking | CLI (Gemini) |

**Example Conversation Flow:**
```
User: "I need to create a custom framework for our company's data residency requirements in the EU"

Gemini: "I'll help you create a custom framework for EU data residency compliance.

Let me first show you available controls related to data location and residency.
What's your organization ID?"

User: "123456789012"

Gemini: [Calls list_cloud_controls with filtering]
"I found 8 built-in controls related to data location and residency:

1. gcp-location-restriction - Ensures resources are in allowed regions
2. storage-bucket-location - Checks Cloud Storage bucket locations
3. compute-zone-restriction - Validates Compute Engine zones
4. bigquery-dataset-location - Checks BigQuery dataset locations
...

Would you like to:
- Use these built-in controls, or
- Create additional custom controls for specific EU requirements?"

User: "Use the built-in controls, and also create a custom control to ensure Cloud Storage
buckets are only in EU regions"

Gemini: "I'll create a custom control for EU-only Cloud Storage buckets.

[Calls create_cloud_control]
✓ Created custom control 'eu-storage-bucket-location'

Details:
- Resource Type: storage.googleapis.com/Bucket
- CEL Expression: resource.data.location.matches('^(europe-|eu-)')
- Severity: HIGH
- Description: Ensures Cloud Storage buckets are located in EU regions only

Now let's create your custom framework. What should we name it?"

User: "eu-data-residency-v1"

Gemini: "I'll create the 'eu-data-residency-v1' framework with:
- 8 built-in location controls
- 1 custom EU storage control

[Calls create_framework]
✓ Created custom framework 'eu-data-residency-v1'

Framework Details:
- Display Name: EU Data Residency Framework v1
- Total Controls: 9
- Coverage: Compute, Storage, BigQuery, and general location restrictions

Would you like to deploy this framework now? If so, to which resource?
(organization/folder/project)"

User: "Deploy to organization 123456789012"

Gemini: [Calls create_framework_deployment]
"✓ Deploying framework to organization 123456789012...

Operation ID: operations/xyz789...
Status: IN_PROGRESS

[After completion]

✓ Deployment complete!

Your 'eu-data-residency-v1' framework is now active across your entire organization.

Summary:
- Framework: eu-data-residency-v1
- Scope: organizations/123456789012
- Active Controls: 9
- Monitoring: All resources in the organization

All resources will now be continuously monitored for EU data residency compliance.
Findings will appear in Security Command Center for any violations.

Next steps:
- Review findings in SCC
- Set up alerting for critical findings
- Document framework for audit purposes"
```

**Success Criteria:**
- User can create complex framework without API knowledge
- Custom controls are created correctly with AI assistance
- Framework is deployed successfully to intended scope
- User understands framework composition and coverage
- Framework is immediately active and monitoring

**Metrics:**
- Framework creation success rate: > 95%
- Time to create and deploy: < 10 minutes
- User satisfaction with guidance: 4.5/5
- Control accuracy: > 90%

**Integration Points:**
- **GCP Products:** Compliance Manager API, Cloud Asset Inventory, Security Command Center
- **Dependencies:** Multi-step workflow orchestration, MCP protocol, Gemini LLM

---

### CUJ 5: Monitor and Audit Compliance Deployments

**User Goal:** Check the status of compliance framework deployments across my organization and identify coverage gaps

**User Role:** Security Engineer (monitoring compliance posture)

**Prerequisites:**
- User has <> or higher
- Frameworks are deployed to various resources
- User wants to audit compliance coverage
- Organization ID known

**Journey Steps:**

| Step | User Story | Features Enabling This Step | API/CLI/GUI |
|------|------------|------------------------------|-------------|
| 1 | As a security engineer, I want to see all framework deployments | `list_framework_deployments` tool | CLI (Gemini) |
| 2 | As a security engineer, I want to drill into specific deployment details | `get_framework_deployment` tool | CLI (Gemini) |
| 3 | As a security engineer, I want to see which controls are actively monitoring | `list_cloud_control_deployments` tool | CLI (Gemini) |
| 4 | As a security engineer, I want to identify resources without coverage | Deployment analysis, gap identification | CLI (Gemini) |
| 5 | As a security engineer, I want to understand compliance status | Deployment status aggregation, reporting | CLI (Gemini) |

**Example Conversation Flow:**
```
User: "Show me all framework deployments in organization 123456789012"

Gemini: [Calls list_framework_deployments]
"I found 12 framework deployments in your organization:

Organization-level (1):
✓ eu-data-residency-v1 → organizations/123456789012
  Status: ACTIVE | Controls: 9 | Created: 2025-01-15

Folder-level (3):
✓ NIST CSF → folders/production-folder
  Status: ACTIVE | Controls: 98 | Created: 2025-01-10
✓ CIS Benchmark → folders/staging-folder
  Status: ACTIVE | Controls: 67 | Created: 2025-01-12
✓ PCI-DSS → folders/payment-systems
  Status: ACTIVE | Controls: 45 | Created: 2025-01-08

Project-level (8):
✓ NIST CSF → projects/my-prod-project
  Status: ACTIVE | Controls: 98 | Created: 2025-01-20
✓ FedRAMP Moderate → projects/gov-project
  Status: ACTIVE | Controls: 112 | Created: 2025-01-18
...

Would you like details on any specific deployment?"

User: "Tell me more about the NIST deployment on project my-prod-project"

Gemini: [Calls get_framework_deployment]
"NIST Cybersecurity Framework Deployment Details:

Deployment Information:
- Framework: NIST CSF
- Target: projects/my-prod-project
- Status: ACTIVE
- Created: 2025-01-20 10:30:00 UTC
- Last Updated: 2025-01-27 08:15:00 UTC

Active Controls: 98
- Identity & Access: 22 controls
- Logging & Monitoring: 18 controls
- Network Security: 25 controls
- Data Protection: 15 controls
- Incident Response: 18 controls

Compliance Status:
- Total Resources Monitored: 1,247
- Compliant Resources: 1,089 (87%)
- Non-Compliant Resources: 158 (13%)
- Active Findings: 158 (45 HIGH, 89 MEDIUM, 24 LOW)

Recent Activity:
- New findings in last 24h: 12
- Resolved findings in last 24h: 8

View findings in SCC:
https://console.cloud.google.com/security/command-center/findings?project=my-prod-project

Would you like to:
- See specific findings
- List active controls
- Check other deployments"

User: "What cloud controls are actively monitoring my production project?"

Gemini: [Calls list_cloud_control_deployments]
"Active Cloud Controls in projects/my-prod-project:

From NIST CSF Framework (98 controls):

High Priority Controls:
✓ require-mfa-for-privileged-users (CRITICAL)
  Findings: 3 | Resource Type: iam.googleapis.com/ServiceAccount
✓ encryption-at-rest-enabled (HIGH)
  Findings: 12 | Resource Type: compute.googleapis.com/Disk
✓ no-public-ip-addresses (HIGH)
  Findings: 8 | Resource Type: compute.googleapis.com/Instance
...

Medium Priority Controls:
✓ log-retention-90-days (MEDIUM)
  Findings: 15 | Resource Type: logging.googleapis.com/LogSink
...

All controls are actively monitoring. You have 158 total findings to address.

Would you like to:
- See findings by severity
- Get remediation guidance
- Export findings report"
```

**Success Criteria:**
- User can see all deployments in one comprehensive view
- Deployment details are accurate and current
- User can track compliance coverage across resources
- User can identify gaps in compliance coverage
- Status information is real-time and actionable

**Metrics:**
- Deployment list retrieval: < 5 seconds
- Deployment detail accuracy: 100%
- User ability to identify gaps: > 90%
- Time to audit completion: < 10 minutes

**Integration Points:**
- **GCP Products:** Security Command Center (for findings), Compliance Manager API, Cloud Resource Manager
- **Dependencies:** MCP protocol, data aggregation and analysis

---

## Summary of CUJ Coverage

### API/CLI/GUI Usage
All CUJs use **CLI (Gemini)** as the primary interface, leveraging:
- Natural language processing for user intent understanding
- MCP protocol for tool invocation
- Google Cloud APIs for backend operations
- Security Command Center GUI for findings visualization (view-only)

### GCP Product Integrations
- **Security Command Center Enterprise** - Core platform for compliance management
- **Compliance Manager API** - All framework, control, and deployment operations
- **Cloud Asset Inventory** - Resource data for control evaluation
- **Cloud Resource Manager** - Resource validation and hierarchy
- **Cloud Logging** - Audit logging for operations

### Product Dependencies
**This product depends on:**
- Gemini CLI (>= 0.6.0)
- Security Command Center Enterprise tier
- Compliance Manager API
- Google Cloud authentication (ADC)
- MCP protocol (>= 1.4.1)

**Products that depend on this product:**
- None currently (standalone extension)
- Future: Potential integration with IaC tools, CI/CD pipelines
---

## Additional Considerations

### Questions Addressed

**Does your feature need API/CLI/GUI?**
- **Primary:** CLI via Gemini (natural language interface)
- **Secondary:** API (underlying Compliance Manager API)
- **Tertiary:** GUI (Security Command Center for viewing findings only)

**Are there any other GCP products you want to integrate with?**
- **Current:** Security Command Center, Cloud Asset Inventory, Cloud Resource Manager
- **Future:** Cloud Logging (for audit trails), Cloud Monitoring (for alerting), BigQuery (for analytics)

**What product(s) depend on your product?**
- Currently none (standalone extension)
- Future potential: Terraform providers, CI/CD tools, compliance automation platforms

**What product(s) does your product depend on?**
- Security Command Center Enterprise (required)
- Compliance Manager API (required)
- Gemini CLI (required)
- Cloud Asset Inventory (for resource data)
- Cloud Resource Manager (for resource validation)


### User Profiles Targeted
Based on Cloud user personas:
- **Cloud Security Architect** - Designing compliance frameworks
- **DevOps Engineer** - Integrating compliance into workflows
- **Compliance Manager** - Monitoring and reporting on compliance
- **Platform Engineer** - Managing infrastructure compliance

---

**End of Mini-PRD**


