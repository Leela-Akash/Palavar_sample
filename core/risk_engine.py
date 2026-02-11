"""Risk scoring engine for CloudStrike Phase-4."""
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class RiskEngine:
    """Intelligent rule-based risk scoring and analysis engine."""
    
    @staticmethod
    def analyze(findings: List[Dict[str, str]], attacks: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Analyze findings and attacks to produce security score and risk assessment.
        
        Args:
            findings: List of security findings
            attacks: List of attack simulations
            
        Returns:
            Dictionary with security_score, risk_level, top_risks, and summary
        """
        logger.info(f"Analyzing {len(findings)} findings and {len(attacks)} attacks...")
        
        score = 100
        
        # Apply severity penalties for findings
        for finding in findings:
            severity = finding.get("severity", "Info")
            if severity == "Critical":
                score -= 15
            elif severity == "Warning":
                score -= 8
            elif severity == "Info":
                score -= 3
        
        # Apply attack penalties
        for attack in attacks:
            severity = attack.get("severity", "Medium")
            if severity == "Critical":
                score -= 20
            elif severity == "High":
                score -= 15
            elif severity == "Medium":
                score -= 10
        
        # Cloud exposure bonus penalty
        affected_clouds = set()
        for finding in findings:
            cloud = finding.get("cloud", "")
            if cloud and cloud != "System":
                affected_clouds.add(cloud)
        
        if len(affected_clouds) > 1:
            score -= 10
            logger.info(f"Multi-cloud exposure detected: {affected_clouds}")
        
        # Persistence risk penalty
        for attack in attacks:
            title = attack.get("title", "").lower()
            if "persistence" in title or "privilege escalation" in title:
                score -= 10
                logger.info(f"High-risk attack detected: {attack.get('title')}")
        
        # Clamp score between 0-100
        score = max(0, min(100, score))
        
        # Determine risk level
        if score >= 80:
            risk_level = "Low"
        elif score >= 60:
            risk_level = "Medium"
        elif score >= 40:
            risk_level = "High"
        else:
            risk_level = "Critical"
        
        # Get top 3 risks sorted by severity
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Warning": 3, "Info": 4}
        sorted_attacks = sorted(
            attacks,
            key=lambda x: severity_order.get(x.get("severity", "Medium"), 5)
        )
        top_risks = [attack["title"] for attack in sorted_attacks[:3]]
        
        # Generate summary
        summary = RiskEngine._generate_summary(
            score, risk_level, len(findings), len(attacks), affected_clouds
        )
        
        logger.info(f"Risk analysis complete: Score={score}, Level={risk_level}")
        
        return {
            "security_score": score,
            "risk_level": risk_level,
            "top_risks": top_risks,
            "summary": summary
        }
    
    @staticmethod
    def _generate_summary(
        score: int,
        risk_level: str,
        findings_count: int,
        attacks_count: int,
        affected_clouds: set
    ) -> str:
        """Generate human-readable risk summary."""
        
        if risk_level == "Critical":
            summary = f"CRITICAL SECURITY POSTURE: Your cloud infrastructure has severe vulnerabilities. "
            summary += f"Detected {findings_count} security issues enabling {attacks_count} potential attack paths. "
            summary += "Immediate remediation required to prevent data breaches and account compromise."
        
        elif risk_level == "High":
            summary = f"HIGH RISK DETECTED: Your environment has significant security gaps. "
            summary += f"Found {findings_count} misconfigurations that could lead to {attacks_count} attack scenarios. "
            summary += "Priority remediation recommended within 24-48 hours."
        
        elif risk_level == "Medium":
            summary = f"MODERATE SECURITY CONCERNS: Your infrastructure has some vulnerabilities. "
            summary += f"Identified {findings_count} issues with {attacks_count} possible attack vectors. "
            summary += "Address critical findings to improve security posture."
        
        else:  # Low
            if findings_count == 0:
                summary = "EXCELLENT SECURITY POSTURE: No significant vulnerabilities detected. "
                summary += "Your cloud infrastructure follows security best practices. Continue monitoring."
            else:
                summary = f"GOOD SECURITY POSTURE: Minor issues detected. "
                summary += f"Found {findings_count} low-priority items. "
                summary += "Address remaining findings to achieve optimal security."
        
        if len(affected_clouds) > 1:
            summary += f" Multi-cloud exposure across {', '.join(affected_clouds)} increases attack surface."
        
        return summary
