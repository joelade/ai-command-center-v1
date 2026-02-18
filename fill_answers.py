#!/usr/bin/env python3
"""
Fill answers from answers.md into questions.md
Author: j.adelubi
"""

import re

def extract_answers(answers_file):
    """Extract all answers from answers.md"""
    with open(answers_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    answers = {}
    # Split by --- separators
    sections = content.split('---')
    
    for section in sections:
        section = section.strip()
        if not section or '# Secure Coding' in section:
            continue
        
        # Extract answer number (A1, A2, etc.) - matches "## A1. Title"
        match = re.search(r'## (A\d+)\..+', section)
        if match:
            answer_num = match.group(1)
            # Extract the answer text (everything after the first line with ##)
            lines = section.split('\n')
            # Find the content starting from line after the header
            answer_lines = []
            for i, line in enumerate(lines):
                if line.startswith('##'):
                    # Get all lines after this header
                    answer_lines = lines[i+1:]
                    break
            
            answer_text = '\n'.join(answer_lines).strip()
            # Convert A1 -> Q1, A2 -> Q2, etc.
            question_num = 'Q' + answer_num[1:]
            answers[question_num] = answer_text
    
    return answers

def fill_questions(questions_file, answers, output_file):
    """Fill questions with answers"""
    with open(questions_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by questions
    sections = content.split('---')
    filled_sections = []
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Check if this section has a question
        match = re.search(r'## (Q\d+)\.', section)
        if match and '<!-- TO BE FILLED -->' in section:
            question_num = match.group(1)
            if question_num in answers:
                # Replace placeholder with answer
                filled_section = section.replace('<!-- TO BE FILLED -->', answers[question_num])
                filled_sections.append(filled_section)
            else:
                filled_sections.append(section)
        else:
            filled_sections.append(section)
    
    # Reconstruct the document with proper spacing
    filled_content = '\n\n---\n\n'.join(filled_sections)
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(filled_content)
    
    return len(answers)

if __name__ == '__main__':
    import os
    
    # File paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    questions_file = os.path.join(script_dir, 'mcp-data', 'questions.md')
    answers_file = os.path.join(script_dir, 'mcp-data', 'answers.md')
    output_file = os.path.join(script_dir, 'mcp-data', 'questions_filled.md')
    
    print("🔍 Reading files...")
    print(f"   Questions: {questions_file}")
    print(f"   Answers:   {answers_file}")
    
    # Extract answers
    answers = extract_answers(answers_file)
    print(f"\n✅ Found {len(answers)} answers")
    
    # Fill questions
    count = fill_questions(questions_file, answers, output_file)
    
    print(f"✅ Filled {count} questions successfully")
    print(f"\n📄 Output saved to: {output_file}")
    print("\n✨ Done!")
