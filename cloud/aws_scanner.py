"""AWS security scanner using boto3."""
import logging
from typing import List, Dict, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


class AWSScanner:
    """Real AWS security misconfiguration scanner."""
    
    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS scanner.
        
        Args:
            access_key: AWS access key ID
            secret_key: AWS secret access key
            region: AWS region
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.session = None
        
    def _create_session(self) -> bool:
        """Create AWS session with credentials."""
        try:
            self.session = boto3.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )
            return True
        except Exception as e:
            logger.error(f"Failed to create AWS session: {e}")
            return False
            
    def run_checks(self) -> List[Dict[str, str]]:
        """
        Run all AWS security checks.
        
        Returns:
            List of findings
        """
        if not self._create_session():
            return [{
                "title": "AWS Authentication Failed",
                "severity": "Critical",
                "cloud": "AWS",
                "description": "Unable to authenticate with provided AWS credentials.",
                "remediation": "Verify your AWS access key and secret key are correct."
            }]
        
        findings = []
        findings.extend(self._check_public_s3_buckets())
        findings.extend(self._check_overpermissive_iam())
        findings.extend(self._check_cloudtrail())
        
        return findings
        
    def _check_public_s3_buckets(self) -> List[Dict[str, str]]:
        """Check for publicly accessible S3 buckets."""
        findings = []
        
        try:
            s3 = self.session.client('s3')
            buckets = s3.list_buckets()
            
            for bucket in buckets.get('Buckets', []):
                bucket_name = bucket['Name']
                
                try:
                    acl = s3.get_bucket_acl(Bucket=bucket_name)
                    
                    for grant in acl.get('Grants', []):
                        grantee = grant.get('Grantee', {})
                        uri = grantee.get('URI', '')
                        
                        if 'AllUsers' in uri or 'AuthenticatedUsers' in uri:
                            findings.append({
                                "title": f"Public S3 Bucket: {bucket_name}",
                                "severity": "Critical",
                                "cloud": "AWS",
                                "description": f"S3 bucket '{bucket_name}' has public access via ACL grants.",
                                "remediation": f"Remove public ACL grants: aws s3api put-bucket-acl --bucket {bucket_name} --acl private"
                            })
                            break
                    
                    try:
                        policy_status = s3.get_bucket_policy_status(Bucket=bucket_name)
                        if policy_status.get('PolicyStatus', {}).get('IsPublic'):
                            findings.append({
                                "title": f"Public S3 Bucket Policy: {bucket_name}",
                                "severity": "Critical",
                                "cloud": "AWS",
                                "description": f"S3 bucket '{bucket_name}' has a public bucket policy.",
                                "remediation": f"Review and restrict bucket policy to remove public access."
                            })
                    except ClientError:
                        pass
                        
                except ClientError as e:
                    logger.debug(f"Cannot check bucket {bucket_name}: {e}")
                    
        except NoCredentialsError:
            logger.error("AWS credentials not found")
        except ClientError as e:
            logger.error(f"Error checking S3 buckets: {e}")
            
        return findings
        
    def _check_overpermissive_iam(self) -> List[Dict[str, str]]:
        """Check for overly permissive IAM roles."""
        findings = []
        
        try:
            iam = self.session.client('iam')
            roles = iam.list_roles()
            
            for role in roles.get('Roles', [])[:10]:
                role_name = role['RoleName']
                
                try:
                    attached_policies = iam.list_attached_role_policies(RoleName=role_name)
                    
                    for policy in attached_policies.get('AttachedPolicies', []):
                        if 'AdministratorAccess' in policy['PolicyName'] or 'FullAccess' in policy['PolicyName']:
                            findings.append({
                                "title": f"Over-Permissive IAM Role: {role_name}",
                                "severity": "Critical",
                                "cloud": "AWS",
                                "description": f"IAM role '{role_name}' has administrator or full access policy attached.",
                                "remediation": "Apply principle of least privilege. Remove overly broad policies and grant only required permissions."
                            })
                            break
                            
                except ClientError as e:
                    logger.debug(f"Cannot check role {role_name}: {e}")
                    
        except ClientError as e:
            logger.error(f"Error checking IAM roles: {e}")
            
        return findings
        
    def _check_cloudtrail(self) -> List[Dict[str, str]]:
        """Check if CloudTrail is enabled."""
        findings = []
        
        try:
            cloudtrail = self.session.client('cloudtrail')
            trails = cloudtrail.describe_trails()
            
            if not trails.get('trailList'):
                findings.append({
                    "title": "CloudTrail Not Enabled",
                    "severity": "Warning",
                    "cloud": "AWS",
                    "description": "No CloudTrail trails found. Logging is not enabled for this account.",
                    "remediation": "Enable CloudTrail to log all API calls: aws cloudtrail create-trail --name main-trail --s3-bucket-name <bucket>"
                })
            else:
                for trail in trails['trailList']:
                    trail_name = trail['Name']
                    status = cloudtrail.get_trail_status(Name=trail_name)
                    
                    if not status.get('IsLogging'):
                        findings.append({
                            "title": f"CloudTrail Not Logging: {trail_name}",
                            "severity": "Warning",
                            "cloud": "AWS",
                            "description": f"CloudTrail '{trail_name}' exists but is not actively logging.",
                            "remediation": f"Start logging: aws cloudtrail start-logging --name {trail_name}"
                        })
                        
        except ClientError as e:
            logger.error(f"Error checking CloudTrail: {e}")
            
        return findings
