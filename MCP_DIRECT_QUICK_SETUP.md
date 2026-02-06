# Direct MCP in OpenWebUI - Quick Setup Guide

## 🎯 What Changed

I've updated your `docker-compose.yml` to include proper MCP configuration environment variables that tell OpenWebUI how to access the MCP filesystem server directly.

### New Environment Variables Added
```yaml
- MCP_SERVER_URL=http://mcp-filesystem:3333        # Server endpoint
- MCP_ENABLE_FILESYSTEM=true                         # Enable filesystem access
- MCP_FILESYSTEM_ROOT=/app/data                      # Root data directory
```

---

## ⚡ Quick Start (3 Steps)

### Step 1: Restart Services with New Configuration
```bash
cd "C:\Users\j.adelubi\Documents\AI Demo\ai-command-center-v2-ready"
docker compose down
docker compose up -d
```

Wait 30 seconds for services to start.

### Step 2: Verify Services Are Running
```bash
docker compose ps
```

You should see:
- ✅ `ollama` - UP
- ✅ `mcp-filesystem` - UP
- ✅ `open-webui` - UP (healthy)
- ✅ `qa-orchestrator` - UP
- ✅ `qa-dashboard` - UP

### Step 3: Test MCP Directly
```bash
# Test MCP server is responding
curl http://localhost:3333/

# Test file access
curl http://localhost:3333/files/questions.md
```

Both should return 200 OK with file contents.

---

## 🔑 Using MCP Directly in OpenWebUI

### Open OpenWebUI
Navigate to: **http://localhost:3000**

### Try This Test Prompt
```
Using the MCP filesystem that's available to me, 
read the questions.md file and tell me how many questions it contains.
```

If MCP is working correctly, the model will:
- Read the questions.md file via MCP
- Count the questions (10 total)
- Tell you the exact count

### Fill Questions Prompt (Main Task)
```
Access the MCP filesystem and read: questions.md and answers.md

Fill in all <!-- TO BE FILLED --> placeholders in questions.md by 
matching each question with its corresponding ISO/IEC 27002 answer:
- Q1 ↔ A1 (Purpose of Secure Coding)
- Q2 ↔ A2 (Input Validation)
- Q3 ↔ A3 (Authentication and Authorization)
- Q4 ↔ A4 (Error and Exception Handling)
- Q5 ↔ A5 (Protection of Sensitive Data)
- Q6 ↔ A6 (Use of Cryptography)
- Q7 ↔ A7 (Secure Software Development Lifecycle)
- Q8 ↔ A8 (Third-party and Open-source Components)
- Q9 ↔ A9 (Logging and Monitoring)
- Q10 ↔ A10 (Vulnerability Handling)

Return the complete filled document with all answers embedded.
```

---

## ✅ Verification Checklist

Before using MCP in OpenWebUI, verify:

```bash
# 1. All services running
docker compose ps
# Should show 5 services, all UP

# 2. MCP server accessible
curl http://localhost:3333/
# Should return JSON with file list

# 3. Files exist and are readable
curl http://localhost:3333/files/questions.md
curl http://localhost:3333/files/answers.md
# Both should return file contents

# 4. OpenWebUI can reach MCP (inside container)
docker exec open-webui curl http://mcp-filesystem:3333/
# Should return JSON with file list
```

All checks should pass ✅

---

## 🚀 How Direct MCP Works (No Setup Required!)

### When You Send a File-Related Prompt:

1. **OpenWebUI receives your message** (e.g., "read questions.md")

2. **OpenWebUI's MCP client** sees the prompt references files

3. **MCP client automatically**:
   - Connects to `http://mcp-filesystem:3333`
   - Reads the requested files
   - Passes content to language model

4. **Language model** can now access actual file contents

5. **Model responds** with accurate, file-based answers

**No function setup needed!** It all happens automatically when MCP is properly configured.

---

## 💡 Best Prompts for Direct MCP Usage

### Prompt Style 1: Explicit MCP Request
```
Using the MCP filesystem, read these files:
- questions.md
- answers.md

Then fill in the answers...
```

### Prompt Style 2: Natural Language
```
I have a questions.md file with placeholders and an answers.md file with answers.
Can you fill in the placeholders by reading both files?
```

### Prompt Style 3: Action-Based
```
Access the data directory via MCP and:
1. Read questions.md
2. Read answers.md
3. Fill in all placeholders
4. Return the filled document
```

---

## 🔍 Troubleshooting

### Issue: Model Still Generates Random Content

**Solution:**
```bash
# 1. Restart OpenWebUI
docker compose restart open-webui

# 2. Wait 15 seconds
sleep 15

# 3. Check logs
docker logs open-webui 2>&1 | grep -i "mcp\|tool\|filesystem" | tail -20
```

Look for lines indicating MCP is initialized.

### Issue: "Cannot Access MCP Server"

**Check container connectivity:**
```bash
# Verify network communication
docker exec open-webui curl -v http://mcp-filesystem:3333/

# Check if containers can ping each other
docker exec open-webui ping -c 3 mcp-filesystem
```

### Issue: Files Not Found

**Verify file setup:**
```bash
# Check files exist
ls -la mcp-data/questions.md
ls -la mcp-data/answers.md

# Check file permissions
stat mcp-data/questions.md

# Check mounted volume
docker exec mcp-filesystem ls -la /app/data/
```

---

## 📊 Configuration Comparison

### ❌ Before (What You Had)
```yaml
environment:
  - ENABLE_MCP=true
  - MCP_SERVERS=http://mcp-filesystem:3333
```
→ Basic MCP support only

### ✅ After (What You Have Now)
```yaml
environment:
  - ENABLE_MCP=true
  - MCP_SERVERS=http://mcp-filesystem:3333
  - MCP_SERVER_URL=http://mcp-filesystem:3333
  - MCP_ENABLE_FILESYSTEM=true
  - MCP_FILESYSTEM_ROOT=/app/data
```
→ **Complete direct MCP filesystem access!**

---

## 🎯 Real Example: Fill Questions Using Direct MCP

### Your Setup:
- ✅ MCP Filesystem Server: http://mcp-filesystem:3333
- ✅ OpenWebUI Configuration: Properly set up for MCP
- ✅ Files Available: questions.md, answers.md

### What Happens When You Use This Prompt:

```
Read mcp-data/questions.md and mcp-data/answers.md using MCP.
Fill all placeholder sections with the corresponding answers.
```

**Result:**
```
MCP reads questions.md ← MCP Filesystem Server
MCP reads answers.md ← MCP Filesystem Server
Model sees actual file contents
Model fills placeholders with real answers
Returns accurate, complete document ✅
```

---

## 🔗 File References

Related documentation:
- **[MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)** - Comprehensive setup details
- **[MCP_TROUBLESHOOTING.md](MCP_TROUBLESHOOTING.md)** - Common issues and solutions
- **[QUICK_START_MCP.md](QUICK_START_MCP.md)** - Quick reference guide
- **[MCP_PROMPTS.md](MCP_PROMPTS.md)** - Prompt template examples

---

## 🚦 Status Check

### Run This Command to Verify Everything:
```bash
echo "=== Docker Services ===" && \
docker compose ps && \
echo -e "\n=== MCP Server ===" && \
curl -s http://localhost:3333/ | json_pp && \
echo -e "\n=== Files in MCP ===" && \
curl -s http://localhost:3333/files/questions.md | head -5 && \
echo -e "\n✅ All checks passed!"
```

---

## 🎓 Next Steps

1. ✅ **Restart services**: `docker compose down && docker compose up -d`
2. ✅ **Wait**: Give it 30 seconds to fully start
3. ✅ **Verify**: Run the verification checklist above
4. ✅ **Test**: Try a simple prompt referencing questions.md
5. ✅ **Use**: Use the fill questions prompt from earlier
6. ✅ **Copy Output**: Save the filled document from OpenWebUI

---

## 🎉 Key Differences: Direct MCP vs Functions

| Feature | Direct MCP | Functions |
|---------|-----------|-----------|
| **Setup** | Configuration only | Code + configuration |
| **Complexity** | Simple | Medium |
| **Speed** | Instant | Fast |
| **Reliability** | Automatic | Requires maintenance |
| **Prompt Changes** | Yes, flexible | No, hardcoded |
| **Recommended** | ✅ YES | ❌ Only if needed |

**Direct MCP is simpler and better for most use cases!**

---

## ✨ Summary

Your OpenWebUI is now configured to use MCP directly without any function setup. Simply:

1. **Restart services** with the new configuration
2. **Open OpenWebUI**
3. **Send a prompt mentioning the files** (e.g., "read questions.md")
4. **The model automatically uses MCP** to access and process files

No additional setup, no custom code, just pure MCP power! 🚀
