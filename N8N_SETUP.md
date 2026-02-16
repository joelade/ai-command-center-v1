# N8N Local Docker Setup Guide

## Quick Start

### Start n8n

Run the following command from the workspace directory:

```bash
docker compose -f docker-compose.n8n.yml up -d
```

This will start:
- **PostgreSQL Database** (port 5432)
- **n8n Workflow Engine** (port 5678)

### Access n8n

Once running, open your browser and navigate to:

```
http://localhost:5678
```

### Stop n8n

```bash
docker compose -f docker-compose.n8n.yml down
```

### Stop and Remove Data

To completely remove the containers and volumes (clears all workflows and data):

```bash
docker compose -f docker-compose.n8n.yml down -v
```

## Configuration

The setup uses PostgreSQL as the database backend, which is recommended for production environments.

### Environment Variables

Edit `.env.n8n` to customize:
- `N8N_HOST` - Hostname/IP (default: localhost)
- `N8N_PORT` - n8n port (default: 5678)
- `DB_USER` - PostgreSQL username
- `DB_PASSWORD` - PostgreSQL password
- `DB_NAME` - Database name

### View Logs

```bash
docker compose -f docker-compose.n8n.yml logs -f n8n
```

## Integration with Existing Services

To integrate n8n with your other services (Ollama, Open WebUI, etc.), you can:

1. **Add n8n to the main docker-compose.yml** and use internal Docker networking
2. **Use webhook integration** to trigger n8n workflows from other services
3. **Call n8n APIs** from your orchestrator service

### Example: Trigger n8n Workflow from Python

```python
import requests

# Trigger a webhook
response = requests.post(
    'http://n8n:5678/webhook/<workflow-id>',
    json={'data': 'your data here'}
)
```

## Useful Commands

### Check container status
```bash
docker compose -f docker-compose.n8n.yml ps
```

### View database
```bash
docker exec -it n8n-postgres psql -U n8n -d n8n
```

### Restart services
```bash
docker compose -f docker-compose.n8n.yml restart n8n
```

### Update to latest n8n image
```bash
docker compose -f docker-compose.n8n.yml pull
docker compose -f docker-compose.n8n.yml up -d
```

## Troubleshooting

### Port Already in Use
If port 5678 is in use, modify the docker-compose.n8n.yml:
```yaml
ports:
  - "5679:5678"  # Use 5679 instead
```

### Database Connection Issues
Wait a few seconds for PostgreSQL to be ready. Check logs:
```bash
docker compose -f docker-compose.n8n.yml logs postgres
```

### Permission Issues (Linux/Mac)
```bash
sudo docker compose -f docker-compose.n8n.yml up -d
```
