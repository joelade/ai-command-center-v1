# Testing Advanced MCP Multi-Source System

## 🧪 Quick Test Menu

### Test 1: Simple Answer Filler (Recommended First)
```bash
# Test basic markdown processing
python fill_answers.py
```
✅ Expected: `mcp-data/questions_filled.md` created with all 10 answers filled

---

### Test 2: Advanced Multi-Source (Text File)
```bash
python fill_answers_advanced.py --sources answers.md
```
✅ Expected: Same output as Test 1, all 10 answers filled
**Note:** Pass filename only, script auto-adds `mcp-data/` prefix

---

### Test 3: Advanced with Multiple Text Sources
```bash
# Create a test file first
echo "## A1. Test Answer 1" > mcp-data/test-answers.md
echo "## A2. Test Answer 2" >> mcp-data/test-answers.md

# Extract from both (pass filenames only)
python fill_answers_advanced.py \
  --sources \
    answers.md \
    test-answers.md
```
✅ Expected: Combined answers, all sources processed

---

### Test 4: MCP Server (HTTP)
```bash
# Test the MCP filesystem server
curl http://localhost:3333/

# Read a file via MCP
curl http://localhost:3333/files/questions.md

# Read answers via MCP
curl http://localhost:3333/files/answers.md
```
✅ Expected: JSON response with files, then file contents

---

### Test 5: OpenWebUI MCP Integration
1. Open http://localhost:3000
2. Create new chat
3. Try this prompt:
```
Read questions.md and answers.md from the MCP filesystem.
Fill in all <!-- TO BE FILLED --> placeholders.
Return the complete filled document.
```
⚠️ Note: May not work automatically (see SOLUTION_SUMMARY.md)

---

## 🎯 Full Testing Guide

### Setup Phase

**Step 1: Verify Files Exist**
```bash
ls mcp-data/questions.md
ls mcp-data/answers.md
ls fill_answers.py
ls fill_answers_advanced.py
```
✅ All should exist

**Step 2: Verify Docker is Running**
```bash
docker compose ps
```
✅ Should show 5 services (ollama, open-webui, mcp-filesystem, qa-orchestrator, qa-dashboard)

---

### Basic Testing

#### Test A: Simple Script Works
```bash
# Run simple filler
python fill_answers.py

# Check output was created
ls -la mcp-data/questions_filled.md

# View output (first 50 lines)
Get-Content mcp-data/questions_filled.md | Select-Object -First 50
```

**Expected Output:**
```
🔍 Reading files...
   Questions: mcp-data/questions.md
   Answers:   mcp-data/answers.md

✅ Found 10 answers
✅ Filled 10 questions successfully

📄 Output saved to: mcp-data/questions_filled.md

✨ Done!
```

**Verify Output:**
```bash
# Count filled questions
(Get-Content mcp-data/questions_filled.md | Select-String "## Q" | Measure-Object).Count

# Should be 10
```

---

#### Test B: Verify All Answers Present
```bash
# Check for all 10 answers
$filled = Get-Content mcp-data/questions_filled.md -Raw

@(1..10) | ForEach-Object {
    $q = "## Q$_."
    if ($filled -match $q) {
        Write-Host "✅ Q$_ found"
    } else {
        Write-Host "❌ Q$_ missing"
    }
}
```

**Expected:** All 10 Q's should be found ✅

---

### Advanced Testing

#### Test C: Install Advanced Dependencies (Optional)
```bash
# Check what's installed
python -c "
import sys
deps = {
    'requests': 'Web scraping',
    'PIL': 'Image processing',
    'PyPDF2': 'PDF reading',
    'docx': 'Word document reading',
    'pytesseract': 'OCR'
}

for dep, desc in deps.items():
    try:
        __import__(dep)
        print(f'✅ {dep:15} ({desc})')
    except:
        print(f'❌ {dep:15} ({desc}) - Not installed')
"
```

**Install missing (if desired):**
```bash
pip install -r requirements-advanced.txt
```

---

#### Test D: Test Configuration File
```bash
# Use the config file
python fill_answers_advanced.py --config mcp-data/sources-config.json

# Verify output
Get-Content mcp-data/questions_filled.md | Select-Object -First 20
```

---

### MCP Server Testing

#### Test E: Test MCP HTTP Server
```bash
# List files via MCP
$response = Invoke-WebRequest -Uri "http://localhost:3333/" -UseBasicParsing
$response.Content | ConvertFrom-Json | Select-Object -ExpandProperty files

# Should show: questions.md, answers.md, test.txt, sources-config.json
```

**Expected Output:**
```
name size is_dir type
---- ---- ------ ----
answers.md 3380 False markdown
questions.md 1261 False markdown
test.txt 24 False text
sources-config.json 37 False json
```

#### Test F: Read File via MCP API
```bash
# Read questions.md
$response = Invoke-WebRequest -Uri "http://localhost:3333/files/questions.md" -UseBasicParsing
Write-Host "Questions file size: $($response.Content.Length) bytes"
Write-Host "First 200 chars:"
$response.Content.Substring(0, 200)
```

**Expected:** File contents with questions

---

### Docker Testing

#### Test G: Test MCP Server in Docker
```bash
# Verify container is running
docker ps | grep mcp-filesystem

# Check logs
docker logs mcp-filesystem | tail -20

# Test from inside container
docker exec mcp-filesystem curl http://localhost:3333/
```

**Expected:** JSON response with file list

---

## 🔍 Verification Checklist

### Simple Script Test
- [ ] `python fill_answers.py` runs without errors
- [ ] `questions_filled.md` is created
- [ ] File contains all 10 questions (Q1-Q10)
- [ ] No "<!-- TO BE FILLED -->" placeholders remain
- [ ] All answers contain ISO/IEC 27002 references
- [ ] Output shows "✅ Filled 10 questions"

### Advanced Script Test
- [ ] `python fill_answers_advanced.py --sources answers.md` works
- [ ] Output matches simple script
- [ ] Shows "Found 10 answers"
- [ ] Questions_filled.md created successfully

### MCP Server Test
- [ ] `curl http://localhost:3333/` returns JSON
- [ ] File listing shows all files
- [ ] `/files/questions.md` returns file content
- [ ] `/files/answers.md` returns file content
- [ ] No errors in docker logs

### Docker Integration
- [ ] All 5 services running (`docker compose ps`)
- [ ] No port conflicts (3000, 3333, 8000, 8501, 11434)
- [ ] OpenWebUI accessible at http://localhost:3000
- [ ] MCP at http://localhost:3333

---

## ⚠️ Troubleshooting Tests

### If Simple Script Fails
```bash
# Check Python is available
python --version

# Check files exist
Test-Path mcp-data/questions.md
Test-Path mcp-data/answers.md

# Try with full path
python "C:\Users\j.adelubi\Documents\AI Demo\ai-command-center-v2-ready\fill_answers.py"
```

### If MCP Server Doesn't Respond
```bash
# Check if server is running
docker ps | grep mcp-filesystem

# Restart server
docker compose restart mcp-filesystem

# Wait 10 seconds
Start-Sleep -Seconds 10

# Try again
curl http://localhost:3333/
```

### If Advanced Script Fails
```bash
# Check Python packages
pip list | grep -i "request\|beautiful\|pdf\|docx\|pil"

# Install missing
pip install -r requirements-advanced.txt
```

---

## 🎯 Test Scenarios by Source Type

### Scenario 1: Text Files (Works Now)
```bash
python fill_answers_advanced.py --sources answers.md
```
✅ Should work immediately

### Scenario 2: Screenshots (Requires OCR)
```bash
# First install OCR
pip install pytesseract pillow

# Install Tesseract (Windows)
# Download: https://github.com/UB-Mannheim/tesseract/wiki

# Then test with screenshot
python fill_answers_advanced.py --sources mcp-data/your-screenshot.png
```

### Scenario 3: PDF (Requires PyPDF2)
```bash
# Install PDF support
pip install PyPDF2

# Test with PDF
python fill_answers_advanced.py --sources mcp-data/answers.pdf
```

### Scenario 4: URLs (Requires requests)
```bash
# Install web support
pip install requests beautifulsoup4

# Test with URL
python fill_answers_advanced.py --sources "https://example.com/answers"
```

### Scenario 5: Word Docs (Requires python-docx)
```bash
# Install Word support
pip install python-docx

# Test with DOCX
python fill_answers_advanced.py --sources mcp-data/answers.docx
```

---

## 📊 Test Results Template

**Fill out after testing:**

```
Simple Script (fill_answers.py)
[ ] Runs without errors
[ ] Creates questions_filled.md
[ ] All 10 questions filled
[ ] No placeholders remain
Result: PASS / FAIL

Advanced Script (fill_answers_advanced.py)
[ ] Runs with markdown source
[ ] Output matches simple script
[ ] Configuration file works
Result: PASS / FAIL

MCP Server
[ ] Docker container running
[ ] HTTP endpoint accessible
[ ] Can list files
[ ] Can read files
Result: PASS / FAIL

Docker Integration
[ ] All services up (docker compose ps)
[ ] OpenWebUI accessible
[ ] No port conflicts
[ ] No errors in logs
Result: PASS / FAIL
```

---

## 🚀 Quick Test Commands (Copy-Paste)

### Test Everything Fast
```bash
# 1. Simple script
python fill_answers.py

# 2. Advanced script
python fill_answers_advanced.py --sources answers.md

# 3. MCP server
curl http://localhost:3333/

# 4. Check output
Get-Content mcp-data/questions_filled.md | Select-Object -First 30
```

Expected: All should complete without errors ✅

---

## 📚 Documentation for Testing

- **[MULTI_SOURCE_GUIDE.md](MULTI_SOURCE_GUIDE.md)** - Detailed usage
- **[QUICK_START_MULTI_SOURCE.md](QUICK_START_MULTI_SOURCE.md)** - Quick start
- **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** - Available solutions
- **[MCP_TROUBLESHOOTING.md](MCP_TROUBLESHOOTING.md)** - Common issues

---

## ✨ What "Working" Means

✅ **Working:**
- Script runs without Python errors
- Output file is created
- All 10 questions are filled
- No "TO BE FILLED" placeholders remain
- Answers match the sources

❌ **Not Working:**
- Script crashes with exception
- Output file not created
- Questions remain unfilled
- Placeholders still present
- Wrong answers or missing content

---

## 🎓 Next Steps After Testing

1. ✅ If simple script works → You're done! Use it.
2. ✅ If advanced script works → Explore multiple sources
3. ✅ If MCP works → Can integrate with OpenWebUI
4. ⚠️ If failures → Check troubleshooting section

Start with **Test 1** and work up! 🚀
