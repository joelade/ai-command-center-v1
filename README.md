# n8n Workflow Automation Platform

**Author:** Joel Adelubi  
**Version:** 1.0  
**License:** Open Source

A powerful, open-source workflow automation platform for integrating applications and automating complex business processes. n8n allows you to create sophisticated workflows without coding.

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- In the workspace directory

### Start n8n

Run the following command from the workspace directory:

```bash
docker compose -f docker-compose.n8n.yml up -d
```

This will start:
- **PostgreSQL Database** (port 5432) - Workflow data persistence
- **n8n Workflow Engine** (port 5678) - Workflow automation runtime

### Access n8n

Once running, open your browser and navigate to:

```
http://localhost:5678
```

### Stop n8n

```bash
docker compose -f docker-compose.n8n.yml down
```

### Stop and Remove All Data

To completely remove the containers and volumes (clears all workflows and data):

```bash
docker compose -f docker-compose.n8n.yml down -v
```

## Configuration

### Environment Variables

The setup uses PostgreSQL as the database backend, which is recommended for production environments.

Edit `.env` to customize:
- `N8N_HOST` - Hostname/IP (default: localhost)
- `N8N_PORT` - n8n port (default: 5678)
- `DB_TYPE` - Database type (default: postgres)
- `DB_USER` - PostgreSQL username
- `DB_PASSWORD` - PostgreSQL password
- `DB_NAME` - Database name

### View Logs

Check service logs to troubleshoot:

```bash
docker compose -f docker-compose.n8n.yml logs -f n8n
```

View database logs:

```bash
docker compose -f docker-compose.n8n.yml logs -f postgres
```

## Services

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| **n8n** | 5678 | http://localhost:5678 | Workflow automation UI and engine |
| **PostgreSQL** | 5432 | - | Workflow data storage |

## Usage

### Creating Your First Workflow

1. **Access n8n**: Open http://localhost:5678 in your browser
2. **Create New Workflow**: Click "New Workflow" button
3. **Add Nodes**: Search and add nodes from the node library
4. **Connect Nodes**: Link nodes together by connecting outputs to inputs
5. **Test**: Click "Test" or "Execute" to run the workflow
6. **Deploy**: Once satisfied, the workflow runs on schedule or trigger

### Available Nodes

n8n comes with hundreds of pre-built nodes for:
- **Communication**: Email, Slack, Teams, Discord
- **Data**: HTTP requests, databases, APIs
- **Business Apps**: Salesforce, HubSpot, Stripe, Shopify
- **Cloud Services**: AWS, Google Cloud, Azure
- **Utilities**: Transformers, code execution, conditionals
- **Scheduling**: Cron jobs, timers, webhooks

### Integration Examples

#### Example 1: HTTP Request to External API

1. Add "HTTP Request" node
2. Set method (GET, POST, etc.)
3. Enter URL and headers
4. Execute to see response
5. Map response data to next node

#### Example 2: Webhook Trigger

1. Add "Webhook" node as trigger
2. Copy the webhook URL
3. Configure external service to POST to that URL
4. Add processing nodes
5. Deploy workflow

#### Example 3: Database Operations

1. Add "Postgres" node
2. Configure connection settings
3. Write SQL queries
4. Execute to read/write data

## Useful Commands

### Check Container Status
```bash
docker compose -f docker-compose.n8n.yml ps
```

### View n8n Logs
```bash
docker compose -f docker-compose.n8n.yml logs -f n8n
```

### View Database Logs
```bash
docker compose -f docker-compose.n8n.yml logs postgres
```

### View Database
Access PostgreSQL database directly:

```bash
docker exec -it n8n-postgres psql -U n8n -d n8n
```

Then you can run SQL queries:
```sql
-- List all workflows
SELECT id, name, active FROM n8n_workflow;

-- List executions
SELECT id, workflowId, startedAt, stoppedAt, status FROM n8n_execution ORDER BY startedAt DESC LIMIT 10;
```

### Restart Services
Restart individual services without stopping others:

```bash
docker compose -f docker-compose.n8n.yml restart n8n
```

### Update to Latest n8n Image
```bash
docker compose -f docker-compose.n8n.yml pull
docker compose -f docker-compose.n8n.yml up -d
```

### Backup Workflows

Backup your workflows and credentials:

```bash
# Create backup directory
mkdir -p n8n-backup

# Copy database container data
docker cp n8n-postgres:/var/lib/postgresql/data n8n-backup/postgres-data

# Or export specific data via psql
docker exec n8n-postgres pg_dump -U n8n n8n > n8n-backup/n8n-backup.sql
```

### Restore from Backup

```bash
docker exec -i n8n-postgres psql -U n8n n8n < n8n-backup/n8n-backup.sql
```

## Troubleshooting

### Port Already in Use
If port 5678 is in use, modify `docker-compose.n8n.yml`:
```yaml
ports:
  - "5679:5678"  # Use 5679 instead
```

Then access n8n at http://localhost:5679

### Database Connection Issues
Wait a few seconds for PostgreSQL to be ready. Check logs:
```bash
docker compose -f docker-compose.n8n.yml logs postgres
```

If still having issues, restart the database:
```bash
docker compose -f docker-compose.n8n.yml restart postgres
```

### Permission Issues (Linux/Mac)
```bash
sudo docker compose -f docker-compose.n8n.yml up -d
```

### n8n Won't Start
Check the logs for specific errors:
```bash
docker compose -f docker-compose.n8n.yml logs n8n | tail -50
```

Common issues:
- **Database not ready**: Wait a few seconds and try accessing the UI again
- **Port in use**: Change the port in docker-compose.n8n.yml
- **Volume permissions**: Ensure Docker has access to the data volumes

### Memory/CPU Issues
If n8n is slow or crashes, increase resource limits in `docker-compose.n8n.yml`:

```yaml
services:
  n8n:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Workflows Not Executing
1. Check if n8n service is running: `docker compose -f docker-compose.n8n.yml ps`
2. Check n8n logs for errors
3. Verify workflow is active/enabled
4. Check credentials are properly configured

### Webhook Not Triggering
1. Ensure workflow is active
2. Verify external service is posting to correct endpoint
3. Check n8n logs for webhook events
4. Test webhook manually:
   ```bash
   curl -X POST http://localhost:5678/webhook/your-workflow-id \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```

## Integration Guide

### Connect to External APIs

1. Create a new workflow
2. Add "HTTP Request" node
3. Set up authentication (API key, OAuth, Basic auth)
4. Configure request parameters
5. Test and monitor responses

### Common Integrations

**Slack Integration:**
- Add "Slack" node
- Connect with workspace API token
- Choose action (send message, post to channel, etc.)

**Email Integration:**
- Add "Email Send" node
- Configure SMTP settings
- Set recipients, subject, and content

**Database Integration:**
- Add database-specific node (Postgres, MySQL, etc.)
- Configure connection details
- Write SQL queries

**Webhook Integration:**
- Add "Webhook" node as trigger
- Copy webhook URL
- Configure external service to POST to URL
- Deploy workflow

## Jira & Zephyr Scale Integration

### Overview

n8n integrates seamlessly with Jira and Zephyr Scale for automated test case management, issue tracking, and quality assurance workflows.

### Prerequisites

- Jira Cloud instance with API token
- Zephyr Scale (Cloud) add-on installed in Jira
- API credentials in `.env.n8n`

### Quick Setup

1. **Get Jira API Token**: https://id.atlassian.com/manage-profile/security/api-tokens
2. **Add Jira Credential** to n8n:
   - Go to Credentials → New → Jira
   - Host: `https://yourinstance.atlassian.net/`
   - Email & API Token
   - Save
3. **Configure Zephyr**: Use HTTP Request node with Bearer token authentication

### Key Integration Features

| Feature | Use Case |
|---------|----------|
| **Auto-create Test Cases from Bugs** | Bug created in Jira → Create test case in Zephyr |
| **Update Issue Status from Tests** | Test execution completed → Update Jira issue |
| **Sync Test Results** | Scheduled sync of test executions to Jira |
| **Auto-link Issues & Tests** | Link created issues to corresponding test cases |
| **Webhook Triggers** | React to Jira events (created, updated, transitioned) |

### Common Workflows

**Create Jira Issue:**
```bash
POST /rest/api/3/issues
{
  "fields": {
    "project": {"key": "LE"},
    "summary": "Issue title",
    "description": "Issue details",
    "issuetype": {"name": "Bug"}
  }
}
```

**Create Zephyr Test Case:**
```bash
POST /rest/atm/1.0/testcase
{
  "name": "Test Case Name",
  "projectKey": "LE",
  "priority": 1,
  "objective": "Test objective"
}
```

**Get Jira Issues:**
```bash
GET /rest/api/3/search?jql=project=LE
```

### Key API Endpoints

**Jira:**
- Create: `POST /rest/api/3/issues`
- Search: `GET /rest/api/3/search`
- Update: `PUT /rest/api/3/issues/{key}`
- Transition: `POST /rest/api/3/issues/{key}/transitions`

**Zephyr Scale:**
- Create Test Case: `POST /rest/atm/1.0/testcase`
- Get Test Cases: `GET /rest/atm/1.0/testcase`
- Create Test Execution: `POST /rest/atm/1.0/testexecution`
- Update Execution: `PUT /rest/atm/1.0/testexecution/{id}`

### Webhooks

**Set up Jira webhook to trigger n8n:**
1. Go to Jira Settings → System → Webhooks
2. Create webhook pointing to: `http://localhost:5678/webhook/jira`
3. Select events (created, updated, etc.)
4. In n8n, add Webhook trigger node with path `/jira`

### Complete Guide

See **[N8N_JIRA_ZEPHYR_SETUP.md](N8N_JIRA_ZEPHYR_SETUP.md)** for:
- Detailed setup instructions
- Full workflow examples with JSON
- Troubleshooting guide
- Rate limiting strategies
- Advanced automation patterns

## Documentation

For more information about n8n:
- [Official n8n Documentation](https://docs.n8n.io/)
- [n8n Node Reference](https://docs.n8n.io/nodes/)
- [Workflow Templating](https://docs.n8n.io/workflows/)
- [API Documentation](https://docs.n8n.io/api/)

## License

n8n is open-source and available under the Sustainable Use License (SUL) and the Server Side Public License (SSPL).

