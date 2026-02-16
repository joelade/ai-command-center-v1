# n8n Jira & Zephyr Integration Setup Guide

## Overview

This guide shows you how to integrate Jira and Zephyr Scale with n8n for automated test case management and issue tracking.

## Prerequisites

- n8n running on `http://localhost:5678`
- Jira Cloud instance with API token
- Zephyr Scale (Cloud) add-on installed in Jira
- Credentials from `.env.n8n`

## Step 1: Get Your Jira Credentials

1. Go to your Jira Cloud instance
2. Create an API token:
   - Navigate to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Copy the token (you won't see it again)
3. Your email and base URL are already configured in `mcp-jira-zephyr/.env`

## Step 2: Add Jira Credential to n8n

1. Open n8n at `http://localhost:5678`
2. Go to **Credentials** (left sidebar)
3. Click **+ New** and select **Jira**
4. Fill in:
   - **Host**: `https://loginvsi.atlassian.net/` (your Jira URL)
   - **Email**: `j.adelubi@loginvsi.com`
   - **API Token**: (paste your API token)
5. Click **Save**

## Step 3: Add Zephyr Credentials to n8n

Since Zephyr Scale uses the same API token as Jira:

1. Go to **Credentials** in n8n
2. Click **+ New** and select **HTTP Request**
3. Name it "Zephyr Scale"
4. Set **Authentication** to "Header Auth"
5. Add header:
   - **Name**: `Authorization`
   - **Value**: `Bearer YOUR_API_TOKEN`
6. Click **Save**

## Workflow Examples

### Example 1: Create Jira Issue from n8n

```json
{
  "nodes": [
    {
      "parameters": {
        "headers": {},
        "method": "POST",
        "url": "https://loginvsi.atlassian.net/rest/api/3/issues",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpBasicAuth",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "fields",
              "value": {
                "project": {
                  "key": "LE"
                },
                "summary": "Test Issue from n8n",
                "description": "Created via n8n automation",
                "issuetype": {
                  "name": "Bug"
                }
              }
            }
          ]
        }
      },
      "name": "Create Jira Issue",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [250, 300]
    }
  ],
  "connections": {}
}
```

### Example 2: Get Jira Issues

Create a workflow that fetches issues from a project:

```json
{
  "nodes": [
    {
      "parameters": {
        "jiraCredentialType": "cloudApi",
        "resource": "issue",
        "operation": "search",
        "jql": "project = LE",
        "maxResults": 10
      },
      "name": "Get Jira Issues",
      "type": "n8n-nodes-base.jira",
      "typeVersion": 2,
      "position": [250, 300]
    }
  ],
  "connections": {}
}
```

### Example 3: Create Test Case in Zephyr Scale

```json
{
  "nodes": [
    {
      "parameters": {
        "url": "https://loginvsi.atlassian.net/rest/atm/1.0/testcase",
        "method": "POST",
        "headers": {
          "Authorization": "Bearer YOUR_API_TOKEN",
          "Content-Type": "application/json"
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "name",
              "value": "Test Case from n8n"
            },
            {
              "name": "projectKey",
              "value": "LE"
            },
            {
              "name": "priority": 1
            },
            {
              "name": "objective",
              "value": "Test objective"
            }
          ]
        }
      },
      "name": "Create Zephyr Test Case",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [250, 300]
    }
  ],
  "connections": {}
}
```

## Common APIs

### Jira API Endpoints

- **Create Issue**: `POST /rest/api/3/issues`
- **Get Issues**: `GET /rest/api/3/search?jql=...`
- **Get Issue**: `GET /rest/api/3/issues/{issueIdOrKey}`
- **Update Issue**: `PUT /rest/api/3/issues/{issueIdOrKey}`
- **Transition Issue**: `POST /rest/api/3/issues/{issueIdOrKey}/transitions`

### Zephyr Scale API Endpoints

- **Create Test Case**: `POST /rest/atm/1.0/testcase`
- **Get Test Cases**: `GET /rest/atm/1.0/testcase?projectKey=...`
- **Create Test Cycle**: `POST /rest/atm/1.0/testcycle`
- **Create Test Execution**: `POST /rest/atm/1.0/testexecution`
- **Update Test Execution**: `PUT /rest/atm/1.0/testexecution/{id}`

## Setting Up Webhooks

### Jira Webhooks (send events to n8n)

1. In Jira, go to **Settings → System → Webhooks**
2. Click **Create a webhook**
3. Configure:
   - **URL**: `http://localhost:5678/webhook/jira`
   - **Events**: Select `updated`, `created`, etc.
4. Test and save

Then in n8n, create a webhook trigger:
1. Add **Webhook** trigger node
2. Set **Path**: `/jira`
3. The node will generate a unique ID for your webhook URL

## Workflow Automation Ideas

1. **Auto-create Test Cases from Bugs**
   - Trigger: Bug created in Jira
   - Action: Create corresponding test case in Zephyr

2. **Update Bug Status from Test Execution**
   - Trigger: Test execution completed in Zephyr
   - Action: Update linked Jira issue status

3. **Sync Test Results**
   - Trigger: Scheduled (daily/weekly)
   - Action: Fetch test execution results and post to Jira

4. **Auto-link Issues and Tests**
   - Trigger: Issue created in Jira
   - Action: Create test case and link to issue

## Troubleshooting

### "Unauthorized" Error
- Verify API token is correct
- Check email address matches Jira account
- Regenerate token if needed

### "Project not found"
- Verify project key is correct (usually visible in issue keys like `LE-123`)
- Check credentials have access to the project

### CORS Issues
- Use n8n's HTTP Request node with proper headers
- Ensure `Content-Type: application/json` is set
- Add `Authorization: Bearer YOUR_TOKEN` header

### Rate Limiting
- Jira Cloud has rate limits (100 requests per 10 seconds)
- Use delays in workflows if processing many items
- Add exponential backoff for retries

## Resources

- Jira API Docs: https://developer.atlassian.com/cloud/jira/rest/v3/
- Zephyr Scale API: https://docs.zephyrscale.smartbear.com/api/
- n8n Jira Node: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.jira/
- n8n HTTP Request: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
