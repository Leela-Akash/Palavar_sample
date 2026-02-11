"""Auto-remediation script generator for CloudStrike Phase-5."""
import logging
import re
from typing import List, Dict

logger = logging.getLogger(__name__)


class RemediationEngine:
    """Generates automated remediation scripts from security findings."""
    
    @staticmethod
    def generate(findings: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Generate remediation scripts for security findings.
        
        Args:
            findings: List of security findings
            
        Returns:
            List of remediation script dictionaries with CLI and Terraform code
        """
        logger.info(f"Generating remediation scripts for {len(findings)} findings...")
        
        remediation_scripts = []
        processed_types = set()
        
        for finding in findings:
            title = finding.get("title", "").lower()
            cloud = finding.get("cloud", "Unknown")
            
            # Extract resource names from title
            bucket_match = re.search(r"['\"]([\w\-]+)['\"]", finding.get("title", ""))
            resource_name = bucket_match.group(1) if bucket_match else "<RESOURCE_NAME>"
            
            if "public s3 bucket" in title and "s3_public" not in processed_types:
                remediation_scripts.append({
                    "title": "Fix Public S3 Bucket Access",
                    "cloud": "AWS",
                    "resource": resource_name,
                    "cli_script": f"""# Block all public access to S3 bucket
aws s3api put-public-access-block \\
  --bucket {resource_name} \\
  --public-access-block-configuration \\
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Remove public ACLs
aws s3api put-bucket-acl --bucket {resource_name} --acl private""",
                    "terraform": f"""resource "aws_s3_bucket_public_access_block" "{resource_name}_block" {{
  bucket = aws_s3_bucket.{resource_name}.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}}"""
                })
                processed_types.add("s3_public")
            
            elif "over-permissive iam" in title and "iam_permissive" not in processed_types:
                role_name = resource_name if "role" in title else "<ROLE_NAME>"
                remediation_scripts.append({
                    "title": "Restrict Over-Permissive IAM Role",
                    "cloud": "AWS",
                    "resource": role_name,
                    "cli_script": f"""# Detach overly permissive policies
aws iam detach-role-policy \\
  --role-name {role_name} \\
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Attach least-privilege policy instead
aws iam attach-role-policy \\
  --role-name {role_name} \\
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess""",
                    "terraform": f"""resource "aws_iam_role_policy_attachment" "{role_name}_restricted" {{
  role       = aws_iam_role.{role_name}.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}}

# Remove this block:
# resource "aws_iam_role_policy_attachment" "{role_name}_admin" {{
#   role       = aws_iam_role.{role_name}.name
#   policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
# }}"""
                })
                processed_types.add("iam_permissive")
            
            elif "cloudtrail" in title and ("not" in title or "disabled" in title) and "cloudtrail_disabled" not in processed_types:
                trail_name = resource_name if "trail" in title else "security-trail"
                remediation_scripts.append({
                    "title": "Enable CloudTrail Logging",
                    "cloud": "AWS",
                    "resource": trail_name,
                    "cli_script": f"""# Create S3 bucket for CloudTrail logs
aws s3 mb s3://cloudtrail-logs-$(aws sts get-caller-identity --query Account --output text)

# Create CloudTrail
aws cloudtrail create-trail \\
  --name {trail_name} \\
  --s3-bucket-name cloudtrail-logs-$(aws sts get-caller-identity --query Account --output text) \\
  --is-multi-region-trail

# Start logging
aws cloudtrail start-logging --name {trail_name}""",
                    "terraform": f"""resource "aws_cloudtrail" "{trail_name}" {{
  name                          = "{trail_name}"
  s3_bucket_name               = aws_s3_bucket.cloudtrail_logs.id
  include_global_service_events = true
  is_multi_region_trail        = true
  enable_logging               = true

  event_selector {{
    read_write_type           = "All"
    include_management_events = true
  }}
}}"""
                })
                processed_types.add("cloudtrail_disabled")
            
            elif "public storage" in title and cloud == "Azure" and "azure_storage" not in processed_types:
                storage_name = resource_name if "storage" in title else "<STORAGE_ACCOUNT>"
                remediation_scripts.append({
                    "title": "Disable Public Access on Azure Storage",
                    "cloud": "Azure",
                    "resource": storage_name,
                    "cli_script": f"""# Disable public blob access
az storage account update \\
  --name {storage_name} \\
  --allow-blob-public-access false

# Require HTTPS only
az storage account update \\
  --name {storage_name} \\
  --https-only true""",
                    "terraform": f"""resource "azurerm_storage_account" "{storage_name}" {{
  name                     = "{storage_name}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  allow_blob_public_access = false
  enable_https_traffic_only = true
  min_tls_version          = "TLS1_2"
}}"""
                })
                processed_types.add("azure_storage")
            
            elif "https" in title and "not enforced" in title and "azure_https" not in processed_types:
                storage_name = resource_name if "storage" in title else "<STORAGE_ACCOUNT>"
                remediation_scripts.append({
                    "title": "Enforce HTTPS on Azure Storage",
                    "cloud": "Azure",
                    "resource": storage_name,
                    "cli_script": f"""# Enable HTTPS-only traffic
az storage account update \\
  --name {storage_name} \\
  --https-only true \\
  --min-tls-version TLS1_2""",
                    "terraform": f"""resource "azurerm_storage_account" "{storage_name}" {{
  name                      = "{storage_name}"
  enable_https_traffic_only = true
  min_tls_version           = "TLS1_2"
}}"""
                })
                processed_types.add("azure_https")
            
            elif "public gcs" in title and "gcs_public" not in processed_types:
                bucket_name = resource_name if "bucket" in title else "<BUCKET_NAME>"
                remediation_scripts.append({
                    "title": "Remove Public Access from GCS Bucket",
                    "cloud": "GCP",
                    "resource": bucket_name,
                    "cli_script": f"""# Remove public access for allUsers
gsutil iam ch -d allUsers gs://{bucket_name}

# Remove public access for allAuthenticatedUsers
gsutil iam ch -d allAuthenticatedUsers gs://{bucket_name}

# Set uniform bucket-level access
gsutil uniformbucketlevelaccess set on gs://{bucket_name}""",
                    "terraform": f"""resource "google_storage_bucket" "{bucket_name}" {{
  name          = "{bucket_name}"
  location      = "US"
  
  uniform_bucket_level_access = true
  
  # Remove public access
  # Do not include these bindings:
  # iam_binding {{
  #   role = "roles/storage.objectViewer"
  #   members = ["allUsers"]
  # }}
}}"""
                })
                processed_types.add("gcs_public")
            
            elif "versioning" in title and "disabled" in title and "gcs_versioning" not in processed_types:
                bucket_name = resource_name if "bucket" in title else "<BUCKET_NAME>"
                remediation_scripts.append({
                    "title": "Enable Versioning on GCS Bucket",
                    "cloud": "GCP",
                    "resource": bucket_name,
                    "cli_script": f"""# Enable versioning
gsutil versioning set on gs://{bucket_name}

# Verify versioning is enabled
gsutil versioning get gs://{bucket_name}""",
                    "terraform": f"""resource "google_storage_bucket" "{bucket_name}" {{
  name          = "{bucket_name}"
  location      = "US"
  
  versioning {{
    enabled = true
  }}
}}"""
                })
                processed_types.add("gcs_versioning")
        
        logger.info(f"Generated {len(remediation_scripts)} remediation scripts")
        return remediation_scripts
