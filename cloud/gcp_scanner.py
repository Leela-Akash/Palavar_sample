"""GCP security scanner using Google Cloud SDK."""
import logging
from typing import List, Dict
from google.cloud import storage
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPIError

logger = logging.getLogger(__name__)


class GCPScanner:
    """Real GCP security misconfiguration scanner."""
    
    def __init__(self, project_id: str, service_account_path: str):
        """
        Initialize GCP scanner.
        
        Args:
            project_id: GCP project ID
            service_account_path: Path to service account JSON file
        """
        self.project_id = project_id
        self.service_account_path = service_account_path
        self.credentials = None
        
    def _create_credentials(self) -> bool:
        """Create GCP credentials from service account."""
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                self.service_account_path
            )
            return True
        except Exception as e:
            logger.error(f"Failed to load GCP credentials: {e}")
            return False
            
    def run_checks(self) -> List[Dict[str, str]]:
        """
        Run all GCP security checks.
        
        Returns:
            List of findings
        """
        if not self._create_credentials():
            return [{
                "title": "GCP Authentication Failed",
                "severity": "Critical",
                "cloud": "GCP",
                "description": "Unable to load GCP service account credentials from provided path.",
                "remediation": "Verify the service account JSON file path is correct and accessible."
            }]
        
        findings = []
        findings.extend(self._check_public_gcs_buckets())
        
        return findings
        
    def _check_public_gcs_buckets(self) -> List[Dict[str, str]]:
        """Check for publicly accessible GCS buckets."""
        findings = []
        
        try:
            storage_client = storage.Client(
                project=self.project_id,
                credentials=self.credentials
            )
            
            buckets = storage_client.list_buckets()
            
            for bucket in buckets:
                try:
                    policy = bucket.get_iam_policy(requested_policy_version=3)
                    
                    for binding in policy.bindings:
                        members = binding.get('members', [])
                        
                        for member in members:
                            if member == 'allUsers' or member == 'allAuthenticatedUsers':
                                findings.append({
                                    "title": f"Public GCS Bucket: {bucket.name}",
                                    "severity": "Critical",
                                    "cloud": "GCP",
                                    "description": f"Cloud Storage bucket '{bucket.name}' is publicly accessible to {member}.",
                                    "remediation": f"Remove public access: gsutil iam ch -d {member} gs://{bucket.name}"
                                })
                                break
                                
                    if bucket.versioning_enabled is False:
                        findings.append({
                            "title": f"Versioning Disabled: {bucket.name}",
                            "severity": "Warning",
                            "cloud": "GCP",
                            "description": f"Cloud Storage bucket '{bucket.name}' does not have versioning enabled.",
                            "remediation": f"Enable versioning: gsutil versioning set on gs://{bucket.name}"
                        })
                        
                except GoogleAPIError as e:
                    logger.debug(f"Cannot check bucket {bucket.name}: {e}")
                    
        except GoogleAPIError as e:
            logger.error(f"Error checking GCS buckets: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            
        return findings
