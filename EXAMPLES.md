# Usage Examples

This document provides practical examples of using the Compliance Manager Gemini CLI Extension.

## Table of Contents

- [Basic Discovery](#basic-discovery)
- [Framework Management](#framework-management)
- [Cloud Control Management](#cloud-control-management)
- [Deployment Operations](#deployment-operations)
- [Monitoring and Reporting](#monitoring-and-reporting)
- [Advanced Use Cases](#advanced-use-cases)

## Basic Discovery

### List All Available Frameworks

```
> @compliance-manager-mcp list_frameworks organization_id="123456789012"
```

**Natural Language Alternative**:
```
> Show me all compliance frameworks available in my organization 123456789012
```

### Get Details of a Specific Framework

```
> @compliance-manager-mcp get_framework organization_id="123456789012" framework_id="cis-google-cloud-foundation-v1.3.0"
```

**Natural Language Alternative**:
```
> Tell me about the CIS Google Cloud Foundation framework in organization 123456789012
```

### List All Cloud Controls

```
> @compliance-manager-mcp list_cloud_controls organization_id="123456789012"
```

**Natural Language Alternative**:
```
> What cloud controls are available in my organization?
```

## Framework Management

### Explore Framework Details

```
> I want to understand what the NIST framework includes. Can you get the details for framework "nist-800-53-rev5" in organization 123456789012?
```

### Compare Frameworks

```
> Can you help me compare the CIS and NIST frameworks? First, get the details of both frameworks from organization 123456789012, then summarize the key differences.
```

### Find Frameworks for Specific Compliance Needs

```
> I need to comply with FedRAMP requirements. Can you list all frameworks in organization 123456789012 and identify which ones are related to FedRAMP?
```

## Cloud Control Management

### Inspect a Specific Cloud Control

```
> @compliance-manager-mcp get_cloud_control organization_id="123456789012" cloud_control_id="require-os-login"
```

**Natural Language Alternative**:
```
> Show me the details of the "require-os-login" cloud control
```

### Find Controls Related to Encryption

```
> List all cloud controls in organization 123456789012, then filter and show me only those related to encryption
```

### Understand Control Parameters

```
> I want to understand what parameters are available for the "restrict-public-ip" cloud control. Can you get its details and explain the parameters?
```

## Deployment Operations

### Deploy a Framework to a Project

```
> @compliance-manager-mcp create_framework_deployment parent="projects/my-project-id" framework_deployment_id="cis-deployment-prod" framework_name="organizations/123456789012/locations/global/frameworks/cis-google-cloud-foundation-v1.3.0"
```

**Natural Language Alternative**:
```
> I need to deploy the CIS framework to my production project. The project ID is "my-project-id", the organization is 123456789012, and I want to call the deployment "cis-deployment-prod"
```

### Deploy a Framework to a Folder

```
> Deploy the NIST framework to folder 987654321. Use organization 123456789012 and call the deployment "nist-folder-deployment"
```

### List All Deployments in an Organization

```
> @compliance-manager-mcp list_framework_deployments parent="organizations/123456789012"
```

**Natural Language Alternative**:
```
> Show me all framework deployments in my organization
```

### Get Deployment Status

```
> @compliance-manager-mcp get_framework_deployment parent="projects/my-project-id" framework_deployment_id="cis-deployment-prod"
```

**Natural Language Alternative**:
```
> What's the status of the "cis-deployment-prod" deployment in project my-project-id?
```

### Delete a Framework Deployment

```
> @compliance-manager-mcp delete_framework_deployment parent="projects/my-project-id" framework_deployment_id="cis-deployment-prod"
```

**Natural Language Alternative**:
```
> Remove the CIS framework deployment from my project my-project-id. The deployment ID is "cis-deployment-prod"
```

## Monitoring and Reporting

### Check Compliance Posture

```
> I want to understand my organization's compliance posture. Can you:
1. List all framework deployments in organization 123456789012
2. Get the details of each deployment
3. Summarize which frameworks are deployed and their status
```

### Monitor Cloud Control Deployments

```
> @compliance-manager-mcp list_cloud_control_deployments parent="projects/my-project-id"
```

**Natural Language Alternative**:
```
> Show me all cloud control deployments in my project and their enforcement status
```

### Audit Framework Coverage

```
> I need to audit which projects have compliance frameworks deployed. Can you:
1. List framework deployments for project "project-a"
2. List framework deployments for project "project-b"
3. Compare and tell me which frameworks are deployed in each
```

## Advanced Use Cases

### Multi-Project Deployment

```
> I need to deploy the same CIS framework to multiple projects. Here are the project IDs:
- project-prod
- project-staging
- project-dev

Can you help me create deployments for each with appropriate naming?
```

### Framework Migration

```
> I want to migrate from CIS v1.2 to CIS v1.3. Can you:
1. Show me the current deployment in project my-project-id
2. Help me understand the differences between the two versions
3. Guide me through deleting the old deployment and creating a new one
```

### Compliance Gap Analysis

```
> I need to perform a compliance gap analysis. Can you:
1. List all available frameworks in organization 123456789012
2. List all current deployments in project my-project-id
3. Identify which frameworks are available but not deployed
4. Recommend which frameworks I should consider deploying
```

### Custom Control Configuration

```
> I want to understand how to configure custom parameters for cloud controls. Can you:
1. Get the details of the "restrict-public-ip" control
2. Show me what parameters are available
3. Explain how I would deploy this control with custom settings
```

### Organizational Hierarchy Deployment

```
> I have an organizational hierarchy:
- Organization: 123456789012
  - Folder: production (987654321)
    - Project: prod-app-1
    - Project: prod-app-2
  - Folder: development (876543210)
    - Project: dev-app-1

Help me deploy appropriate frameworks at each level for maximum coverage
```

### Compliance Reporting

```
> Generate a compliance report for my organization. I need:
1. All available frameworks
2. All current deployments across all projects
3. Cloud control deployment status
4. A summary of compliance coverage

Organization ID: 123456789012
Projects to check: project-a, project-b, project-c
```

### Troubleshooting Deployment Issues

```
> My framework deployment seems to be stuck. Can you:
1. Get the deployment status for "cis-deployment-prod" in project my-project-id
2. Check if there are any errors
3. Suggest what might be wrong and how to fix it
```

### Best Practices Consultation

```
> I'm new to Compliance Manager. Can you:
1. Explain what frameworks are available
2. Recommend which framework to start with for a typical web application
3. Guide me through deploying it to my project
4. Explain what happens after deployment

My organization ID is 123456789012 and project ID is my-web-app
```

## Tips for Effective Usage

### 1. Use Natural Language

Gemini CLI understands natural language, so you don't always need to use the exact tool syntax:

**Instead of**:
```
@compliance-manager-mcp list_frameworks organization_id="123456789012"
```

**You can say**:
```
Show me all compliance frameworks in my organization
```

### 2. Chain Operations

You can ask Gemini CLI to perform multiple operations in sequence:

```
> First, list all frameworks in organization 123456789012, then get the details of the CIS framework, and finally show me if it's deployed to project my-project-id
```

### 3. Ask for Explanations

Don't hesitate to ask for explanations:

```
> What's the difference between a framework and a cloud control?
> Explain what happens when I deploy a framework
> What are the implications of deleting a framework deployment?
```

### 4. Request Summaries

Ask for summaries of complex information:

```
> List all frameworks and give me a brief summary of each
> Show me all deployments and summarize their status
```

### 5. Get Recommendations

Leverage Gemini's AI capabilities for recommendations:

```
> Based on my current deployments, what additional frameworks should I consider?
> What's the best practice for deploying compliance frameworks in a multi-project setup?
```

## Common Workflows

### Initial Setup Workflow

1. **Discover available frameworks**
2. **Choose appropriate framework(s)**
3. **Deploy to test project first**
4. **Verify deployment**
5. **Deploy to production projects**

### Ongoing Monitoring Workflow

1. **List all deployments regularly**
2. **Check deployment status**
3. **Review cloud control deployments**
4. **Generate compliance reports**

### Framework Update Workflow

1. **Check for new framework versions**
2. **Review changes in new version**
3. **Test in non-production environment**
4. **Update production deployments**

## Getting Help

If you need help with any operation:

```
> How do I deploy a framework?
> What parameters does the create_framework_deployment tool accept?
> Can you show me an example of deploying the NIST framework?
```

Gemini CLI will provide guidance and examples based on the extension's capabilities.

