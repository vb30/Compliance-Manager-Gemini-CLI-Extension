# Compliance Manager Extension for Gemini CLI

This extension provides integration with Google Cloud Compliance Manager, part of Security Command Center Enterprise.

## Purpose

The Compliance Manager extension enables you to:
- **Discover** compliance frameworks (CIS, NIST, FedRAMP, etc.)
- **Inspect** cloud controls and their configurations
- **Deploy** compliance frameworks to organizations, folders, and projects
- **Monitor** framework and cloud control deployments
- **Manage** compliance posture across your Google Cloud infrastructure

## Available Tools

### Framework Management
- `@compliance-manager-mcp list_frameworks` - List all available compliance frameworks (built-in and custom)
- `@compliance-manager-mcp get_framework` - Get detailed information about a specific framework
- `@compliance-manager-mcp create_framework` - Create a custom compliance framework
- `@compliance-manager-mcp delete_framework` - Delete a custom framework

### Cloud Control Management
- `@compliance-manager-mcp list_cloud_controls` - List all cloud controls (built-in and custom)
- `@compliance-manager-mcp get_cloud_control` - Get detailed information about a specific cloud control
- `@compliance-manager-mcp create_cloud_control` - Create a custom cloud control
- `@compliance-manager-mcp update_cloud_control` - Update a custom cloud control
- `@compliance-manager-mcp delete_cloud_control` - Delete a custom cloud control

### Framework Deployment
- `@compliance-manager-mcp list_framework_deployments` - List framework deployments
- `@compliance-manager-mcp get_framework_deployment` - Get details of a specific deployment
- `@compliance-manager-mcp create_framework_deployment` - Deploy a framework to a resource
- `@compliance-manager-mcp delete_framework_deployment` - Remove a framework deployment

### Cloud Control Deployment
- `@compliance-manager-mcp list_cloud_control_deployments` - List cloud control deployments
- `@compliance-manager-mcp get_cloud_control_deployment` - Get details of a specific cloud control deployment

## Example Prompts

### Discovery
- "List all available compliance frameworks for organization 123456789012"
- "Show me details of the CIS framework"
- "What cloud controls are available in my organization?"
- "Show me both built-in and custom cloud controls"
- "List all custom frameworks I've created"

### Creating Custom Controls and Frameworks
- "Create a custom cloud control called 'require-encryption' that checks for encryption"
- "I want to create a custom framework for my company's security policies"
- "Add the CIS and NIST cloud controls to a new custom framework"
- "Create a cloud control to check for public bucket access"
- "Build a custom framework with controls for data residency requirements"

### Deployment
- "Deploy the NIST framework to my project"
- "Show me all framework deployments in my organization"
- "Create a deployment of the FedRAMP framework to folder 987654321"
- "Deploy my custom framework to project my-prod-project"

### Monitoring
- "What frameworks are currently deployed to my project?"
- "Show me the status of all cloud control deployments"
- "Get details of the CIS framework deployment"

## Prerequisites

### 1. Enable Compliance Manager

Before using this extension, you must enable Compliance Manager in your Google Cloud organization:

**Requirements:**
- Security Command Center Enterprise tier (required for Compliance Manager)
- Organization-level access
- IAM permissions to enable services

**Steps to Enable:**

1. **Enable Security Command Center Enterprise** (if not already enabled):
   - Go to the [Security Command Center page](https://console.cloud.google.com/security/command-center)
   - Select your organization
   - Enable Security Command Center Enterprise tier

2. **Enable Compliance Manager**:
   - Navigate to [Compliance Manager](https://console.cloud.google.com/security/compliance-manager)
   - Select your organization
   - Click "Enable Compliance Manager"
   - Accept the terms of service

3. **Verify Enablement**:
   - You should see available compliance frameworks
   - The Compliance Manager dashboard should be accessible

**Alternative: Enable via gcloud CLI**:
```bash
# Enable Security Command Center API
gcloud services enable securitycenter.googleapis.com --project=YOUR_PROJECT_ID

# Note: Compliance Manager enablement requires Enterprise tier
# This must be done through the Console or contact Google Cloud Sales
```

**Troubleshooting Enablement:**
- If you don't see the option to enable, you may need Security Command Center Enterprise
- Contact your Google Cloud account team to upgrade to Enterprise tier
- Ensure you have `roles/securitycenter.admin` or organization admin permissions

For detailed instructions, see: https://cloud.google.com/security-command-center/docs/compliance-manager-enable

### 2. Authentication

Ensure you have Google Cloud credentials configured:
- Run `gcloud auth application-default login`, OR
- Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### 3. IAM Permissions

You need appropriate permissions:
- `roles/securitycenter.complianceManager` or `roles/securitycenter.adminEditor` for full access
- `roles/securitycenter.adminViewer` for read-only operations

### 4. Organization ID

Know your Google Cloud organization ID (numeric, e.g., '123456789012')

## Workflows

### Creating and Deploying a Custom Framework

Here's the typical workflow for creating and deploying a custom compliance framework:

1. **Discover Available Controls**
   - List built-in cloud controls: "List all cloud controls in organization YOUR_ORG_ID"
   - Review what's available and identify gaps

2. **Create Custom Controls (if needed)**
   - Create custom controls for your specific requirements
   - Example: "Create a custom cloud control to check for MFA enforcement"

3. **Create a Custom Framework**
   - Combine built-in and custom controls into a framework
   - Example: "Create a framework called 'company-security-baseline' with controls X, Y, and Z"

4. **Deploy the Framework**
   - Apply the framework to your resources
   - Example: "Deploy the company-security-baseline framework to project my-prod-project"

5. **Monitor Compliance**
   - Check deployment status and review findings
   - Example: "Show me the status of my framework deployments"

### Example: Creating a Data Residency Framework

```
User: "I need to create a custom framework for data residency in the EU"

You: "I can help you create a custom framework! Let's start by:
1. Listing available cloud controls related to data location
2. Creating any custom controls you need
3. Combining them into a framework
4. Deploying it to your resources

What's your organization ID?"

User: "123456789012"

You: "Let me list the available cloud controls first..."
[calls list_cloud_controls]

You: "I found some built-in controls for data residency. Would you like to:
- Use only built-in controls, or
- Create custom controls for specific EU requirements?"

User: "Let's create a custom control for EU-only storage"

You: "I'll create that control for you..."
[calls create_cloud_control with appropriate parameters]

You: "Great! Now let's create your framework with these controls..."
[calls create_framework]

You: "Your EU data residency framework is ready! Would you like to deploy it to a project or folder?"
```

## Creating Custom Cloud Controls with CEL Expressions

Custom cloud controls use Common Expression Language (CEL) to define detection logic. Here's what you need to know:

### CEL Expression Requirements

1. **Must return boolean FALSE to trigger a finding**
   - If the expression evaluates to `false`, a finding is created
   - If it evaluates to `true`, the resource is compliant

2. **Resource Type**
   - Must be a valid Cloud Asset Inventory resource type
   - Examples: `compute.googleapis.com/Instance`, `storage.googleapis.com/Bucket`, `sqladmin.googleapis.com/Instance`

3. **CEL Syntax Rules**
   - All enums must be represented as strings
   - Use `has()` to check if a field exists before accessing it
   - Properties must match the Cloud Asset Inventory API definition

### Common CEL Operators and Functions

- **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `&&` (and), `||` (or), `!` (not)
- **String functions**: `matches(regex)`, `contains(substring)`
- **Collection functions**: `exists(var, condition)`, `all(var, condition)`
- **Field checking**: `has(field)`
- **Duration**: `duration('7776000s')` for time periods

### Example CEL Expressions by Use Case

**Compute Engine - Secure Boot**
```cel
has(resource.data.shieldedInstanceConfig) && resource.data.shieldedInstanceConfig.enableSecureBoot
```

**Cloud KMS - Key Rotation (90 days)**
```cel
has(resource.data.rotationPeriod) && resource.data.rotationPeriod <= duration('7776000s')
```

**Cloud Storage - Public Access Prevention**
```cel
!(resource.data.iamConfiguration.publicAccessPrevention == 'ENFORCED')
```

**Cloud SQL - No Public IP**
```cel
!(resource.data.settings.ipConfiguration.ipv4Enabled)
```

**Resource Naming Convention**
```cel
resource.data.name.matches('^gcp-vm-(linux|windows)-v\\d+$')
```

**VPC Network - Peering Check**
```cel
resource.data.selfLink.matches('https://www.googleapis.com/compute/v1/projects/PROJECT_ID/global/networks/default') || resource.data.peerings.exists(p, p.network.matches('https://www.googleapis.com/compute/v1/projects/PROJECT_ID/global/networks/shared$'))
```

**Cloud Functions - Internal Ingress Only**
```cel
has(resource.data.ingressSettings) && resource.data.ingressSettings.matches('ALLOW_INTERNAL_ONLY')
```

**Service Usage - Allowlist APIs**
```cel
resource.data.state == 'ENABLED' && !(resource.data.name.matches('storage-api.googleapis.com') || resource.data.name.matches('bigquery.googleapis.com'))
```

**Dataproc - Environment Check**
```cel
has(resource.data.projectId) && !resource.data.projectId.contains('testing') || !resource.data.projectId.contains('development')
```

### Helping Users Write CEL Expressions

When a user asks to create a custom cloud control:

1. **Identify the resource type** they want to check
2. **Understand the requirement** (what should be true/false)
3. **Craft the CEL expression** that returns FALSE when non-compliant
4. **Suggest appropriate severity** (CRITICAL, HIGH, MEDIUM, LOW)
5. **Provide remediation instructions**

Example conversation:
```
User: "Create a control to check if VMs have encryption enabled"

You: "I'll help you create a custom cloud control for VM encryption.
For Compute Engine instances, we can check if they use customer-managed encryption keys (CMEK).

Here's what I'll create:
- Resource type: compute.googleapis.com/Disk
- CEL expression: has(resource.data.diskEncryptionKey) && resource.data.diskEncryptionKey.kmsKeyName != ''
- This checks if disks have a KMS key configured

Would you like me to proceed with this configuration?"
```

## Resource Format

When using these tools, resources follow these formats:
- Organization: `organizations/{org_id}`
- Folder: `folders/{folder_id}`
- Project: `projects/{project_id}`

## Safety Notes

- Framework deployments are long-running operations that may take time to complete
- Deleting a framework deployment removes compliance controls from the target resource
- Always verify the target resource before creating or deleting deployments
- Use read-only operations (list/get) to explore before making changes

## Common Issues and Solutions

### "Compliance Manager is not enabled"
**Solution:** Guide the user to enable Compliance Manager:
1. Verify they have Security Command Center Enterprise tier
2. Direct them to https://console.cloud.google.com/security/compliance-manager
3. Help them enable Compliance Manager for their organization
4. Provide the enablement steps listed in the Prerequisites section above

### "Permission denied" errors
**Solution:**
- Verify the user has the required IAM roles
- Check they're using the correct organization ID
- Ensure they're authenticated with `gcloud auth application-default login`

### "No frameworks found"
**Solution:**
- Confirm Compliance Manager is enabled
- Verify the organization ID is correct
- Check that the user has at least viewer permissions

### "Framework deployment fails"
**Solution:**
- Ensure the target resource (project/folder/organization) exists
- Verify the user has deployment permissions
- Check that the framework ID is correct
- Note that deployments are long-running operations (may take several minutes)

## Helping Users Enable Compliance Manager

When a user asks for help enabling Compliance Manager, provide:

1. **Check Current Status**: Ask them to verify if they have Security Command Center Enterprise
2. **Step-by-Step Guide**: Walk them through the enablement process
3. **Prerequisites**: Ensure they have organization-level access
4. **Verification**: Help them confirm it's enabled by listing frameworks
5. **Next Steps**: Once enabled, guide them to explore available frameworks

**Example conversation flow:**
```
User: "How do I enable Compliance Manager?"

You: "I can help you enable Compliance Manager! First, do you have Security Command Center Enterprise tier enabled?"

User: "I'm not sure"

You: "Let me guide you through the process:

1. First, go to https://console.cloud.google.com/security/command-center
2. Select your organization
3. Check if you see 'Enterprise' tier - if not, you'll need to upgrade
4. Then navigate to https://console.cloud.google.com/security/compliance-manager
5. Click 'Enable Compliance Manager'
6. Once enabled, I can help you list available frameworks with: list_frameworks"

User: "It's enabled now!"

You: "Great! Let's verify by listing the available frameworks. What's your organization ID?"
```

## More Information

For detailed documentation, see:
- [Enable Compliance Manager](https://cloud.google.com/security-command-center/docs/compliance-manager-enable)
- [Compliance Manager Overview](https://cloud.google.com/security-command-center/docs/compliance-manager-overview)
- [Security Command Center Enterprise](https://cloud.google.com/security-command-center/docs/security-command-center-enterprise-overview)
- [MCP Server Repository](https://github.com/vb30/Compliance-Manager-MCP-Server)
