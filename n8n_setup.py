#!/usr/bin/env python3
"""
n8n Jira & Zephyr Integration Setup Script

This script automatically configures Jira and Zephyr credentials in n8n
and can import sample workflows.

Usage:
    python n8n_setup.py --add-credentials
    python n8n_setup.py --import-workflows
"""

import json
import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('.env.n8n')
load_dotenv('mcp-jira-zephyr/.env')

N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'http://localhost:5678')
JIRA_BASE_URL = os.getenv('JIRA_BASE_URL', '').rstrip('/')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')
ZEPHYR_API_TOKEN = os.getenv('ZEPHYR_API_TOKEN', JIRA_API_TOKEN)


def get_n8n_headers():
    """Get headers for n8n API requests"""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


def add_jira_credential():
    """Add Jira credential to n8n"""
    print("Adding Jira credential to n8n...")
    
    url = f"{N8N_BASE_URL}/api/v1/credentials"
    
    payload = {
        "name": "Jira",
        "type": "jira",
        "data": {
            "host": JIRA_BASE_URL,
            "user": JIRA_EMAIL,
            "apiToken": JIRA_API_TOKEN
        },
        "nodesAccess": [
            {
                "nodeType": "n8n-nodes-base.jira",
                "user": "owner"
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=get_n8n_headers())
        if response.status_code in [200, 201]:
            credential = response.json()
            print(f"✓ Jira credential created: {credential.get('id')}")
            return credential.get('id')
        else:
            print(f"✗ Failed to create Jira credential: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def add_zephyr_credential():
    """Add Zephyr credential (as HTTP Basic Auth) to n8n"""
    print("Adding Zephyr Scale credential to n8n...")
    
    url = f"{N8N_BASE_URL}/api/v1/credentials"
    
    # Prepare basic auth
    import base64
    auth_string = base64.b64encode(f"{JIRA_EMAIL}:{ZEPHYR_API_TOKEN}".encode()).decode()
    
    payload = {
        "name": "Zephyr Scale",
        "type": "httpBasicAuth",
        "data": {
            "user": JIRA_EMAIL,
            "password": ZEPHYR_API_TOKEN
        },
        "nodesAccess": [
            {
                "nodeType": "n8n-nodes-base.httpRequest",
                "user": "owner"
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=get_n8n_headers())
        if response.status_code in [200, 201]:
            credential = response.json()
            print(f"✓ Zephyr credential created: {credential.get('id')}")
            return credential.get('id')
        else:
            print(f"✗ Failed to create Zephyr credential: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def import_workflow(workflow_name, workflow_data):
    """Import a workflow into n8n"""
    print(f"Importing workflow: {workflow_name}...")
    
    url = f"{N8N_BASE_URL}/api/v1/workflows"
    
    payload = {
        "name": workflow_name,
        "nodes": workflow_data.get('nodes', []),
        "connections": workflow_data.get('connections', {}),
        "active": False
    }
    
    try:
        response = requests.post(url, json=payload, headers=get_n8n_headers())
        if response.status_code in [200, 201]:
            workflow = response.json()
            print(f"✓ Workflow imported: {workflow.get('id')}")
            return workflow.get('id')
        else:
            print(f"✗ Failed to import workflow: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def create_sample_workflows():
    """Create sample workflows"""
    
    # Sample 1: Get Jira Issues
    get_issues_workflow = {
        "name": "Get Jira Issues (LE Project)",
        "nodes": [
            {
                "parameters": {
                    "authentication": "predefinedCredentialType",
                    "nodeCredentialType": "jira",
                    "resource": "issue",
                    "operation": "search",
                    "jql": f"project = {JIRA_PROJECT_KEY}",
                    "maxResults": 20
                },
                "name": "Get Issues",
                "type": "n8n-nodes-base.jira",
                "typeVersion": 2,
                "position": [250, 300]
            },
            {
                "parameters": {
                    "content": "Found {{ $node[\"Get Issues\"].json.total }} issues"
                },
                "name": "Log Results",
                "type": "n8n-nodes-base.executeCommand",
                "typeVersion": 1,
                "position": [450, 300]
            }
        ],
        "connections": {
            "Get Issues": {
                "success": [
                    ["Log Results", 0]
                ]
            }
        }
    }
    
    # Sample 2: Create Jira Issue
    create_issue_workflow = {
        "name": "Create Jira Issue from Template",
        "nodes": [
            {
                "parameters": {
                    "authentication": "predefinedCredentialType",
                    "nodeCredentialType": "jira",
                    "resource": "issue",
                    "operation": "create",
                    "issueTypeField": "Bug",
                    "summary": "Test Issue from n8n",
                    "description": "This is a test issue created via n8n automation",
                    "projectKey": JIRA_PROJECT_KEY,
                    "additionalFields": ""
                },
                "name": "Create Issue",
                "type": "n8n-nodes-base.jira",
                "typeVersion": 2,
                "position": [250, 300]
            }
        ],
        "connections": {}
    }
    
    # Sample 3: Fetch and Log Zephyr Test Cases
    zephyr_workflow = {
        "name": "Get Zephyr Test Cases",
        "nodes": [
            {
                "parameters": {
                    "url": f"{JIRA_BASE_URL}/rest/atm/1.0/testcase?projectKey={JIRA_PROJECT_KEY}",
                    "method": "GET",
                    "authentication": "predefinedCredentialType",
                    "nodeCredentialType": "httpBasicAuth"
                },
                "name": "Get Test Cases",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [250, 300]
            }
        ],
        "connections": {}
    }
    
    workflows = [
        ("Get Jira Issues", get_issues_workflow),
        ("Create Jira Issue", create_issue_workflow),
        ("Get Zephyr Test Cases", zephyr_workflow)
    ]
    
    for workflow_name, workflow_data in workflows:
        import_workflow(workflow_name, workflow_data)


def test_connection():
    """Test if n8n is accessible"""
    try:
        response = requests.get(f"{N8N_BASE_URL}/api/v1/health", headers=get_n8n_headers())
        if response.status_code == 200:
            print(f"✓ n8n is accessible at {N8N_BASE_URL}")
            return True
        else:
            print(f"✗ n8n returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to n8n: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Setup Jira & Zephyr integration in n8n')
    parser.add_argument('--add-credentials', action='store_true', help='Add Jira and Zephyr credentials')
    parser.add_argument('--import-workflows', action='store_true', help='Import sample workflows')
    parser.add_argument('--all', action='store_true', help='Do everything (credentials + workflows)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("n8n Jira & Zephyr Integration Setup")
    print("=" * 60)
    
    # Test connection
    if not test_connection():
        print("\nMake sure n8n is running: docker compose -f docker-compose.n8n.yml up -d")
        return
    
    print(f"\nConfiguration:")
    print(f"  Jira URL: {JIRA_BASE_URL}")
    print(f"  Jira Email: {JIRA_EMAIL}")
    print(f"  Project Key: {JIRA_PROJECT_KEY}")
    print(f"  n8n URL: {N8N_BASE_URL}")
    
    # Execute requested actions
    if args.add_credentials or args.all:
        print("\n" + "-" * 60)
        print("Adding Credentials")
        print("-" * 60)
        add_jira_credential()
        add_zephyr_credential()
    
    if args.import_workflows or args.all:
        print("\n" + "-" * 60)
        print("Importing Workflows")
        print("-" * 60)
        create_sample_workflows()
    
    if not (args.add_credentials or args.import_workflows or args.all):
        print("\nUsage: python n8n_setup.py [OPTIONS]")
        print("  --add-credentials     Add Jira and Zephyr credentials")
        print("  --import-workflows    Import sample workflows")
        print("  --all                 Do everything")
    
    print("\n" + "=" * 60)
    print("Setup complete! Visit: http://localhost:5678")
    print("=" * 60)


if __name__ == '__main__':
    main()
