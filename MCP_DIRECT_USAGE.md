# Using MCP Directly in OpenWebUI (Without Functions)

## 🎯 Direct MCP Integration in OpenWebUI

OpenWebUI can use MCP tools directly in conversations **if the MCP server is properly configured**. Here's how to set it up correctly.

---

## ⚙️ Step 1: Verify Your Current MCP Setup

Your MCP server is running, but we need to ensure OpenWebUI can discover and use it properly.

### Check MCP Server Status
```bash
# Verify MCP is running
docker ps | grep mcp-filesystem

# Test direct access
curl http://localhost:3333/

# Test file reading
curl http://localhost:3333/files/questions.md
```

Expected output: File listing with `questions.md`, `answers.md`, `test.txt`

---

## 🔧 Step 2: Configure OpenWebUI Environment Variables

The key is properly setting up OpenWebUI's MCP configuration. Update `docker-compose.yml`:

### Current Configuration (What You Have)
```yaml
open-webui:
  environment:
    - ENABLE_MCP=true
    - MCP_SERVERS=http://mcp-filesystem:3333
```

### Correct Configuration (What You Need)
```yaml
open-webui:
  environment:
    - ENABLE_MCP=true
    - MCP_SERVER_URL=http://mcp-filesystem:3333
    - MCP_FILESYSTEM_ROOT=/app/data
    - MCP_ENABLE_FILESYSTEM=true
```

### Or In OpenWebUI Settings

1. **Open OpenWebUI** → http://localhost:3000
2. **Go to Settings** (⚙️ icon)
3. **Find MCP Configuration section**
4. **Set:**
   ```
   MCP Server URL: http://mcp-filesystem:3333
   Enable Filesystem: true
   Root Path: /app/data
   ```

---

## 📡 Step 3: Use MCP Tools Directly in Chat

Once configured, you can use MCP tools directly in OpenWebUI without any function setup.

### Method 1: Reference Files by Path (Simplest)

In your chat, just mention the file path and ask OpenWebUI to access it via MCP:

```
@mcp questions.md
@mcp answers.md

Fill in all the <!-- TO BE FILLED --> placeholders in questions.md 
with the corresponding answers from answers.md.
```

### Method 2: Use MCP Tool Syntax

```
I need to use the MCP filesystem to read two files:
- /questions.md
- /answers.md

Please read both files and then fill in the <!-- TO BE FILLED --> 
placeholders with the appropriate answers.
```

### Method 3: Direct Tool Invocation

```
Using the MCP filesystem tools available:

1. Read the file: questions.md
2. Read the file: answers.md
3. Match each Q1-Q10 with A1-A10
4. Fill in all placeholders
5. Return the completed document
```

---

## 🚀 Quick Setup (Copy-Paste Method)

### 1. Stop Current Services
```bash
docker compose down
```

### 2. Update docker-compose.yml

Find the `open-webui` section and update the entire service:

```yaml
  open-webui:
    image: ghcr.io/open-webui/open-webui:latest
    container_name: open-webui
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - ENABLE_RAG=1
      - HF_HUB_DISABLE_TELEMETRY=1
      - ENABLE_MCP=true
      - MCP_SERVERS=http://mcp-filesystem:3333
      - MCP_SERVER_URL=http://mcp-filesystem:3333
      - MCP_ENABLE_FILESYSTEM=true
      - MCP_FILESYSTEM_ROOT=/app/data
    volumes:
      - openwebui:/app/backend/data
    depends_on:
      - ollama
      - mcp-filesystem
    restart: unless-stopped
    networks:
      - ai-command-center-v2-ready_default
```

### 3. Restart Services
```bash
docker compose up -d
```

### 4. Wait for OpenWebUI to Start
```bash
docker compose logs -f open-webui | grep -i "ready\|running\|listening"
```

Wait until you see "listening on" or similar message, then press Ctrl+C

### 5. Access OpenWebUI
Open: http://localhost:3000

---

## 💬 Example Prompts for Direct MCP Usage

### Prompt 1: Simple Answer Filling
```
Access the mcp-data directory using MCP.

Files to read:
- questions.md (has 10 questions with <!-- TO BE FILLED --> placeholders)
- answers.md (has 10 answers labeled A1-A10)

Task: Fill in the placeholders by matching Q1↔A1, Q2↔A2, etc.

Return the completed questions file.
```

### Prompt 2: With Verification
```
Using MCP filesystem access:

1. Read questions.md
2. Read answers.md
3. Verify all 10 questions have matching answers
4. Fill in each <!-- TO BE FILLED --> with the appropriate answer
5. Confirm all 10 are filled correctly
6. Return the completed document

Show a summary of what was filled.
```

### Prompt 3: Detailed Processing
```
MCP Task - Fill ISO/IEC 27002 Answers

Access these files via MCP:
- /questions.md - 10 questions with placeholders
- /answers.md - ISO/IEC 27002 answers with control references

Processing:
1. Extract all answers (A1-A10) with their control references
2. Match each to corresponding question (Q1-Q10)
3. Replace <!-- TO BE FILLED --> with full answer text
4. Preserve all control references [ISO/IEC 27002:2022 – Controls: X.X]
5. Maintain professional formatting

Return: Complete filled document
```

---

## 🔍 How to Verify MCP is Working in OpenWebUI

### Sign 1: MCP Tools Available
- Look for a **tool icon** or **@** symbol in the chat input
- Type `@` and you should see available MCP tools
- Should include filesystem operations

### Sign 2: OpenWebUI Can Access Files
Send this test message:
```
Using MCP, list all files in the data directory and tell me their sizes.
```

If MCP is working, you'll get:
```
Files found:
- questions.md (1261 bytes)
- answers.md (3380 bytes)
- test.txt (24 bytes)
```

### Sign 3: File Reading Works
```
Read the first 10 lines of questions.md using MCP.
```

You should see the actual content from the file.

### Check Logs
```bash
docker logs open-webui | grep -i "mcp\|filesystem"
```

Look for messages like:
- "MCP enabled"
- "Connecting to MCP server"
- "Filesystem tool registered"

---

## 🛠️ Troubleshooting MCP Direct Access

### Issue 1: MCP Tools Not Visible in Chat

**Solution:**
```bash
# Restart OpenWebUI with fresh configuration
docker compose restart open-webui

# Wait 10 seconds
sleep 10

# Check logs
docker logs open-webui | tail -20
```

### Issue 2: "Cannot Access MCP Server" Error

**Check connectivity:**
```bash
# From OpenWebUI container
docker exec open-webui curl http://mcp-filesystem:3333/

# Should return JSON with file list
```

If error, check:
```bash
# Verify network
docker network ls

# Check network connectivity
docker network inspect ai-command-center-v2-ready_default
```

### Issue 3: MCP Responds but Files Not Accessible

**Verify file permissions:**
```bash
# Check mcp-data directory
ls -la mcp-data/

# Check file permissions
ls -la mcp-data/*.md

# Both should be readable (r-- permissions)
```

### Issue 4: OpenWebUI Doesn't See MCP Server

**Try alternative configuration:**

In OpenWebUI Settings:
1. Go to **Settings** → **Models**
2. Look for **Tools** or **Integrations** section
3. Enable "MCP Filesystem" or similar
4. Set URL to: `http://mcp-filesystem:3333`

---

## 📊 Architecture: How Direct MCP Works

```
┌─────────────────┐
│   OpenWebUI     │
│   (Port 3000)   │
│                 │
│  MCP Client ---┐│
└────────────────┘│
                  │
                  │ HTTP Connection
                  │ (Direct TCP)
                  │
                  ▼
┌─────────────────────────────┐
│  MCP Filesystem Server      │
│  (Port 3333)                │
│                             │
│  /files/questions.md        │
│  /files/answers.md          │
│  /files/test.txt            │
└─────────────────────────────┘
         ▲
         │
    Mounts from
    /mcp-data
```

When you use MCP directly:
1. OpenWebUI makes HTTP request to `http://mcp-filesystem:3333/files/questions.md`
2. MCP server reads file from mounted `/app/data` volume
3. Returns file content to OpenWebUI
4. OpenWebUI provides content to language model
5. Model processes and fills in answers

---

## ✨ Complete Direct Usage Example

### Action: Use MCP in OpenWebUI Right Now

1. **Open OpenWebUI:** http://localhost:3000
2. **Create New Chat**
3. **Select a Model** (llama3 or mistral recommended)
4. **Type this exact prompt:**

```
Using the MCP filesystem, read these files from mcp-data:
1. questions.md - contains questions Q1-Q10 with <!-- TO BE FILLED --> placeholders
2. answers.md - contains answers A1-A10 with ISO/IEC 27002:2022 references

Fill in all placeholders by matching:
- Q1 with A1
- Q2 with A2
- ... through Q10 with A10

Return the complete filled document showing all questions with their answers.
```

5. **Send Message**
6. **Model will use MCP to:**
   - Access questions.md
   - Access answers.md
   - Process both files
   - Return filled document

---

## 🎯 Expected Behavior

### ✅ MCP IS Working When:
- Model mentions specific file contents (not making it up)
- Responses reference actual file paths
- Model provides exact content from questions.md and answers.md
- All 10 questions are filled with real answers

### ❌ MCP NOT Working When:
- Model generates random content about different topics
- No file paths mentioned
- Content doesn't match files
- "Cannot access" or timeout errors

---

## 🔑 Key Configuration Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `ENABLE_MCP` | `true` | Enable MCP support |
| `MCP_SERVERS` | `http://mcp-filesystem:3333` | Server endpoint |
| `MCP_SERVER_URL` | `http://mcp-filesystem:3333` | Alternative endpoint config |
| `MCP_ENABLE_FILESYSTEM` | `true` | Enable filesystem access |
| `MCP_FILESYSTEM_ROOT` | `/app/data` | Root directory for files |

---

## 📝 Quick Reference

### To Use MCP Directly:
1. ✅ Services running: `docker compose ps`
2. ✅ MCP accessible: `curl http://localhost:3333/`
3. ✅ OpenWebUI environment configured
4. ✅ OpenWebUI restarted
5. ✅ Type a prompt mentioning file access
6. ✅ Model uses MCP automatically

### No Function Setup Needed!
- No custom code required
- No tool creation necessary
- Just proper configuration + prompts
- MCP handles file access transparently

---

## 🚀 Next Steps

1. **Update docker-compose.yml** with MCP environment variables
2. **Restart OpenWebUI:** `docker compose restart open-webui`
3. **Verify MCP:** Try the test prompts in OpenWebUI
4. **Use directly:** Send file-based prompts to the model
5. **Check logs:** `docker logs open-webui | grep -i mcp`

The key difference: **Functions are optional**. Direct MCP access requires only proper configuration and standard prompts! 🎯
