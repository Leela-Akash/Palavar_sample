# CloudStrike - AI-Powered Cloud Security Auditor

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**CloudStrike** is an advanced cybersecurity tool that performs automated penetration testing and security auditing for AWS, Azure, and GCP cloud environments. It combines real cloud scanning with AI-powered attack simulation to identify vulnerabilities and generate actionable remediation strategies.

---

## 🚀 Key Features

### Core Capabilities
- 🤖 **AI-Powered Analysis** - Uses Google Gemini AI to generate intelligent attack scenarios and risk assessments
- ☁️ **Multi-Cloud Support** - Scan AWS, Azure, and GCP environments from a single interface
- 🔍 **Real Security Scanning** - Actual cloud API integration (not simulated)
- ⚔️ **Attack Chain Simulation** - Step-by-step exploitation paths based on discovered vulnerabilities
- 🛠️ **Auto-Remediation** - Generate CLI commands and Terraform scripts to fix issues
- 📊 **Professional Dashboard** - Modern cyberpunk-themed UI with real-time metrics
- 📈 **Risk Scoring Engine** - Intelligent security posture assessment (0-100 scale)
- 📄 **Export Reports** - JSON and PDF report generation
- 🔐 **Credential Management** - Secure credential validation before scanning

### AI Features (Optional)
When configured with a Gemini API key, CloudStrike provides:
- **Intelligent Attack Generation** - Context-aware, realistic attack scenarios
- **Executive Risk Summaries** - AI-generated security posture assessments
- **Smart Remediation Advice** - Tailored fix recommendations

> **Note:** CloudStrike works perfectly without AI using rule-based analysis. AI features enhance the intelligence but are not required.

---

## 📦 What We Implemented

### Architecture
- **Modular Design** - Separated concerns: core scanning, UI, cloud providers, remediation
- **Thread-Safe Operations** - All long-running tasks use QThread workers
- **Signal-Based Communication** - Clean separation between business logic and UI
- **Graceful Fallbacks** - System works even when AI or cloud credentials are unavailable

### Cloud Scanners
- **AWS Scanner** - S3 bucket permissions, IAM roles, CloudTrail logging
- **Azure Scanner** - Storage account access, HTTPS enforcement
- **GCP Scanner** - GCS bucket permissions, versioning status

### Security Engines
- **Attack Engine** - Rule-based attack path generation (data exfiltration, privilege escalation, persistence)
- **AI Engine** - Google Gemini integration for enhanced intelligence
- **Risk Engine** - Severity-based scoring with penalty system
- **Remediation Engine** - Automated fix script generation (CLI + Terraform)

### User Interface
- **Dashboard Page** - Security overview with metrics and activity feed
- **Cloud Setup & Scan Page** - Credential management and scan execution
- **Attack Simulation Page** - Visual attack path display
- **Reports Page** - Detailed findings with collapsible cards and export options
- **Toast Notifications** - Real-time feedback for user actions
- **Progress Tracking** - 5-stage scan pipeline with terminal-style logs

### Design System
- **Cyberpunk Theme** - Neon colors (#00ffd5 primary, #ff3c7e accent)
- **8px Spacing System** - Consistent layout (4, 8, 16, 24, 32)
- **JetBrains Mono Font** - Professional monospace typography
- **Layout-Based UI** - No absolute positioning, fully responsive

---

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.11 or higher**
- **pip** (Python package manager)
- **Cloud Provider Credentials** (AWS, Azure, or GCP)
- **Gemini API Key** (optional, for AI features)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Leela-Akash/Automated-Cloud-Pentesting-Security-Auditor.git
cd CloudStrike
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `PySide6` - GUI framework
- `boto3` - AWS SDK
- `azure-identity`, `azure-mgmt-storage`, `azure-mgmt-resource` - Azure SDK
- `google-cloud-storage`, `google-auth` - GCP SDK
- `google-genai` - Google Gemini AI
- `python-dotenv` - Environment variable management
- `reportlab` - PDF generation

### Step 3: Configure Cloud Credentials

#### AWS Credentials
Create `~/.aws/credentials` (Linux/Mac) or `C:\Users\YourName\.aws\credentials` (Windows):
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

Or set environment variables:
```bash
# Windows
set AWS_ACCESS_KEY_ID=your_key
set AWS_SECRET_ACCESS_KEY=your_secret

# Linux/Mac
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

#### Azure Credentials
```bash
az login
```

#### GCP Credentials
```bash
# Set path to service account JSON
set GOOGLE_APPLICATION_CREDENTIALS=path\to\service-account.json
```

### Step 4: Configure AI Features (Optional)

1. **Get a free Gemini API key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the key

2. **Create `.env` file in project root:**
```bash
# CloudStrike AI Configuration
GEMINI_API_KEY=your-api-key-here
```

> **Tip:** Without AI configuration, CloudStrike uses rule-based analysis automatically.

---

## 🎯 Running CloudStrike

### Start the Application
```bash
python main.py
```

### Using the Application

#### 1. Dashboard (Home)
- View security overview and statistics
- Monitor recent activity
- Check scan history

#### 2. Cloud Setup & Scan
- **Select Cloud Provider** - Choose AWS, Azure, or GCP tab
- **Enter Credentials** - Provide access keys/tokens
- **Validate Connection** - Click "Start Cloud Scan" to validate credentials
- **Run Scan** - Watch the 5-stage scan pipeline:
  1. Credential Validation (10%)
  2. Cloud Misconfiguration Scan (60%)
  3. Attack Simulation (80%)
  4. Risk Analysis (90%)
  5. Remediation Generation (100%)

#### 3. Attack Simulation
- View AI-generated attack scenarios
- See step-by-step exploitation paths
- Understand potential impact
- Navigate to full report

#### 4. Security Reports
- **Executive Summary** - Security score, risk level, findings count
- **Vulnerability Cards** - Collapsible detailed findings
- **Attack Paths** - Exploitation scenarios
- **Remediation Scripts** - CLI commands and Terraform code
- **Export Options** - Download as JSON or PDF

---

## 📁 Project Structure

```
CloudStrike/
├── main.py                      # Application entry point
├── config.py                    # Design system constants
├── requirements.txt             # Python dependencies
├── .env                         # API keys (create this)
├── README.md                    # This file
│
├── assets/
│   └── theme.qss               # Global stylesheet
│
├── core/
│   ├── scanner.py              # Cloud scanner orchestrator
│   ├── attack_engine.py        # Rule-based attack generation
│   ├── ai_engine.py            # AI-powered analysis (Gemini)
│   ├── risk_engine.py          # Risk scoring engine
│   └── scan_history.py         # Scan tracking
│
├── cloud/
│   ├── aws_scanner.py          # AWS security checks
│   ├── azure_scanner.py        # Azure security checks
│   └── gcp_scanner.py          # GCP security checks
│
├── remediation/
│   └── remediation_engine.py   # Auto-fix generation
│
├── ui/
│   ├── main_window.py          # Main application window
│   ├── dashboard.py            # Security dashboard
│   ├── cloud_setup_scan_page.py # Credentials + Scan
│   ├── attack_page.py          # Attack simulation viewer
│   └── report_page.py          # Security reports
│
└── components/
    ├── glow_button.py          # Neon button component
    ├── cyber_card.py           # Card component
    ├── metric_card.py          # Dashboard metric card
    └── toast.py                # Notification widget
```

---

## 🔒 Security & Permissions

### Required Cloud Permissions

**AWS (Read-Only):**
- `s3:GetBucketAcl`
- `s3:GetBucketPolicy`
- `iam:ListRoles`
- `iam:GetRolePolicy`
- `cloudtrail:DescribeTrails`
- `sts:GetCallerIdentity`

**Azure (Read-Only):**
- `Microsoft.Storage/storageAccounts/read`
- `Microsoft.Resources/subscriptions/read`

**GCP (Read-Only):**
- `storage.buckets.list`
- `storage.buckets.get`

> **Important:** CloudStrike requires **read-only** permissions. It does NOT make any changes to your cloud infrastructure.

---

## 🐛 Troubleshooting

### Issue: "Gemini API key not found"
**Solution:** Create `.env` file with `GEMINI_API_KEY=your-key`. Or run without AI (uses rule-based analysis).

### Issue: "AWS credentials not found"
**Solution:** Configure `~/.aws/credentials` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.

### Issue: "Azure authentication failed"
**Solution:** Run `az login` in terminal to authenticate.

### Issue: "GCP authentication failed"
**Solution:** Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable to service account JSON path.

### Issue: "Unknown property box-shadow warnings"
**Solution:** These are harmless Qt warnings (Qt doesn't support CSS box-shadow). Ignore them.

### Issue: "Module not found" errors
**Solution:** Run `pip install -r requirements.txt` to install all dependencies.

---

## 🆚 Comparison to Existing Tools

| Feature | ScoutSuite | Prowler | CloudStrike |
|---------|-----------|---------|-------------|
| Multi-cloud | ✅ | ✅ | ✅ |
| Attack Simulation | ❌ | ❌ | ✅ |
| AI-Powered Analysis | ❌ | ❌ | ✅ |
| GUI Dashboard | ❌ | ❌ | ✅ |
| Auto-Remediation | ❌ | ❌ | ✅ |
| Risk Scoring | ✅ | ✅ | ✅ |
| Real-time Scanning | ✅ | ✅ | ✅ |

---

## 📊 Scan Results Example

```
Security Score: 62/100
Risk Level: Medium
Total Findings: 1
Attack Paths: 1

Findings:
- [High] Public S3 Bucket Detected
  Resource: my-bucket
  Impact: Data exfiltration risk
  
Attack Scenarios:
- Stealth Persistence Attack
  Steps:
    1. Enumerate public S3 buckets
    2. Upload malicious objects
    3. Establish backdoor access
  Impact: Long-term unauthorized access

Remediation:
  CLI: aws s3api put-bucket-acl --bucket my-bucket --acl private
  Terraform: acl = "private"
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **PySide6** - Qt for Python GUI framework
- **Google Gemini** - AI-powered security analysis
- **AWS/Azure/GCP SDKs** - Cloud provider integrations
- **ReportLab** - PDF generation

---

## 📧 Contact

For questions, issues, or feature requests, please open an issue on GitHub.

---

**⚠️ Disclaimer:** CloudStrike is for authorized security testing only. Always obtain proper authorization before scanning cloud environments. The developers are not responsible for misuse of this tool.
