# Example Commands for Your Organization

This file contains ready-to-use commands for your specific GCP setup.

## Your Configuration

- **Organization ID**: `1035865795181`
- **Project ID**: `csc-audit-test-project`

## Quick Test Commands

### 1. List All Available Frameworks

```
@compliance-manager-mcp list_frameworks organization_id="1035865795181"
```

**Natural Language Alternative**:
```
Show me all compliance frameworks available in organization 1035865795181
```

### 2. Get Details of a Specific Framework

First, list frameworks to see what's available, then get details:

```
@compliance-manager-mcp get_framework organization_id="1035865795181" framework_id="cis-google-cloud-foundation-v1.3.0"
```

**Natural Language Alternative**:
```
Tell me about the CIS Google Cloud Foundation framework in my organization
```

### 3. List All Cloud Controls

```
@compliance-manager-mcp list_cloud_controls organization_id="1035865795181"
```

**Natural Language Alternative**:
```
What cloud controls are available in my organization?
```

### 4. List Framework Deployments (Organization Level)

```
@compliance-manager-mcp list_framework_deployments parent="organizations/1035865795181"
```

**Natural Language Alternative**:
```
Show me all framework deployments in my organization
```

### 5. List Framework Deployments (Project Level)

```
@compliance-manager-mcp list_framework_deployments parent="projects/csc-audit-test-project"
```

**Natural Language Alternative**:
```
What frameworks are deployed to project csc-audit-test-project?
```

### 6. List Cloud Control Deployments

```
@compliance-manager-mcp list_cloud_control_deployments parent="projects/csc-audit-test-project"
```

**Natural Language Alternative**:
```
Show me cloud control deployments in my test project
```

## Deployment Examples

### Deploy CIS Framework to Your Project

```
@compliance-manager-mcp create_framework_deployment parent="projects/csc-audit-test-project" framework_deployment_id="cis-deployment-test" framework_name="organizations/1035865795181/locations/global/frameworks/cis-google-cloud-foundation-v1.3.0"
```

**Natural Language Alternative**:
```
I want to deploy the CIS Google Cloud Foundation framework to project csc-audit-test-project. Call the deployment "cis-deployment-test"
```

### Check Deployment Status

```
@compliance-manager-mcp get_framework_deployment parent="projects/csc-audit-test-project" framework_deployment_id="cis-deployment-test"
```

**Natural Language Alternative**:
```
What's the status of the cis-deployment-test deployment in my project?
```

### Delete a Deployment

```
@compliance-manager-mcp delete_framework_deployment parent="projects/csc-audit-test-project" framework_deployment_id="cis-deployment-test"
```

**Natural Language Alternative**:
```
Remove the cis-deployment-test deployment from my project
```

## Advanced Workflows

### Complete Compliance Assessment

```
I need to assess the compliance posture of my organization. Can you:
1. List all available frameworks in organization 1035865795181
2. Show me which frameworks are currently deployed to project csc-audit-test-project
3. List all cloud controls available
4. Show me the cloud control deployments in my project
5. Summarize the current compliance status
```

### Deploy Multiple Frameworks

```
I want to deploy compliance frameworks to project csc-audit-test-project. Can you help me:
1. First, show me what frameworks are available in organization 1035865795181
2. Then guide me through deploying the CIS framework
3. After that, help me deploy the NIST framework
4. Finally, verify both deployments are successful
```

### Framework Comparison

```
I need to compare different compliance frameworks. Can you:
1. Get the details of the CIS framework from organization 1035865795181
2. Get the details of the NIST framework
3. Compare them and tell me which one would be better for a financial services application
```

### Troubleshooting Deployments

```
I'm having issues with my framework deployment. Can you:
1. Check the status of deployment "cis-deployment-test" in project csc-audit-test-project
2. List all deployments to see if there are any conflicts
3. Suggest what might be wrong and how to fix it
```

## Natural Language Queries

You can ask Gemini CLI questions in plain English:

### Discovery Questions
```
> What compliance frameworks are available in my organization?
> Explain what the CIS framework does
> What's the difference between CIS and NIST frameworks?
> How many cloud controls are available?
```

### Status Questions
```
> What frameworks are currently deployed to my project?
> Show me the compliance status of project csc-audit-test-project
> Are there any framework deployments in my organization?
> What cloud controls are active in my project?
```

### Action Questions
```
> How do I deploy a compliance framework?
> Can you help me deploy the CIS framework to my test project?
> What happens if I delete a framework deployment?
> How do I check if a deployment was successful?
```

### Analysis Questions
```
> Which framework should I use for a healthcare application?
> What are the best practices for deploying compliance frameworks?
> How can I ensure my project meets HIPAA requirements?
> What controls should I enable for PCI DSS compliance?
```

## Testing Workflow

### Step 1: Verify Extension Works
```
> @compliance-manager-mcp list_frameworks organization_id="1035865795181"
```

### Step 2: Explore Available Frameworks
```
> Show me all frameworks and give me a brief description of each
```

### Step 3: Check Current State
```
> What frameworks are currently deployed to project csc-audit-test-project?
```

### Step 4: Deploy a Test Framework (if needed)
```
> I want to test deploying a framework. Can you help me deploy the CIS framework to my test project with a deployment ID of "test-deployment-001"?
```

### Step 5: Verify Deployment
```
> Check the status of deployment test-deployment-001 in my project
```

### Step 6: Clean Up (if needed)
```
> Remove the test-deployment-001 from my project
```

## Common Use Cases

### Use Case 1: Initial Compliance Setup
```
I'm setting up compliance for the first time. My organization is 1035865795181 and project is csc-audit-test-project. Can you:
1. Show me what frameworks are available
2. Recommend which framework to start with
3. Help me deploy it
4. Verify it's working correctly
```

### Use Case 2: Compliance Audit
```
I need to prepare for a compliance audit. Can you:
1. List all frameworks deployed in my organization
2. Show me all cloud control deployments
3. Generate a summary of our compliance posture
4. Identify any gaps or missing controls
```

### Use Case 3: Framework Migration
```
I want to migrate from one framework to another. Can you:
1. Show me the current deployments in project csc-audit-test-project
2. Help me understand the differences between frameworks
3. Guide me through deploying the new framework
4. Help me remove the old framework after verification
```

## Tips for Success

1. **Start with read-only commands** (list, get) to familiarize yourself
2. **Use natural language** - Gemini CLI understands context
3. **Test in your test project** (csc-audit-test-project) before production
4. **Ask for explanations** - Gemini can explain concepts and guide you
5. **Chain operations** - Ask Gemini to perform multiple steps in sequence

## Getting Help

If you need help with any command:

```
> How do I list frameworks?
> What parameters does create_framework_deployment need?
> Can you show me an example of deploying a framework?
> Explain what happens when I deploy a framework
```

Gemini CLI will provide guidance based on the extension's capabilities and your specific setup.

---

**Your Configuration**:
- Organization: `1035865795181`
- Project: `csc-audit-test-project`

**Ready to start?** Run `gemini` and try any of the commands above!

