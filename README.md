# CloudStrike - Automated Cloud Pentesting & Security Auditor

Professional cybersecurity tool for testing AWS, Azure, and GCP environments for security misconfigurations.

## Phase 1: Foundation + Cyber Dashboard UI + Fake Scanner Engine

This is a production-ready implementation with clean, modular, and scalable code.

## Features

- 🎨 Professional cyberpunk-themed UI
- ☁️ Multi-cloud support (AWS, Azure, GCP)
- 🔍 Automated security scanning
- 📊 Interactive dashboard
- 📋 Detailed security reports
- 🔑 Secure credential management

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Project Structure

```
CloudStrike/
├── main.py                 # Application entry point
├── config.py              # Design system constants
├── core/
│   └── scanner.py         # Fake scanner engine
├── ui/
│   ├── main_window.py     # Main application window
│   ├── dashboard.py       # Dashboard page
│   ├── credentials_page.py # Credentials management
│   ├── scan_page.py       # Scan execution
│   └── report_page.py     # Security reports
├── components/
│   ├── glow_button.py     # Neon glow button
│   ├── cyber_card.py      # Container card
│   ├── section_header.py  # Section headers
│   ├── status_badge.py    # Status badges
│   └── input_field.py     # Aligned input fields
└── assets/
    └── theme.qss          # Global stylesheet
```

## Design System

- **Color Palette**: Cyberpunk neon theme
- **Spacing**: 8px system (4, 8, 16, 24, 32)
- **Font**: JetBrains Mono / Consolas
- **Layout**: 100% layout-based (no absolute positioning)

## Usage

1. **Dashboard**: View security overview and statistics
2. **Credentials**: Configure cloud provider credentials
3. **Scan Center**: Execute security scans
4. **Reports**: Review detailed findings

## Current Status

✅ Phase 1 Complete
- Professional UI implementation
- Reusable component library
- Fake scanner engine
- Multi-cloud credential management
- Interactive reporting

## Next Phases

- Phase 2: Real cloud API integration
- Phase 3: Advanced attack chain simulation
- Phase 4: Automated remediation

## License

Proprietary - CloudStrike Security
