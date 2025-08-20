# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive LangChain educational website using a hybrid architecture:
- **VitePress**: Static documentation site deployed to GitHub Pages
- **Streamlit**: Interactive demos for hands-on learning

## Project Structure

```
/
├── docs/                         # VitePress documentation site
│   ├── .vitepress/              # VitePress configuration
│   │   └── config.js            # Site configuration
│   ├── index.md                 # Homepage
│   ├── tutorials/               # Tutorial documentation
│   ├── examples/                # Example documentation  
│   └── demos/                   # Demo documentation
├── streamlit-demos/             # Interactive Streamlit applications
│   ├── 01_gemini_basic/        # Gemini API integration demo
│   │   ├── gemini_chat.py      # Chat application
│   │   └── README.md           # Demo documentation
│   └── README.md               # Demo overview
├── .github/workflows/           # GitHub Actions for deployment
│   └── deploy.yml              # VitePress to GitHub Pages
├── app.py                      # Local demo navigation (Streamlit)
├── package.json                # Node.js dependencies for VitePress
├── requirements.txt            # Python dependencies for demos
├── .env                        # Environment variables (not in git)
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

# Individual demos
cd streamlit-demos/01_gemini_basic
streamlit run gemini_chat.py
```

### Installing Dependencies
```bash
# 1. Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# 2. Install Python dependencies (Streamlit demos)
pip install -r requirements.txt

# 3. Install Node.js dependencies (VitePress)
npm install
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