# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive LangChain educational website (gemini-langchain-test) using a hybrid architecture:
- **VitePress**: Static documentation site deployed to GitHub Pages
- **Streamlit**: Interactive demos for hands-on learning

## Project Structure

```
/
├── docs/                         # VitePress documentation site
│   ├── index.md                 # Homepage
│   ├── mermaid-test.md          # Mermaid diagram testing
│   ├── README.md                # Documentation overview
│   ├── tutorials/               # Tutorial documentation
│   │   ├── index.md             # Tutorial index
│   │   ├── setup.md             # Environment setup
│   │   ├── introduction.md      # LangChain introduction
│   │   ├── first-app.md         # First application
│   │   ├── chat-models.md       # Chat models
│   │   ├── prompt-template.md   # Prompt templates
│   │   ├── output-parsers.md    # Output parsers
│   │   ├── lcel.md             # LangChain Expression Language
│   │   ├── memory.md           # Memory systems
│   │   ├── rag.md              # RAG applications
│   │   ├── model-integration.md # Model integration
│   │   ├── free-llm-models.md  # Free LLM models
│   │   ├── multiple-llm-generations.md # Multiple generations
│   │   ├── streaming-chat-models.md # Streaming
│   │   ├── memory-systems.md   # Advanced memory
│   │   ├── langgraph.md        # LangGraph
│   │   ├── monitoring.md       # Monitoring
│   │   ├── architecture.md     # Architecture patterns
│   │   └── advanced-examples.md # Advanced examples
│   ├── examples/                # Example documentation
│   │   ├── index.md             # Examples index
│   │   ├── chatbot.md          # Chatbot example
│   │   ├── document-qa.md      # Document Q&A
│   │   └── tools.md            # Tool usage
│   └── demos/                   # Demo documentation
│       ├── index.md             # Demo index
│       ├── how-to-run.md       # How to run demos
│       ├── gemini-chat.md      # Gemini chat demo
│       └── free-models.md      # Free models demo
├── examples/                    # Example files and resources
│   └── README.md               # Examples overview
├── tutorials/                   # Tutorial resources
│   └── README.md               # Tutorials overview
├── streamlit-demos/             # Interactive Streamlit applications
│   ├── README.md               # Demo overview
│   ├── 02_free_models/         # Free LLM models demo
│   │   ├── free_models_demo.py # Main demo application
│   │   ├── requirements.txt    # Demo-specific dependencies
│   │   └── README.md           # Demo documentation
│   └── demos/                  # Legacy demo structure
│       └── 01_gemini_basic/    # Gemini API integration demo
│           ├── gemini_chat.py  # Chat application
│           └── README.md       # Demo documentation
├── app.py                      # Local demo navigation (Streamlit)
├── package.json                # Node.js dependencies for VitePress
├── package-lock.json           # Node.js dependency lock file
├── requirements.txt            # Python dependencies for demos
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── .mcp.json                   # MCP server configuration
└── CLAUDE.md                   # This file
```

## Key Commands

### VitePress Documentation Site
```bash
# Development server
npm run docs:dev

# Build for production
npm run docs:build

# Preview production build
npm run docs:preview
```

### Streamlit Demos
```bash
# Local demo navigation
streamlit run app.py

# Individual demos - Gemini Basic (legacy structure)
cd streamlit-demos/demos/01_gemini_basic
streamlit run gemini_chat.py

# Individual demos - Free Models
cd streamlit-demos/02_free_models
streamlit run free_models_demo.py
```

### Installing Dependencies
```bash
# 1. Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# 2. Install Python dependencies (Streamlit demos)
pip install -r requirements.txt
# Note: Main dependencies include:
# - streamlit, langchain, langchain-google-genai
# - langchain-ollama, langchain-huggingface, langchain-core
# - python-dotenv, requests, transformers, torch

# 3. Install Node.js dependencies (VitePress)
npm install
# Note: Main dependencies include:
# - vitepress, mermaid, vitepress-plugin-mermaid
```

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API keys
# GOOGLE_API_KEY=your_actual_api_key_here
```

## Architecture

### Hybrid Architecture Benefits
- **Static Site (VitePress)**: Fast loading, SEO-friendly documentation deployed to GitHub Pages
- **Interactive Demos (Streamlit)**: Hands-on Python applications with real AI model integration
- **Separation of Concerns**: Documentation for reading, demos for practicing

### VitePress Documentation Site
- **docs/**: Complete learning materials in Markdown
- **GitHub Pages**: Automatic deployment via GitHub Actions
- **Responsive Design**: Mobile-friendly documentation
- **Search & Navigation**: Built-in VitePress features

### Streamlit Demo Structure
Each demo includes:
- Self-contained Streamlit application
- Individual README with setup instructions
- Focused learning objectives
- Error handling examples

### Educational Content Organization
- **docs/tutorials/**: Step-by-step learning content (VitePress)
- **docs/examples/**: Real-world application scenarios (VitePress)
- **docs/demos/**: Demo documentation and instructions (VitePress)
- **streamlit-demos/**: Interactive, runnable examples (Streamlit)

### Integration Patterns
- Dynamic imports for optional dependencies
- Environment-based configuration
- Modular demo architecture
- Consistent UI/UX across demos

## Development Guidelines

### Adding New Demos
1. Create numbered directory in `streamlit-demos/`
2. Include main application file
3. Add comprehensive README
4. Update VitePress demo documentation
5. Update local demo navigation (app.py)

### Content Standards
- Use Traditional Chinese (繁體中文) for UI
- Include error handling examples
- Provide clear setup instructions
- Focus on practical learning outcomes

### MCP Configuration
The project includes MCP server configuration in `.mcp.json` with:
- Serena: Code analysis and editing capabilities
- Context7: Documentation retrieval