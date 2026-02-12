# AI Features Setup Guide

## Overview

CloudStrike includes AI-powered security analysis using OpenAI GPT-3.5 to provide:
- Intelligent attack scenario generation
- Context-aware risk summaries
- Smart remediation recommendations

## Quick Setup

### 1. Get OpenAI API Key

1. Visit https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key (starts with `sk-...`)

### 2. Set API Key (Choose One Method)

**Method A: .env File (Easiest - Recommended)**

1. Install python-dotenv:
```bash
pip install python-dotenv
```

2. Create a file named `.env` in the CloudStrike folder:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

3. Run CloudStrike:
```bash
python main.py
```

That's it! The key is automatically loaded.

**Method B: Environment Variable**

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
python main.py
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
python main.py
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY=sk-your-key-here
python main.py
```

### 3. Verify AI is Active

When you run a scan, check the terminal logs:
```
INFO - Generating AI-powered attack scenarios...
INFO - AI generated 3 attack scenarios
INFO - Generating AI-powered risk summary...
INFO - AI generated risk summary
```

If you see these logs, AI features are working!

## Without AI

CloudStrike works perfectly without AI using rule-based analysis:
- Rule-based attack generation
- Standard risk scoring
- Predefined remediation templates

Simply run without setting the API key.

## Cost Estimate

OpenAI API costs (as of 2024):
- GPT-3.5-turbo: ~$0.002 per scan
- Typical usage: $0.10-0.50 per month for testing

## Troubleshooting

**"OpenAI library not installed"**
```bash
pip install openai
```

**"AI features disabled"**
- Check if OPENAI_API_KEY is set
- Verify API key is valid
- Check internet connection

**"Rate limit exceeded"**
- Wait a few seconds between scans
- Upgrade OpenAI plan if needed

## Privacy

- Findings are sent to OpenAI API for analysis
- No credentials are sent to OpenAI
- Only vulnerability descriptions and metadata are shared
- OpenAI does not store data by default (check their policy)

## Disable AI

To disable AI features:
1. Don't set OPENAI_API_KEY
2. Or set it to empty: `set OPENAI_API_KEY=`

CloudStrike will automatically fall back to rule-based analysis.
