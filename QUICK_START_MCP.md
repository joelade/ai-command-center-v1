# Quick Start: Using MCP to Fill Answers in OpenWebUI

## ✅ Your Current Setup

Your project is configured to use MCP (Model Context Protocol) with OpenWebUI. Here's what's already in place:

### 1. **MCP Server** (docker-compose.yml)
```yaml
mcp-filesystem:
  - Serves files from: mcp-data/
  - Port: 3333
  - Status: Ready to start
```

### 2. **OpenWebUI Integration**
```yaml
environment:
  - ENABLE_MCP=true
  - MCP_SERVERS=http://mcp-filesystem:3333
```

### 3. **Available Files**
- `mcp-data/questions.md` - 10 ISO/IEC 27002 questions with `<!-- TO BE FILLED -->` placeholders
- `mcp-data/answers.md` - Corresponding answers (A1-A10)
- `mcp-data/test.txt` - Test file

## 🚀 Quick Start (5 Steps)

### Step 1: Start All Services
```bash
docker compose up -d
```

Wait 30 seconds for services to fully initialize.

### Step 2: Verify Services Are Running
```bash
docker compose ps
```

You should see:
- ✅ `ollama` (port 11434)
- ✅ `open-webui` (port 3000)
- ✅ `mcp-filesystem` (port 3333)
- ✅ `qa-orchestrator` (port 8000)
- ✅ `qa-dashboard` (port 8501)

### Step 3: Open OpenWebUI
Navigate to: **http://localhost:3000**

### Step 4: Create a New Chat

Copy and paste **one** of these prompts:

#### 🎯 **Simple Version (Recommended for First Try):**
```
Read mcp-data/questions.md and mcp-data/answers.md.

Fill in all the <!-- TO BE FILLED --> placeholders in questions.md with 
the corresponding answers from answers.md (Q1→A1, Q2→A2, etc).

Return the complete filled document.
```

#### 📋 **Advanced Version (For Detailed Results):**
```
You are an ISO/IEC 27002:2022 expert. Use MCP to:

1. Read mcp-data/questions.md (10 questions with placeholders)
2. Read mcp-data/answers.md (10 answers with control references)
3. Match each Q with its corresponding A
4. Replace each <!-- TO BE FILLED --> with the exact answer text
5. Preserve all ISO/IEC 27002 control references
6. Return the completed questions.md file

Validate that all 10 questions are filled accurately.
```

### Step 5: Copy the Output

The model will return the filled document. Copy and use as needed!

## ✓ Verification Checklist

Before using MCP, verify:

```bash
# Check if all services are running
docker compose ps

# Test MCP server directly
curl http://localhost:3333/

# Test reading questions file
curl http://localhost:3333/files/questions.md

# Test reading answers file
curl http://localhost:3333/files/answers.md

# Verify OpenWebUI can reach MCP
docker exec open-webui curl http://mcp-filesystem:3333/
```

All should return 200 OK or file contents.

## 📚 Available Documentation

- **[MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)** - Comprehensive MCP configuration guide
- **[MCP_PROMPTS.md](MCP_PROMPTS.md)** - 4 Different prompt templates for various use cases
- **[README.md](README.md)** - Full system documentation (see "Using MCP with OpenWebUI" section)

## 🔧 Troubleshooting

### Issue: MCP Server Not Responding
```bash
# Restart the service
docker compose restart mcp-filesystem

# View logs
docker logs mcp-filesystem
```

### Issue: Files Not Found
```bash
# Check mcp-data directory exists
ls -la mcp-data/

# Check file permissions
ls -la mcp-data/questions.md mcp-data/answers.md
```

### Issue: OpenWebUI Can't Access MCP
```bash
# Rebuild and restart
docker compose down
docker compose up -d --build
```

## 💡 Tips for Best Results

1. **Use a Capable Model**: llama3 or mistral work well for this task
2. **Be Specific**: Mention "ISO/IEC 27002" in your prompt for context
3. **Check Output**: Verify all 10 answers are filled (Q1-Q10)
4. **Format**: The answers should match the source content exactly
5. **Save Results**: Copy the output to a file for safekeeping

## 📊 Expected Output

When you use the MCP correctly, you'll get a document like:

```markdown
# Secure Coding – ISO/IEC 27002:2022

## Q1. What is the purpose of secure coding according to ISO/IEC 27002?
Secure coding ensures that software is designed and implemented to prevent 
the introduction of vulnerabilities that could compromise the confidentiality, 
integrity, or availability of information...
[ISO/IEC 27002:2022 – Controls: 8.28]

## Q2. How does ISO/IEC 27002 address input validation in software development?
ISO/IEC 27002 recommends validating all input data to prevent common attacks 
such as injection, buffer overflows, and cross-site scripting...
[ISO/IEC 27002:2022 – Controls: 8.28, 8.25]

... (continues for Q3-Q10)
```

## 🎓 Next Steps

1. ✅ Start services: `docker compose up -d`
2. ✅ Open OpenWebUI: http://localhost:3000
3. ✅ Try a prompt from Step 4 above
4. ✅ Review and save the output
5. ✅ Explore advanced MCP features in [MCP_PROMPTS.md](MCP_PROMPTS.md)

Enjoy using MCP for accurate, AI-assisted content generation! 🚀
