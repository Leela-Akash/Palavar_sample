"""Azure security scanner using Azure SDK."""
import logging
from typing import List, Dict
from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import AzureError

logger = logging.getLogger(__name__)


class AzureScanner:
    """Real Azure security misconfiguration scanner."""
    
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        """
        Initialize Azure scanner.
        
        Args:
            tenant_id: Azure tenant ID
            client_id: Azure client ID
            client_secret: Azure client secret
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.credential = None
        
    def _create_credential(self) -> bool:
        """Create Azure credential."""
        try:
            self.credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            return True
        except Exception as e:
            logger.error(f"Failed to create Azure credential: {e}")
            return False
            
    def run_checks(self) -> List[Dict[str, str]]:
        """
        Run all Azure security checks.
        
        Returns:
            List of findings
        """
        if not self._create_credential():
            return [{
                "title": "Azure Authentication Failed",
                "severity": "Critical",
                "cloud": "Azure",
                "description": "Unable to authenticate with provided Azure credentials.",
                "remediation": "Verify your Azure tenant ID, client ID, and client secret are correct."
            }]
        
        findings = []
        findings.extend(self._check_public_storage_accounts())
        
        return findings
        
    def _check_public_storage_accounts(self) -> List[Dict[str, str]]:
        """Check for publicly accessible storage accounts."""
        findings = []
        
        try:
            from azure.mgmt.resource import SubscriptionClient
            
            subscription_client = SubscriptionClient(self.credential)
            subscriptions = list(subscription_client.subscriptions.list())
            
            if not subscriptions:
                return [{
                    "title": "No Azure Subscriptions Found",
                    "severity": "Info",
                    "cloud": "Azure",
                    "description": "No accessible Azure subscriptions found with provided credentials.",
                    "remediation": "Ensure the service principal has Reader access to subscriptions."
                }]
            
            for subscription in subscriptions[:3]:
                subscription_id = subscription.subscription_id
                
                try:
                    storage_client = StorageManagementClient(self.credential, subscription_id)
                    storage_accounts = storage_client.storage_accounts.list()
                    
                    for account in storage_accounts:
                        if hasattr(account, 'allow_blob_public_access') and account.allow_blob_public_access:
                            findings.append({
                                "title": f"Public Storage Account: {account.name}",
                                "severity": "Critical",
                                "cloud": "Azure",
                                "description": f"Storage account '{account.name}' allows public blob access.",
                                "remediation": f"Disable public access: az storage account update --name {account.name} --allow-blob-public-access false"
                            })
                            
                        if hasattr(account, 'enable_https_traffic_only') and not account.enable_https_traffic_only:
                            findings.append({
                                "title": f"HTTPS Not Enforced: {account.name}",
                                "severity": "Warning",
                                "cloud": "Azure",
                                "description": f"Storage account '{account.name}' does not enforce HTTPS-only traffic.",
                                "remediation": f"Enable HTTPS only: az storage account update --name {account.name} --https-only true"
                            })
                            
                except AzureError as e:
                    logger.debug(f"Cannot check subscription {subscription_id}: {e}")
                    
        except AzureError as e:
            logger.error(f"Error checking Azure storage accounts: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            
        return findings
