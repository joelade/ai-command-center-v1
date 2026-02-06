# Multi-Source MCP Answer Extraction Guide

## 🎯 Overview

This advanced MCP system can extract answers from **multiple sources**:
- 📄 **Text Files** (MD, TXT, JSON, CSV)
- 🖼️ **Screenshots/Images** (PNG, JPG, GIF) - with OCR
- 🌐 **Web URLs** (HTTP/HTTPS)
- 📕 **PDF Documents**
- 📘 **Word Documents** (DOCX)

---

## 🚀 Quick Start

### Option 1: Using Markdown File (Already Working)
```bash
python fill_answers_advanced.py
```
Uses `mcp-data/answers.md` by default ✅

### Option 2: Using Multiple Sources
```bash
python fill_answers_advanced.py --sources mcp-data/answers.md mcp-data/answers.pdf https://example.com/answers
```

### Option 3: Using Configuration File
```bash
python fill_answers_advanced.py --config mcp-data/sources-config.json
```

---

## 📦 Installation

### Step 1: Install Dependencies
```bash
# Install all advanced features
pip install -r requirements-advanced.txt
```

**Or install selectively:**
```bash
# For web scraping
pip install requests beautifulsoup4

# For image/screenshot OCR
pip install pytesseract pillow

# For PDF support
pip install PyPDF2

# For Word documents
pip install python-docx
```

### Step 2: Install Tesseract (for OCR)
**Windows:**
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install to: C:\Program Files\Tesseract-OCR
# Add to PATH
```

**Linux/Mac:**
```bash
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
brew install tesseract              # macOS
```

---

## 📋 Usage Examples

### Example 1: Extract from Markdown File
```bash
python fill_answers_advanced.py --sources mcp-data/answers.md
```

**Input:** `answers.md` with 10 answers  
**Output:** `questions_filled.md` with all placeholders filled

---

### Example 2: Extract from Screenshot (OCR)

**Step 1:** Take a screenshot of answers and save it
```
mcp-data/
  ├── questions.md
  └── answers-screenshot.png  ← Your screenshot
```

**Step 2:** Run extraction
```bash
python fill_answers_advanced.py --sources mcp-data/answers-screenshot.png
```

**What Happens:**
- Script reads the image
- Uses OCR (Tesseract) to extract text
- Parses answers (A1-A10)
- Fills questions.md

---

### Example 3: Extract from PDF Document

**Step 1:** Place PDF in mcp-data/
```
mcp-data/
  ├── questions.md
  └── iso27002-answers.pdf  ← Your PDF
```

**Step 2:** Extract
```bash
python fill_answers_advanced.py --sources mcp-data/iso27002-answers.pdf
```

**Supports:**
- Multi-page PDFs
- Text-based PDFs (not scanned images)
- Formatted documents

---

### Example 4: Extract from Web URL

**Direct from webpage:**
```bash
python fill_answers_advanced.py --sources "https://example.com/iso27002-secure-coding-answers"
```

**What Happens:**
- Fetches webpage content
- Extracts text (removes scripts, styles, navigation)
- Parses answers
- Fills questions

---

### Example 5: Extract from Word Document (DOCX)

```bash
python fill_answers_advanced.py --sources mcp-data/answers.docx
```

**Supports:**
- DOCX format (not legacy DOC)
- Formatted text
- Multi-section documents

---

### Example 6: Combine Multiple Sources

**Use Case:** Answers spread across different files

```bash
python fill_answers_advanced.py \
  --sources \
    mcp-data/answers-part1.md \
    mcp-data/answers-part2.pdf \
    mcp-data/screenshot-q5-q7.png \
    "https://example.com/remaining-answers"
```

**What Happens:**
- Extracts from all sources
- Combines answers
- Fills all 10 questions from different sources

---

## ⚙️ Configuration File Method

### Create `sources-config.json`
```json
{
  "sources": [
    {
      "type": "file",
      "path": "answers.md"
    },
    {
      "type": "pdf",
      "path": "iso-guidelines.pdf"
    },
    {
      "type": "url",
      "path": "https://cybersecurity.example.com/27002-answers"
    },
    {
      "type": "image",
      "path": "screenshot-answers.png"
    }
  ],
  "questions": "questions.md",
  "output": "questions_filled.md"
}
```

### Run with Config
```bash
python fill_answers_advanced.py --config mcp-data/sources-config.json
```

---

## 🔧 Advanced Features

### Feature 1: OCR from Multiple Screenshots

```bash
python fill_answers_advanced.py \
  --sources \
    mcp-data/screenshot1.png \
    mcp-data/screenshot2.png \
    mcp-data/screenshot3.png
```

**Best Practices for Screenshots:**
- ✅ High resolution (readable text)
- ✅ Good contrast (dark text on light background)
- ✅ Clear, non-blurry images
- ✅ Horizontal text (OCR works best)
- ❌ Avoid handwritten text
- ❌ Avoid overly compressed images

---

### Feature 2: Web Scraping with Filters

Extract from specific webpage sections:

```bash
# The script automatically filters out navigation, headers, footers
python fill_answers_advanced.py --sources "https://docs.example.com/security"
```

**Supported:**
- Clean HTML extraction
- Auto-removal of navigation/ads
- Text normalization
- Multi-paragraph content

---

### Feature 3: PDF with Multiple Pages

```bash
python fill_answers_advanced.py --sources mcp-data/multi-page-answers.pdf
```

**Output shows:**
```
  📄 Processing PDF: mcp-data/multi-page-answers.pdf
     Pages: 15
     Reading page 1...
     Reading page 2...
     ...
  ✅ Found 10 answers
```

---

## 🧪 Testing Your Setup

### Test 1: Verify OCR Installation
```python
# test_ocr.py
from PIL import Image
import pytesseract

img = Image.new('RGB', (200, 100), color='white')
# Add text to image in a real test
text = pytesseract.image_to_string(img)
print(f"OCR Working: {len(text) >= 0}")
```

### Test 2: Verify PDF Support
```python
# test_pdf.py
import PyPDF2

print("PDF support: Available" if PyPDF2 else "Not installed")
```

### Test 3: Verify Web Scraping
```python
# test_web.py
import requests
from bs4 import BeautifulSoup

response = requests.get("https://example.com")
print(f"Web scraping: {response.status_code == 200}")
```

---

## 📊 Supported File Formats

| Format | Extension | Capability | Installation |
|--------|-----------|------------|--------------|
| **Markdown** | .md | ✅ Native | Built-in |
| **Text** | .txt | ✅ Native | Built-in |
| **JSON** | .json | ✅ Native | Built-in |
| **CSV** | .csv | ✅ Native | Built-in |
| **PDF** | .pdf | ✅ With PyPDF2 | `pip install PyPDF2` |
| **Word** | .docx | ✅ With python-docx | `pip install python-docx` |
| **Images** | .png, .jpg, .gif | ✅ With OCR | `pip install pytesseract pillow` |
| **Web** | http://, https:// | ✅ With requests | `pip install requests beautifulsoup4` |

---

## 🔍 How Answer Detection Works

### Pattern Recognition

The script looks for answers in this format:

```markdown
## A1. Purpose of Secure Coding
Answer text here...
[ISO/IEC 27002:2022 – Controls: 8.28]

---

## A2. Input Validation
Answer text here...
```

**What It Detects:**
- Answer headers: `## A1.`, `## A2.`, ... `## A10.`
- Section separators: `---`
- Answer content: Text between header and next separator
- Control references: `[ISO/IEC 27002:2022 – Controls: X.X]`

**Works Across All Formats:**
- Markdown files preserve formatting
- PDFs extract text as-is
- OCR converts images to text
- Web pages extract clean text
- DOCX preserves paragraphs

---

## 🚀 Real-World Examples

### Example 1: Security Training Materials

**Scenario:** Answers from training PDF

```bash
# Place training.pdf in mcp-data/
python fill_answers_advanced.py --sources mcp-data/security-training.pdf
```

### Example 2: Compliance Documentation

**Scenario:** Answers from compliance website

```bash
python fill_answers_advanced.py \
  --sources "https://compliance.example.com/iso27002"
```

### Example 3: Meeting Screenshots

**Scenario:** Whiteboard photos from security review

```bash
python fill_answers_advanced.py \
  --sources \
    mcp-data/whiteboard-1.jpg \
    mcp-data/whiteboard-2.jpg
```

### Example 4: Mixed Sources

**Scenario:** Answers from various documents

```bash
python fill_answers_advanced.py \
  --sources \
    mcp-data/official-guidelines.pdf \
    mcp-data/team-notes.docx \
    "https://security-wiki.company.com/27002" \
    mcp-data/expert-screenshot.png
```

---

## 🛠️ Troubleshooting

### Issue 1: OCR Not Working

**Error:** `pytesseract.TesseractNotFoundError`

**Solution:**
```bash
# Windows: Install Tesseract
# Download from: https://github.com/UB-Mannheim/tesseract/wiki

# Add to PATH or set explicitly:
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Issue 2: PDF Text Not Extracting

**Problem:** Scanned PDF (image-based)

**Solution:** Convert to image + OCR
```python
# Use pdf2image + OCR instead of PyPDF2
pip install pdf2image
```

### Issue 3: Web URL Blocked

**Error:** 403 Forbidden or timeout

**Solution:** Add headers
```python
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
```

### Issue 4: DOCX Format Error

**Error:** Can't open DOCX

**Solution:** Ensure it's DOCX not DOC
```bash
# Convert DOC to DOCX using Word or online converter
```

---

## 📈 Performance Tips

### Tip 1: Optimize Images for OCR
- Use PNG for screenshots (better quality)
- Crop to relevant sections
- Increase contrast before processing

### Tip 2: Pre-process PDFs
- Extract text-heavy pages only
- Combine multiple PDFs if needed

### Tip 3: Cache Web Content
- Download webpage once, process locally
- Saves time on repeated runs

### Tip 4: Parallel Processing (Advanced)
```python
# Process multiple sources concurrently
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    results = executor.map(extract_from_source, sources)
```

---

## ✅ Quick Checklist

Before running advanced extraction:

- [ ] Install required dependencies
- [ ] Test OCR with sample image (if using screenshots)
- [ ] Verify Tesseract installation (if using OCR)
- [ ] Test PDF reading (if using PDFs)
- [ ] Check internet connection (if using URLs)
- [ ] Prepare source files in mcp-data/
- [ ] Configure sources in config file (optional)
- [ ] Run extraction command
- [ ] Verify output in questions_filled.md

---

## 🎓 Next Steps

1. **Install dependencies** for formats you need
2. **Prepare your answer sources** (PDFs, screenshots, URLs)
3. **Place files** in `mcp-data/` directory
4. **Run extraction** with appropriate sources
5. **Verify results** in `questions_filled.md`

---

## 📁 Example Directory Structure

```
ai-command-center-v2-ready/
├── mcp-data/
│   ├── questions.md                 ← Input questions
│   ├── answers.md                   ← Text answers
│   ├── answers.pdf                  ← PDF answers
│   ├── answers.docx                 ← Word answers
│   ├── screenshot1.png              ← Image answers (OCR)
│   ├── screenshot2.jpg              ← Image answers (OCR)
│   ├── sources-config.json          ← Configuration
│   └── questions_filled.md          ← Output
├── fill_answers_advanced.py         ← Advanced script
├── requirements-advanced.txt        ← Dependencies
└── docker-compose.yml
```

---

## 🎯 Summary

**You can now extract answers from:**
- ✅ Markdown/text files
- ✅ Screenshots (OCR)
- ✅ PDF documents
- ✅ Word documents
- ✅ Web URLs
- ✅ Multiple sources combined

**Your answers can come from anywhere!** 🚀

For simpler use cases, stick with the original `fill_answers.py`.  
For advanced multi-source extraction, use `fill_answers_advanced.py`.
