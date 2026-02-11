"""Real cloud scanner orchestrator for CloudStrike Phase-2."""
import logging
from typing import List, Dict, Optional
from cloud.aws_scanner import AWSScanner
from cloud.azure_scanner import AzureScanner
from cloud.gcp_scanner import GCPScanner
from core.attack_engine import AttackEngine
from core.risk_engine import RiskEngine
from remediation.remediation_engine import RemediationEngine

logger = logging.getLogger(__name__)


def run_cloud_scan(credentials: Dict[str, Dict[str, str]]) -> Dict[str, any]:
    """
    Run real cloud security scan across all configured providers.
    
    Args:
        credentials: Dictionary with cloud provider credentials
            {
                'aws': {'access_key': '...', 'secret_key': '...', 'region': '...'},
                'azure': {'tenant_id': '...', 'client_id': '...', 'client_secret': '...'},
                'gcp': {'project_id': '...', 'service_account_path': '...'}
            }
    
    Returns:
        Dictionary with findings, attacks, risk analysis, and remediation scripts:
        {
            'findings': [...],
            'attacks': [...],
            'risk': {...},
            'remediation': [...]
        }
    """
    logger.info("Starting real cloud security scan...")
    all_findings = []
    scanned_clouds = []
    
    aws_creds = credentials.get('aws', {})
    if aws_creds.get('access_key') and aws_creds.get('secret_key'):
        logger.info("Scanning AWS...")
        try:
            aws_scanner = AWSScanner(
                access_key=aws_creds['access_key'],
                secret_key=aws_creds['secret_key'],
                region=aws_creds.get('region', 'us-east-1')
            )
            aws_findings = aws_scanner.run_checks()
            all_findings.extend(aws_findings)
            scanned_clouds.append('AWS')
            logger.info(f"AWS scan complete: {len(aws_findings)} findings")
        except Exception as e:
            logger.error(f"AWS scan failed: {e}")
            all_findings.append({
                "title": "AWS Scan Error",
                "severity": "Warning",
                "cloud": "AWS",
                "description": f"Failed to complete AWS scan: {str(e)}",
                "remediation": "Check AWS credentials and permissions."
            })
    
    azure_creds = credentials.get('azure', {})
    if azure_creds.get('tenant_id') and azure_creds.get('client_id') and azure_creds.get('client_secret'):
        logger.info("Scanning Azure...")
        try:
            azure_scanner = AzureScanner(
                tenant_id=azure_creds['tenant_id'],
                client_id=azure_creds['client_id'],
                client_secret=azure_creds['client_secret']
            )
            azure_findings = azure_scanner.run_checks()
            all_findings.extend(azure_findings)
            scanned_clouds.append('Azure')
            logger.info(f"Azure scan complete: {len(azure_findings)} findings")
        except Exception as e:
            logger.error(f"Azure scan failed: {e}")
            all_findings.append({
                "title": "Azure Scan Error",
                "severity": "Warning",
                "cloud": "Azure",
                "description": f"Failed to complete Azure scan: {str(e)}",
                "remediation": "Check Azure credentials and permissions."
            })
    
    gcp_creds = credentials.get('gcp', {})
    if gcp_creds.get('project_id') and gcp_creds.get('service_account_path'):
        logger.info("Scanning GCP...")
        try:
            gcp_scanner = GCPScanner(
                project_id=gcp_creds['project_id'],
                service_account_path=gcp_creds['service_account_path']
            )
            gcp_findings = gcp_scanner.run_checks()
            all_findings.extend(gcp_findings)
            scanned_clouds.append('GCP')
            logger.info(f"GCP scan complete: {len(gcp_findings)} findings")
        except Exception as e:
            logger.error(f"GCP scan failed: {e}")
            all_findings.append({
                "title": "GCP Scan Error",
                "severity": "Warning",
                "cloud": "GCP",
                "description": f"Failed to complete GCP scan: {str(e)}",
                "remediation": "Check GCP credentials and service account permissions."
            })
    
    if not scanned_clouds:
        logger.warning("No cloud credentials configured")
        return {
            "findings": [{
                "title": "No Credentials Configured",
                "severity": "Info",
                "cloud": "System",
                "description": "No cloud provider credentials have been configured. Please add credentials in the Credentials page.",
                "remediation": "Navigate to Credentials page and configure at least one cloud provider."
            }],
            "attacks": [],
            "risk": {
                "security_score": 100,
                "risk_level": "Low",
                "top_risks": [],
                "summary": "No cloud credentials configured. Add credentials to begin security assessment."
            },
            "remediation": []
        }
    
    logger.info(f"Scan complete. Scanned {len(scanned_clouds)} clouds, found {len(all_findings)} total findings.")
    
    attack_engine = AttackEngine()
    attack_paths = attack_engine.generate_attack_paths(all_findings)
    
    risk_engine = RiskEngine()
    risk_analysis = risk_engine.analyze(all_findings, attack_paths)
    
    remediation_engine = RemediationEngine()
    remediation_scripts = remediation_engine.generate(all_findings)
    
    return {
        "findings": all_findings,
        "attacks": attack_paths,
        "risk": risk_analysis,
        "remediation": remediation_scripts
    }
