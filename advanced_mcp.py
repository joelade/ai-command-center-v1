#!/usr/bin/env python3
"""
Advanced MCP Server - Multi-format Answer Extraction
Author: j.adelubi
Supports: Screenshots, URLs, PDFs, DOCX, Images, and more
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import uvicorn
import base64
from pathlib import Path

# Optional imports - install as needed
try:
    from PIL import Image
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_WEB = True
except ImportError:
    HAS_WEB = False

try:
    import PyPDF2
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


class AnswerSource(BaseModel):
    type: str  # 'file', 'url', 'image', 'pdf', 'docx'
    source: str  # file path or URL
    query: Optional[str] = None  # optional query for extraction


def create_app(root: str = "/app/data"):
    app = FastAPI(title="Advanced MCP Filesystem")

    # Ensure data directory exists
    os.makedirs(root, exist_ok=True)

    # Serve files under /static
    app.mount("/static", StaticFiles(directory=root), name="static")

    @app.get("/")
    def list_files():
        """List all files with type detection"""
        items = []
        for entry in sorted(os.listdir(root)):
            path = os.path.join(root, entry)
            file_type = detect_file_type(entry)
            items.append({
                "name": entry,
                "is_dir": os.path.isdir(path),
                "type": file_type,
                "size": os.path.getsize(path) if os.path.isfile(path) else None,
                "supported": is_supported_format(file_type)
            })
        return {
            "root": root,
            "files": items,
            "capabilities": get_capabilities()
        }

    @app.get("/files/{path:path}")
    def get_file(path: str):
        """Get file - detect type and serve appropriately"""
        file_path = os.path.join(root, path)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Not found")
        if os.path.isdir(file_path):
            raise HTTPException(status_code=400, detail="Requested path is a directory")
        return FileResponse(file_path)

    @app.post("/extract")
    async def extract_content(source: AnswerSource):
        """Extract content from various sources"""
        try:
            if source.type == "url":
                content = extract_from_url(source.source)
            elif source.type == "image":
                content = extract_from_image(os.path.join(root, source.source))
            elif source.type == "pdf":
                content = extract_from_pdf(os.path.join(root, source.source))
            elif source.type == "docx":
                content = extract_from_docx(os.path.join(root, source.source))
            elif source.type == "file":
                content = extract_from_file(os.path.join(root, source.source))
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported type: {source.type}")
            
            return {
                "source": source.source,
                "type": source.type,
                "content": content,
                "status": "success"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/extract-answers")
    async def extract_answers(sources: List[AnswerSource]):
        """Extract answers from multiple sources"""
        results = []
        for source in sources:
            try:
                if source.type == "url":
                    content = extract_from_url(source.source)
                elif source.type == "image":
                    content = extract_from_image(os.path.join(root, source.source))
                elif source.type == "pdf":
                    content = extract_from_pdf(os.path.join(root, source.source))
                elif source.type == "docx":
                    content = extract_from_docx(os.path.join(root, source.source))
                else:
                    content = extract_from_file(os.path.join(root, source.source))
                
                # Extract answers from content
                answers = parse_answers_from_content(content)
                results.append({
                    "source": source.source,
                    "type": source.type,
                    "answers": answers,
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "source": source.source,
                    "type": source.type,
                    "error": str(e),
                    "status": "failed"
                })
        
        return {"results": results}

    @app.get("/capabilities")
    def get_capabilities():
        """Return supported capabilities"""
        return {
            "ocr": HAS_OCR,
            "web_scraping": HAS_WEB,
            "pdf": HAS_PDF,
            "docx": HAS_DOCX,
            "supported_formats": {
                "images": ["jpg", "jpeg", "png", "gif", "bmp"] if HAS_OCR else [],
                "documents": ["pdf"] if HAS_PDF else [] + ["docx"] if HAS_DOCX else [],
                "text": ["md", "txt", "json", "csv"],
                "web": ["http", "https"] if HAS_WEB else []
            }
        }

    return app


def detect_file_type(filename: str) -> str:
    """Detect file type from extension"""
    ext = Path(filename).suffix.lower()
    type_map = {
        '.md': 'markdown',
        '.txt': 'text',
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.doc': 'doc',
        '.jpg': 'image',
        '.jpeg': 'image',
        '.png': 'image',
        '.gif': 'image',
        '.bmp': 'image',
        '.json': 'json',
        '.csv': 'csv',
        '.html': 'html',
        '.htm': 'html'
    }
    return type_map.get(ext, 'unknown')


def is_supported_format(file_type: str) -> bool:
    """Check if format is supported"""
    supported = ['markdown', 'text', 'json', 'csv']
    if HAS_PDF and file_type == 'pdf':
        supported.append('pdf')
    if HAS_DOCX and file_type == 'docx':
        supported.append('docx')
    if HAS_OCR and file_type == 'image':
        supported.append('image')
    return file_type in supported


def extract_from_file(file_path: str) -> str:
    """Extract content from text-based files"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_from_url(url: str) -> str:
    """Extract content from web URL"""
    if not HAS_WEB:
        raise Exception("Web scraping not available. Install: pip install requests beautifulsoup4")
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Clean up text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text


def extract_from_image(image_path: str) -> str:
    """Extract text from image using OCR"""
    if not HAS_OCR:
        raise Exception("OCR not available. Install: pip install pytesseract pillow")
    
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def extract_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF"""
    if not HAS_PDF:
        raise Exception("PDF support not available. Install: pip install PyPDF2")
    
    text = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text.append(page.extract_text())
    
    return '\n'.join(text)


def extract_from_docx(docx_path: str) -> str:
    """Extract text from DOCX"""
    if not HAS_DOCX:
        raise Exception("DOCX support not available. Install: pip install python-docx")
    
    doc = Document(docx_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    
    return '\n'.join(text)


def parse_answers_from_content(content: str) -> Dict[str, str]:
    """Parse answers from extracted content"""
    import re
    
    answers = {}
    
    # Try to find answer patterns (A1, A2, etc.)
    pattern = r'## (A\d+)\..+?(?=## A\d+|$)'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        section = match.group(0)
        answer_num = re.search(r'## (A\d+)\.', section).group(1)
        
        # Extract text after the header
        lines = section.split('\n')
        answer_text = '\n'.join(lines[1:]).strip()
        
        # Map to question number
        question_num = 'Q' + answer_num[1:]
        answers[question_num] = answer_text
    
    return answers


app = create_app(root="/app/data")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3333)
