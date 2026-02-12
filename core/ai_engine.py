"""AI-powered security analysis engine using Google Gemini."""
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        logger.info("Loaded API key from .env file")
except ImportError:
    pass  # python-dotenv not installed, use environment variables


class AISecurityAnalyzer:
    """AI-powered security analyzer using Google Gemini."""
    
    def __init__(self):
        """Initialize AI analyzer."""
        self.api_key = os.environ.get('GEMINI_API_KEY', '')
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            logger.warning("Gemini API key not found. AI features disabled. Set GEMINI_API_KEY environment variable.")
    
    def generate_ai_attack_scenarios(self, findings: list) -> list:
        """
        Generate AI-powered attack scenarios from findings.
        
        Args:
            findings: List of security findings
            
        Returns:
            List of AI-generated attack scenarios
        """
        if not self.enabled or not findings:
            return []
        
        try:
            from google import genai
            from google.genai import types
            import json
            
            client = genai.Client(api_key=self.api_key)
            
            # Prepare findings summary for AI
            findings_summary = "\n".join([
                f"- {f['title']} ({f['severity']}) on {f['cloud']}: {f['description'][:100]}"
                for f in findings[:5]
            ])
            
            prompt = f"""You are a cybersecurity expert analyzing cloud security vulnerabilities.

Given these security findings:
{findings_summary}

Generate 3 realistic attack scenarios that an attacker could execute. For each scenario:
1. Give it a threatening title
2. List 3-4 specific attack steps
3. Describe the potential impact

Format as JSON array:
[
  {{
    "title": "Attack name",
    "severity": "Critical/High/Medium",
    "cloud": "AWS/Azure/GCP",
    "steps": ["step1", "step2", "step3"],
    "impact": "Description of damage"
  }}
]

Focus on realistic, technical attack chains. Return ONLY the JSON array, no other text."""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            text = response.text.strip()
            
            # Extract JSON from response
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            ai_attacks = json.loads(text)
            logger.info(f"AI generated {len(ai_attacks)} attack scenarios")
            return ai_attacks
            
        except ImportError:
            logger.warning("Google GenAI library not installed. Run: pip install google-genai")
            return []
        except Exception as e:
            logger.error(f"AI attack generation failed: {str(e)}")
            return []
    
    def generate_ai_risk_summary(self, findings: list, attacks: list, security_score: int) -> str:
        """
        Generate AI-powered risk summary.
        
        Args:
            findings: List of security findings
            attacks: List of attack scenarios
            security_score: Current security score
            
        Returns:
            AI-generated risk summary text
        """
        if not self.enabled:
            return self._fallback_risk_summary(findings, security_score)
        
        try:
            from google import genai
            
            client = genai.Client(api_key=self.api_key)
            
            critical_count = sum(1 for f in findings if f['severity'] == 'Critical')
            high_count = sum(1 for f in findings if f['severity'] == 'High')
            
            prompt = f"""Analyze this cloud security posture:
- Security Score: {security_score}/100
- Critical Issues: {critical_count}
- High Severity Issues: {high_count}
- Total Findings: {len(findings)}
- Attack Paths: {len(attacks)}

Write a 2-3 sentence executive summary of the security risks. Be direct and actionable."""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            summary = response.text.strip()
            logger.info("AI generated risk summary")
            return summary
            
        except Exception as e:
            logger.error(f"AI risk summary failed: {str(e)}")
            return self._fallback_risk_summary(findings, security_score)
    
    def generate_ai_remediation_advice(self, finding: dict) -> str:
        """
        Generate AI-powered remediation advice.
        
        Args:
            finding: Security finding dictionary
            
        Returns:
            AI-generated remediation advice
        """
        if not self.enabled:
            return "Apply security best practices and follow cloud provider guidelines."
        
        try:
            from google import genai
            
            client = genai.Client(api_key=self.api_key)
            
            prompt = f"""Security Issue: {finding['title']}
Cloud: {finding['cloud']}
Severity: {finding['severity']}
Description: {finding['description']}

Provide a 1-sentence actionable remediation recommendation."""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"AI remediation advice failed: {str(e)}")
            return "Apply security best practices and follow cloud provider guidelines."
    
    def _fallback_risk_summary(self, findings: list, security_score: int) -> str:
        """Generate fallback risk summary when AI is unavailable."""
        critical_count = sum(1 for f in findings if f['severity'] == 'Critical')
        
        if security_score >= 80:
            return f"Your cloud environment has a strong security posture with {len(findings)} minor issues to address."
        elif security_score >= 60:
            return f"Your cloud environment has moderate security risks with {critical_count} critical issues requiring immediate attention."
        else:
            return f"Your cloud environment has significant security vulnerabilities with {critical_count} critical issues that pose immediate risk."


# Global AI analyzer instance
ai_analyzer = AISecurityAnalyzer()
