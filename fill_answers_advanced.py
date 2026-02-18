#!/usr/bin/env python3
"""
Advanced Answer Filler - Multi-source Support
Supports: Screenshots, URLs, PDFs, DOCX, and text files
Author: j.adelubi
"""

import re
import requests
import json
import os
from pathlib import Path
from typing import Dict, List, Union

# Optional imports
try:
    from PIL import Image
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

try:
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
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


class AnswerExtractor:
    """Extract answers from various sources"""
    
    def __init__(self, data_dir: str = "mcp-data"):
        self.data_dir = data_dir
        self.answers = {}
    
    def extract_from_file(self, file_path: str) -> str:
        """Extract text from file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_from_url(self, url: str) -> str:
        """Extract content from URL"""
        if not HAS_WEB:
            raise Exception("Install: pip install requests beautifulsoup4")
        
        print(f"  📡 Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove scripts and styles
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)
    
    def extract_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        if not HAS_OCR:
            raise Exception("Install: pip install pytesseract pillow")
        
        print(f"  🖼️  Processing image: {image_path}")
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    
    def extract_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        if not HAS_PDF:
            raise Exception("Install: pip install PyPDF2")
        
        print(f"  📄 Processing PDF: {pdf_path}")
        text = []
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"     Pages: {len(reader.pages)}")
            for i, page in enumerate(reader.pages, 1):
                print(f"     Reading page {i}...")
                text.append(page.extract_text())
        
        return '\n'.join(text)
    
    def extract_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX"""
        if not HAS_DOCX:
            raise Exception("Install: pip install python-docx")
        
        print(f"  📝 Processing DOCX: {docx_path}")
        doc = DocxDocument(docx_path)
        text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)
        
        return '\n'.join(text)
    
    def extract_from_source(self, source: Union[str, dict]) -> str:
        """Extract content from any source"""
        
        # Handle dict source specification
        if isinstance(source, dict):
            source_type = source.get('type')
            source_path = source.get('path')
        else:
            # Auto-detect type
            source_path = source
            if source_path.startswith(('http://', 'https://')):
                source_type = 'url'
            else:
                ext = Path(source_path).suffix.lower()
                type_map = {
                    '.pdf': 'pdf',
                    '.docx': 'docx',
                    '.png': 'image',
                    '.jpg': 'image',
                    '.jpeg': 'image',
                    '.gif': 'image',
                    '.bmp': 'image'
                }
                source_type = type_map.get(ext, 'file')
        
        # Extract based on type
        if source_type == 'url':
            content = self.extract_from_url(source_path)
        elif source_type == 'image':
            full_path = os.path.join(self.data_dir, source_path)
            content = self.extract_from_image(full_path)
        elif source_type == 'pdf':
            full_path = os.path.join(self.data_dir, source_path)
            content = self.extract_from_pdf(full_path)
        elif source_type == 'docx':
            full_path = os.path.join(self.data_dir, source_path)
            content = self.extract_from_docx(full_path)
        else:  # file
            full_path = os.path.join(self.data_dir, source_path)
            content = self.extract_from_file(full_path)
        
        return content
    
    def parse_answers(self, content: str) -> Dict[str, str]:
        """Parse answers from content"""
        answers = {}
        
        # Split by section separators
        sections = content.split('---')
        
        for section in sections:
            section = section.strip()
            if not section or '# Secure Coding' in section:
                continue
            
            # Look for answer pattern (A1, A2, etc.)
            match = re.search(r'## (A\d+)\..+', section)
            if match:
                answer_num = match.group(1)
                
                # Extract answer text after the header
                lines = section.split('\n')
                answer_lines = []
                for i, line in enumerate(lines):
                    if line.startswith('##'):
                        answer_lines = lines[i+1:]
                        break
                
                answer_text = '\n'.join(answer_lines).strip()
                question_num = 'Q' + answer_num[1:]
                answers[question_num] = answer_text
        
        return answers
    
    def load_answers_from_sources(self, sources: List[Union[str, dict]]) -> Dict[str, str]:
        """Load answers from multiple sources"""
        all_answers = {}
        
        print(f"\n🔍 Extracting answers from {len(sources)} source(s)...")
        
        for i, source in enumerate(sources, 1):
            print(f"\n  Source {i}/{len(sources)}:")
            try:
                content = self.extract_from_source(source)
                answers = self.parse_answers(content)
                
                print(f"  ✅ Found {len(answers)} answers")
                all_answers.update(answers)
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue
        
        return all_answers
    
    def fill_questions(self, questions_file: str, answers: Dict[str, str], output_file: str):
        """Fill questions with answers"""
        with open(questions_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = content.split('---')
        filled_sections = []
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            match = re.search(r'## (Q\d+)\.', section)
            if match and '<!-- TO BE FILLED -->' in section:
                question_num = match.group(1)
                if question_num in answers:
                    filled_section = section.replace('<!-- TO BE FILLED -->', answers[question_num])
                    filled_sections.append(filled_section)
                else:
                    filled_sections.append(section)
            else:
                filled_sections.append(section)
        
        filled_content = '\n\n---\n\n'.join(filled_sections)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(filled_content)
        
        return len(answers)


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fill questions from various answer sources')
    parser.add_argument('--questions', default='mcp-data/questions.md', help='Questions file')
    parser.add_argument('--output', default='mcp-data/questions_filled.md', help='Output file')
    parser.add_argument('--sources', nargs='+', help='Answer sources (files, URLs, etc.)')
    parser.add_argument('--config', help='JSON config file with sources')
    
    args = parser.parse_args()
    
    print("🚀 Advanced Answer Filler")
    print("=" * 50)
    
    # Determine sources
    if args.config:
        print(f"📋 Loading config: {args.config}")
        with open(args.config, 'r') as f:
            config = json.load(f)
        sources = config.get('sources', [])
    elif args.sources:
        sources = args.sources
    else:
        # Default: use answers.md
        sources = ['answers.md']
    
    print(f"📁 Questions: {args.questions}")
    print(f"📁 Output: {args.output}")
    
    # Extract and fill
    extractor = AnswerExtractor()
    answers = extractor.load_answers_from_sources(sources)
    
    print(f"\n✅ Total answers extracted: {len(answers)}")
    
    if answers:
        count = extractor.fill_questions(args.questions, answers, args.output)
        print(f"✅ Filled {count} questions successfully")
        print(f"\n📄 Output saved to: {args.output}")
        print("\n✨ Done!")
    else:
        print("\n❌ No answers found in sources")


if __name__ == '__main__':
    main()
