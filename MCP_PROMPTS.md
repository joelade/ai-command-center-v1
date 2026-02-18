# OpenWebUI Prompt Templates for MCP Answer Filling

## Template 1: Simple Answer Filling Prompt

```
Use the MCP filesystem server to read files from mcp-data/ directory.

Task: Fill in answers from answers.md into the corresponding questions in questions.md

Steps:
1. Read the file: mcp-data/questions.md (contains Q1-Q10 with <!-- TO BE FILLED --> placeholders)
2. Read the file: mcp-data/answers.md (contains A1-A10 with detailed answers)
3. For each question Q1-Q10, find the matching answer A1-A10
4. Replace each <!-- TO BE FILLED --> placeholder with the appropriate answer
5. Return the complete filled document

Ensure accuracy and maintain the ISO/IEC 27002:2022 context throughout.
```

## Template 2: Detailed Answer Filling with Validation

```
You are an ISO/IEC 27002:2022 subject matter expert. Use MCP to complete this task:

MCP Filesystem Access:
- Read mcp-data/questions.md for secure coding questions
- Read mcp-data/answers.md for referenced answers

Your Task:
1. Parse both documents
2. Map each question (Q1-Q10) to its answer (A1-A10)
3. Fill in the <!-- TO BE FILLED --> placeholders with accurate answers
4. Verify each answer matches the corresponding control reference
5. Format the output as a clean, professional document

Quality Checks:
- All 10 answers must be included
- Each answer should directly address the question
- Maintain ISO/IEC 27002:2022 standards
- Preserve all control references [ISO/IEC 27002:2022 – Controls: X.X]

Deliver the completed questions.md file with all answers properly inserted.
```

## Template 3: Interactive Answer Filling with Explanations

```
I need your help filling in answers using the MCP filesystem.

Context:
- Questions file: mcp-data/questions.md
- Answers file: mcp-data/answers.md
- Standard: ISO/IEC 27002:2022

Please:
1. Read both files using MCP
2. For each question, provide:
   - The question number (Q1-Q10)
   - The corresponding answer
   - Key points from the ISO/IEC 27002:2022 reference
   - Practical application example

3. Generate a filled version of questions.md with:
   - Each placeholder replaced with the full answer
   - Related control references preserved
   - Professional formatting maintained

4. Provide a summary showing:
   - Total questions processed
   - All answers filled successfully
   - Validation against ISO/IEC 27002:2022 standards
```

## Template 4: Batch Processing with Export

```
Execute MCP-based answer filling workflow:

Input:
- Source: mcp-data/questions.md
- Reference: mcp-data/answers.md

Processing:
1. Load both documents via MCP filesystem
2. Identify all "<!-- TO BE FILLED -->" sections
3. Extract matching answer from answers.md
4. Validate answer relevance to question
5. Insert answer maintaining markdown structure

Output Format:
- Filled questions.md with all answers embedded
- Validation report (questions answered: X/10)
- Control references summary
- Ready-to-use markdown document

Start processing now.
```

## How to Use These Templates

### In OpenWebUI:

1. **Open New Chat**: Click "+" for a new conversation
2. **Select Model**: Choose your preferred model (e.g., llama3, mistral)
3. **Paste Template**: Copy one of the templates above into the chat
4. **Submit**: Press Enter or click Send
5. **Review Output**: The model will use MCP to read files and generate the filled answers.md

### Pro Tips:

- **For Quick Results**: Use Template 1 (Simple)
- **For Accuracy**: Use Template 2 (Detailed with Validation)
- **For Understanding**: Use Template 3 (Interactive)
- **For Production**: Use Template 4 (Batch Processing)

### Customization:

Feel free to modify templates based on:
- Specific questions you want to focus on
- Different standards or compliance requirements
- Additional validation criteria
- Custom output formats

## MCP Access in Your Environment

The MCP server is running at: `http://mcp-filesystem:3333`

Available endpoints:
- `GET /` - List mcp-data files
- `GET /files/questions.md` - Read questions
- `GET /files/answers.md` - Read answers

You can also test MCP access directly:
```bash
# From your machine
curl http://localhost:3333/files/questions.md
curl http://localhost:3333/files/answers.md

# From inside docker network
curl http://mcp-filesystem:3333/files/questions.md
```

## Verification Checklist

Before using MCP in OpenWebUI:

- [ ] Docker services running: `docker ps`
- [ ] MCP server active: `docker ps | grep mcp-filesystem`
- [ ] OpenWebUI accessible: http://localhost:3000
- [ ] MCP files present: Check `mcp-data/` directory
- [ ] Network connectivity: `docker exec open-webui curl http://mcp-filesystem:3333/`

Enjoy using MCP for accurate answer filling!
