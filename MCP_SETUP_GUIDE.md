# MCP Integration Guide for OpenWebUI

## Overview
This guide explains how to use the Model Context Protocol (MCP) in OpenWebUI to access and manipulate files from the `mcp-data/` directory.

## Setup

### 1. Start Services
```bash
docker compose up -d
```

This will start:
- **Ollama** on port 11434 (LLM runtime)
- **OpenWebUI** on port 3000
- **MCP Filesystem Server** on port 3333 (serves files from mcp-data/)

### 2. Access OpenWebUI
Open your browser and go to: **http://localhost:3000**

## Using MCP in OpenWebUI

### Available Endpoints
The MCP filesystem server exposes:

- `GET /` - List all files in mcp-data/
- `GET /files/{path}` - Read file contents (e.g., `/files/questions.md`)
- `GET /static/{path}` - Serve static files

### Example Requests via cURL (for reference)
```bash
# List files
curl http://localhost:3333/

# Read questions
curl http://localhost:3333/files/questions.md

# Read answers
curl http://localhost:3333/files/answers.md
```

## Using MCP to Fill Answers in OpenWebUI

### Method 1: Direct Prompt in OpenWebUI

1. **Open OpenWebUI** (http://localhost:3000)
2. **Create a new chat**
3. **Use this prompt to fill answers:**

```
I need to use MCP to fill in answers from answers.md into questions.md.

Available MCP operations:
- READ questions.md: Contains 10 questions with "<!-- TO BE FILLED -->" placeholders
- READ answers.md: Contains corresponding answers A1-A10

Task:
1. Read both files from the MCP filesystem
2. Match each answer (A1-A10) to corresponding question (Q1-Q10)
3. Replace each "<!-- TO BE FILLED -->" with the appropriate answer
4. Return the completed questions.md with all answers filled in

Please proceed with reading the files and filling in the answers accurately according to ISO/IEC 27002:2022 standards.
```

### Method 2: Create a System Prompt (Recommended)

1. Go to **Settings** → **System Prompt**
2. Add this system message:

```
You are an expert assistant with access to the MCP filesystem server at http://localhost:3333.

You can read files using MCP endpoints:
- /files/questions.md (contains questions with placeholders)
- /files/answers.md (contains ISO/IEC 27002:2022 answers)

When asked to fill answers, you will:
1. Read the questions file
2. Read the answers file
3. Match Q1-Q10 with A1-A10
4. Generate the filled document with all answers in place
5. Present the completed version to the user

Always reference ISO/IEC 27002:2022 when explaining security concepts.
```

### Method 3: Using Custom Tools (Advanced)

Create a custom tool in OpenWebUI that calls the MCP endpoints directly:

```javascript
// Tool: Fill Answers from MCP
async function fillAnswersFromMCP() {
  try {
    // Read questions
    const questionsRes = await fetch('http://localhost:3333/files/questions.md');
    const questions = await questionsRes.text();
    
    // Read answers
    const answersRes = await fetch('http://localhost:3333/files/answers.md');
    const answers = await answersRes.text();
    
    // Process and fill
    return { questions, answers };
  } catch (error) {
    console.error('MCP Error:', error);
    return null;
  }
}
```

## Troubleshooting

### MCP Server Not Responding
```bash
# Check if container is running
docker ps | grep mcp-filesystem

# View logs
docker logs mcp-filesystem

# Check connectivity from OpenWebUI container
docker exec open-webui curl http://mcp-filesystem:3333/
```

### Files Not Found
- Ensure files are in `mcp-data/` directory
- Check file permissions: `ls -la mcp-data/`
- Verify docker volume mount: `docker inspect mcp-filesystem | grep mcp-data`

### Restart Services
```bash
docker compose restart mcp-filesystem open-webui
```

## Files Available via MCP

- `questions.md` - 10 ISO/IEC 27002 secure coding questions
- `answers.md` - Corresponding answers with control references
- `test.txt` - Test file

## Next Steps

1. **Start the services**: `docker compose up -d`
2. **Access OpenWebUI**: http://localhost:3000
3. **Use the prompt above** to fill in answers via MCP
4. **Save the output** to update your questions file

## MCP Server Configuration

The MCP server is configured in `docker-compose.yml`:

```yaml
environment:
  - ENABLE_MCP=true
  - MCP_SERVERS=http://mcp-filesystem:3333
```

This allows OpenWebUI to automatically discover and use the MCP filesystem server.
