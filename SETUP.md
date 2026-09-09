# 🤖 AI Knowledge Assistant - Setup Guide

## Installation

### Prerequisites
- Python 3.8+
- pip or conda
- OpenAI API key

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd AI
```

### Step 2: Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

Get your API key from: https://platform.openai.com/api-keys

### Step 5: Run the Application
```bash
python main.py
```

## Features

✨ **Interactive Menu**
- 🔍 Ask questions
- 🌐 Add websites to knowledge base
- 📊 View database statistics
- 🗑️ Clear knowledge base

## How It Works

1. **Add Website**: Extract and process web content
2. **Store**: Save text chunks in vector database (ChromaDB)
3. **Query**: Search for relevant context based on your question
4. **Answer**: Generate AI-powered responses using OpenAI GPT

## Configuration

Edit `config.json` to customize:
- Chat model (default: gpt-3.5-turbo)
- Embedding model
- Chunk size and overlap
- Max context length

## Troubleshooting

### OpenAI API Key Error
- Ensure `.env` file exists and contains `OPENAI_API_KEY`
- Verify the API key is valid
- Check API usage limits on OpenAI dashboard

### Database Issues
- Clear database: Choose option 4 from menu
- Data stored in: `./data/chroma_db/`

## Project Structure
```
AI/
├── main.py              # Entry point
├── config.json          # Configuration
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── core/
│   ├── __init__.py
│   ├── config.py        # Configuration management
│   ├── agent.py         # AI agent
│   ├── database.py      # Vector database
│   └── processor.py     # Web processor
├── ui/
│   ├── __init__.py
│   └── console.py       # Console interface
└── data/
    └── .gitkeep
```

## License
MIT License

## Support
For issues and questions, create a GitHub issue.
