"""
Example: Triggering n8n Workflows from Python

This module shows how to interact with n8n from your Python services.
Use this in your orchestrator or other services to automate Jira/Zephyr operations.
"""

import requests
import json
import os
from typing import Dict, Any, Optional

# Configuration
N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'http://localhost:5678')
N8N_API_KEY = os.getenv('N8N_API_KEY', '')  # Optional, define in .env if using API key auth


class N8nClient:
    """Client for interacting with n8n workflows and credentials"""
    
    def __init__(self, base_url: str = N8N_BASE_URL, api_key: str = N8N_API_KEY):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if api_key:
            self.headers['X-N8N-API-KEY'] = api_key

    def get_workflows(self) -> Optional[list]:
        """Get all workflows"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/workflows",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching workflows: {e}")
            return None

    def get_workflow_by_name(self, name: str) -> Optional[Dict]:
        """Find workflow by name"""
        workflows = self.get_workflows()
        if workflows:
            for workflow in workflows.get('data', []):
                if workflow.get('name') == name:
                    return workflow
        return None

    def trigger_webhook(self, path: str, data: Dict[str, Any] = None) -> Optional[Dict]:
        """
        Trigger a webhook-enabled workflow
        
        Args:
            path: The webhook path (e.g., 'slack-issue-webhook')
            data: JSON payload to send
            
        Example:
            client.trigger_webhook('slack-issue-webhook', {
                'text': 'Create a new test',
                'user': 'john',
                'channel': 'testing'
            })
        """
        try:
            response = requests.post(
                f"{self.base_url}/webhook/{path}",
                json=data or {},
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Webhook error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error triggering webhook: {e}")
            return None

    def execute_workflow(self, workflow_id: str, data: Dict[str, Any] = None) -> Optional[Dict]:
        """
        Execute a workflow directly
        
        Args:
            workflow_id: The workflow ID
            data: Input data for the workflow
            
        Note: Requires n8n enterprise or API execution enabled
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/workflows/{workflow_id}/execute",
                json=data or {},
                headers=self.headers
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Execution error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error executing workflow: {e}")
            return None

    def get_executions(self, workflow_id: str = None, limit: int = 10) -> Optional[list]:
        """Get workflow executions"""
        try:
            url = f"{self.base_url}/api/v1/executions"
            if workflow_id:
                url += f"?workflowId={workflow_id}"
            url += f"&limit={limit}"
            
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching executions: {e}")
            return None


# ============================================================================
# PRACTICAL EXAMPLES
# ============================================================================

def example_trigger_jira_sync():
    """
    Example: Trigger the Jira-to-Zephyr sync workflow via webhook
    This would sync Jira issues to Zephyr test cases
    """
    client = N8nClient()
    
    print("Starting Jira to Zephyr sync workflow...")
    result = client.trigger_webhook('jira-zephyr-sync', {
        'action': 'sync_issues',
        'project_key': 'LE',
        'issue_type': 'Bug'
    })
    
    if result:
        print(f"✓ Workflow triggered successfully")
        print(f"Response: {json.dumps(result, indent=2)}")
    else:
        print("✗ Failed to trigger workflow")


def example_create_issue_from_orchestrator():
    """
    Example: From your QA Orchestrator, create a Jira issue
    """
    client = N8nClient()
    
    # This would be called from your orchestrator when a test fails
    test_result = {
        'test_name': 'Login Test',
        'status': 'FAILED',
        'error_message': 'Wrong password validation',
        'test_environment': 'Staging',
        'timestamp': '2026-02-12T15:30:00Z'
    }
    
    print("Creating Jira issue from test failure...")
    result = client.trigger_webhook('test-failure-issue', {
        'test_name': test_result['test_name'],
        'error': test_result['error_message'],
        'environment': test_result['test_environment'],
        'timestamp': test_result['timestamp']
    })
    
    if result:
        print(f"✓ Jira issue created: {result.get('key')}")
    else:
        print("✗ Failed to create issue")


def example_update_test_status():
    """
    Example: Update test status in Zephyr based on test execution results
    """
    client = N8nClient()
    
    test_execution = {
        'test_case_id': 'TC-123',
        'status': 'PASS',
        'duration': '2.5s',
        'execution_date': '2026-02-12'
    }
    
    print("Updating Zephyr test execution...")
    result = client.trigger_webhook('update-zephyr-status', {
        'test_case_id': test_execution['test_case_id'],
        'status': test_execution['status'],
        'duration': test_execution['duration']
    })
    
    if result:
        print(f"✓ Test status updated")
    else:
        print("✗ Failed to update status")


def example_list_workflows():
    """
    Example: List all available workflows in n8n
    """
    client = N8nClient()
    
    workflows = client.get_workflows()
    if workflows:
        print("Available workflows:")
        for workflow in workflows.get('data', []):
            print(f"  - {workflow['name']} (ID: {workflow['id']})")
    else:
        print("No workflows found or error occurred")


# ============================================================================
# ORCHESTRATOR INTEGRATION EXAMPLE
# ============================================================================

def integrate_with_orchestrator(test_result: Dict[str, Any]):
    """
    Integration function to call from your orchestrator main.py
    
    This function handles test results and triggers appropriate n8n workflows
    
    Usage in orchestrator/main.py:
        from n8n_client import integrate_with_orchestrator
        
        @app.post("/run-tests")
        async def run_tests():
            test_result = {...}  # Your test results
            integrate_with_orchestrator(test_result)
    """
    client = N8nClient()
    
    # If tests failed, create Jira issue
    if test_result.get('failed_count', 0) > 0:
        print(f"Creating Jira issue for {test_result['failed_count']} failed tests...")
        client.trigger_webhook('test-failure-issue', {
            'failed_count': test_result['failed_count'],
            'test_names': test_result.get('failed_tests', []),
            'environment': test_result.get('environment', 'Unknown'),
            'timestamp': test_result.get('timestamp')
        })
    
    # Update Zephyr with execution results
    if test_result.get('total_count', 0) > 0:
        print("Syncing results to Zephyr...")
        client.trigger_webhook('update-zephyr-status', {
            'total': test_result['total_count'],
            'passed': test_result.get('passed_count', 0),
            'failed': test_result.get('failed_count', 0),
            'skipped': test_result.get('skipped_count', 0),
            'duration': test_result.get('duration_seconds')
        })


if __name__ == '__main__':
    print("n8n Integration Examples")
    print("=" * 60)
    
    # Uncomment to run examples:
    # example_list_workflows()
    # example_trigger_jira_sync()
    # example_create_issue_from_orchestrator()
    # example_update_test_status()
    
    print("\nTo use these examples in your code:")
    print("1. Import the N8nClient class")
    print("2. Create an instance: client = N8nClient()")
    print("3. Call methods like trigger_webhook() or execute_workflow()")
