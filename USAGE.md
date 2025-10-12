# Usage Examples

## Basic Commands

### List Frameworks
```
List all compliance frameworks in organization 123456789012

Show me both built-in and custom frameworks
```

### Get Framework Details
```
Show me details of the CIS framework

Tell me about the NIST framework
```

### List Cloud Controls
```
What cloud controls are available in my organization?

Show me all cloud controls (built-in and custom)

List only custom cloud controls
```

### List Deployments
```
What frameworks are currently deployed?

Show me all framework deployments in organization 123456789012
```

## Creating Custom Cloud Controls

Custom cloud controls use CEL (Common Expression Language) expressions to evaluate resources. The expression must return **FALSE** to trigger a finding.

### Create Controls for Compute Engine

```
Create a cloud control to ensure all VMs have Secure Boot enabled

I need a control to check if Compute Engine instances use custom service accounts (not the default)

Create a control to verify all VM disks are encrypted with customer-managed keys

Make a control to check if VMs follow our naming convention: gcp-vm-prod-*
```

### Create Controls for Cloud Storage

```
Create a cloud control to check if Cloud Storage buckets have public access prevention enforced

I need a control to verify all buckets have versioning enabled

Create a control to ensure buckets are not publicly accessible

Make a control to check if buckets use customer-managed encryption keys
```

### Create Controls for Cloud SQL

```
Create a cloud control to ensure Cloud SQL instances don't have public IP addresses

I need a control to check if Cloud SQL instances have automated backups enabled

Create a control to verify SSL/TLS is required for Cloud SQL connections

Make a control to check if Cloud SQL instances are in high-availability configuration
```

### Create Controls for Cloud KMS

```
Create a cloud control to ensure KMS keys are rotated every 90 days or less

I need a control to check if KMS keys have destruction scheduled

Create a control to verify KMS keys are in specific regions only
```

### Create Controls for Networking

```
Create a cloud control to check if VPC networks have flow logs enabled

I need a control to verify firewall rules don't allow 0.0.0.0/0 ingress on sensitive ports

Create a control to ensure VPCs use private Google access

Make a control to check if load balancers use HTTPS only
```

### Create Controls for IAM and Security

```
Create a cloud control to check if service accounts have key rotation policies

I need a control to verify no service accounts have owner or editor roles

Create a control to ensure MFA is required for all users

Make a control to check if service accounts follow naming conventions
```

## Understanding CEL Expressions for Cloud Controls

When creating custom cloud controls, you'll use CEL (Common Expression Language) expressions. Here's what you need to know:

### Key Concepts

- **The expression must return FALSE to trigger a finding** (non-compliant resource)
- **Use `has()` to check if a field exists** before accessing it
- **All enums must be strings** (e.g., `"ENABLED"` not `ENABLED`)
- **Resource properties** come from Cloud Asset Inventory

### Example CEL Expressions

**Check if a field exists and has a specific value:**
```
has(resource.data.shieldedInstanceConfig) && resource.data.shieldedInstanceConfig.enableSecureBoot
```

**Check duration/time periods (90 days = 7776000 seconds):**
```
has(resource.data.rotationPeriod) && resource.data.rotationPeriod <= duration('7776000s')
```

**Check if a field does NOT have a value (negation):**
```
!(resource.data.settings.ipConfiguration.ipv4Enabled)
```

**Pattern matching with regex:**
```
resource.data.name.matches('^gcp-vm-(prod|staging)-v\\d+$')
```

**Check if string contains substring:**
```
resource.data.projectId.contains('production')
```

**Check collections with exists():**
```
resource.data.peerings.exists(p, p.network.matches('shared-vpc'))
```

**Combine multiple conditions:**
```
resource.data.state == 'ENABLED' && !(resource.data.name.matches('approved-api.googleapis.com'))
```

### Common Mistakes to Avoid

❌ **Don't forget `has()` checks:**
```
resource.data.encryptionKey.kmsKeyName != ''  // May fail if encryptionKey doesn't exist
```

✅ **Always check existence first:**
```
has(resource.data.encryptionKey) && resource.data.encryptionKey.kmsKeyName != ''
```

❌ **Don't use enum values without quotes:**
```
resource.data.state == ENABLED  // Wrong!
```

✅ **Use string values for enums:**
```
resource.data.state == 'ENABLED'  // Correct!
```

## Creating Custom Frameworks

### Create a Framework from Existing Controls
```
Create a custom framework called "company-baseline" using CIS and NIST controls

Build a framework with controls for PCI-DSS compliance

I want to create a framework combining built-in controls for data protection
```

### Create a Framework with Custom Controls
```
Create a framework called "eu-data-residency" with custom controls for EU compliance

Build a custom framework for financial services with specific controls

Create a framework that includes both built-in and my custom controls
```

## Deployment Commands

### Deploy a Framework
```
Deploy the NIST framework to project my-project-id

I want to deploy CIS to my production project
```

### Check Deployment Status
```
What's the status of my compliance deployments?

Show me deployment details for the CIS framework
```

### Delete a Deployment
```
Remove the NIST framework deployment from project my-project-id
```

## Natural Language Examples

The extension understands natural language. Here are some examples:

```
Help me understand what compliance frameworks are available

I need to ensure my project meets NIST compliance requirements

What's the difference between CIS and FedRAMP?

Show me the current compliance posture of my organization

How do I deploy compliance controls to a folder?

What frameworks are recommended for financial services?
```

## Getting Help from the Extension

The extension can help you with setup and troubleshooting:

```
How do I enable Compliance Manager?

I'm getting permission denied errors, what should I do?

What do I need to get started with Compliance Manager?

Can you explain what Security Command Center Enterprise is?

How do I find my organization ID?
```

## Common Questions

### "Compliance Manager is not enabled"
Ask the extension: "How do I enable Compliance Manager?" and it will guide you through the process.

### "No frameworks found"
This usually means Compliance Manager isn't enabled yet. The extension can help you enable it.

### "Permission denied"
Ask: "What permissions do I need for Compliance Manager?" and verify you have the required IAM roles.

## Tips

1. **Be conversational** - Ask questions naturally
2. **Provide context** - Mention your organization ID, project ID, etc.
3. **Ask for help** - Gemini can explain concepts and guide you through setup
4. **Start simple** - Begin with listing frameworks before deploying
5. **Enable first** - Make sure Compliance Manager is enabled in your organization

