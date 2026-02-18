# Quick Start: Multi-Source Answer Extraction

## 🎯 What This Does

Extract answers from **any source** to fill your questions:
- 📄 Text files (MD, TXT)
- 🖼️ Screenshots (with OCR)
- 🌐 Websites
- 📕 PDFs
- 📘 Word docs

---

## ⚡ Quick Examples

### Example 1: From Markdown (Already Works)
```bash
python fill_answers_advanced.py
```
✅ Uses `mcp-data/answers.md` by default

---

### Example 2: From Screenshot
```bash
# Take a screenshot of your answers, save as screenshot.png
python fill_answers_advanced.py --sources mcp-data/screenshot.png
```
✅ Uses OCR to read text from image

---

### Example 3: From PDF
```bash
python fill_answers_advanced.py --sources mcp-data/answers.pdf
```
✅ Extracts text from all pages

---

### Example 4: From Website
```bash
python fill_answers_advanced.py --sources "https://example.com/answers"
```
✅ Scrapes and extracts text

---

### Example 5: Multiple Sources
```bash
python fill_answers_advanced.py \
  --sources \
    mcp-data/answers.md \
    mcp-data/extra-answers.pdf \
    mcp-data/screenshot.png
```
✅ Combines all sources

---

## 📦 Installation (One Time)

### Basic (Markdown only - already working)
```bash
# Nothing needed - already works!
```

### Advanced (All formats)
```bash
# Install all dependencies
pip install -r requirements-advanced.txt

# For Windows OCR: Download Tesseract
# https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH after installation
```

**Or install selectively:**
```bash
pip install requests beautifulsoup4     # For web URLs
pip install pytesseract pillow          # For screenshots/images
pip install PyPDF2                      # For PDFs
pip install python-docx                 # For Word docs
```

---

## 📋 Common Scenarios

### Scenario 1: Answers in Training PDF
```bash
# Place security-training.pdf in mcp-data/
python fill_answers_advanced.py --sources mcp-data/security-training.pdf
```

### Scenario 2: Whiteboard Photos After Meeting
```bash
# Take photos, save as .jpg
python fill_answers_advanced.py \
  --sources \
    mcp-data/whiteboard-1.jpg \
    mcp-data/whiteboard-2.jpg
```

### Scenario 3: Compliance Website
```bash
python fill_answers_advanced.py \
  --sources "https://compliance.yourcompany.com/iso27002"
```

### Scenario 4: Team's Shared Word Doc
```bash
python fill_answers_advanced.py --sources mcp-data/team-answers.docx
```

---

## 🔍 How to Check What Works

```bash
# Check installed capabilities
python -c "
import sys
print('✅ PDF support') if 'PyPDF2' in sys.modules or __import__('importlib').util.find_spec('PyPDF2') else print('❌ PDF support')
print('✅ DOCX support') if __import__('importlib').util.find_spec('docx') else print('❌ DOCX support')
print('✅ OCR support') if __import__('importlib').util.find_spec('pytesseract') else print('❌ OCR support')
print('✅ Web scraping') if __import__('importlib').util.find_spec('requests') else print('❌ Web scraping')
"
```

---

## 🎯 Expected Output

```
🚀 Advanced Answer Filler
==================================================
📁 Questions: mcp-data/questions.md
📁 Output: mcp-data/questions_filled.md

🔍 Extracting answers from 1 source(s)...

  Source 1/1:
  📄 Processing PDF: mcp-data/answers.pdf
     Pages: 5
     Reading page 1...
     Reading page 2...
     Reading page 3...
     Reading page 4...
     Reading page 5...
  ✅ Found 10 answers

✅ Total answers extracted: 10
✅ Filled 10 questions successfully

📄 Output saved to: mcp-data/questions_filled.md

✨ Done!
```

---

## 📁 File Structure

```
mcp-data/
├── questions.md              ← Questions with placeholders
├── answers.md                ← Option 1: Text file
├── answers.pdf               ← Option 2: PDF
├── screenshot.png            ← Option 3: Screenshot
└── questions_filled.md       ← Output (created automatically)
```

---

## 🛠️ Troubleshooting

### "OCR not available"
```bash
# Install OCR support
pip install pytesseract pillow

# Windows: Install Tesseract executable
# Download: https://github.com/UB-Mannheim/tesseract/wiki
```

### "PDF support not available"
```bash
pip install PyPDF2
```

### "Web scraping not available"
```bash
pip install requests beautifulsoup4
```

### "DOCX support not available"
```bash
pip install python-docx
```

---

## 📚 Documentation

- **[MULTI_SOURCE_GUIDE.md](MULTI_SOURCE_GUIDE.md)** - Complete guide with all examples
- **[requirements-advanced.txt](requirements-advanced.txt)** - All dependencies
- **[sources-config.json](mcp-data/sources-config.json)** - Configuration example

---

## ✅ Comparison

| Feature | Original Script | Advanced Script |
|---------|----------------|-----------------|
| Markdown files | ✅ | ✅ |
| Screenshots (OCR) | ❌ | ✅ |
| PDFs | ❌ | ✅ |
| Word docs | ❌ | ✅ |
| Web URLs | ❌ | ✅ |
| Multiple sources | ❌ | ✅ |

---

## 🚀 Get Started

**For simple use (already working):**
```bash
python fill_answers.py
```

**For advanced multi-source:**
```bash
# 1. Install dependencies
pip install -r requirements-advanced.txt

# 2. Run with your sources
python fill_answers_advanced.py --sources YOUR_FILE_OR_URL

# 3. Check output
cat mcp-data/questions_filled.md
```

**Done!** 🎉

---

For complete examples and details, see **MULTI_SOURCE_GUIDE.md**
