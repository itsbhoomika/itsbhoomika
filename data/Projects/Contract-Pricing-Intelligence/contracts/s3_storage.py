"""
AWS S3 utilities for contract document storage
"""
import boto3
import os
from django.conf import settings


class S3ContractStorage:
    """Handle contract document storage on AWS S3"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    def upload_document(self, contract_id, file_path):
        """
        Upload contract document to S3
        
        Args:
            contract_id: Unique contract identifier
            file_path: Local file path to upload
            
        Returns:
            S3 object path or None if failed
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            file_name = os.path.basename(file_path)
            s3_key = f"contracts/{contract_id}/{file_name}"
            
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                s3_key,
                ExtraArgs={'ContentType': 'application/pdf'}
            )
            
            return s3_key
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return None
    
    def download_document(self, s3_key, local_path):
        """
        Download contract document from S3
        
        Args:
            s3_key: S3 object key
            local_path: Local file path to save to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.s3_client.download_file(
                self.bucket_name,
                s3_key,
                local_path
            )
            return True
        except Exception as e:
            print(f"Error downloading from S3: {e}")
            return False
    
    def get_document_url(self, s3_key, expiration=3600):
        """
        Get a presigned URL for a contract document
        
        Args:
            s3_key: S3 object key
            expiration: URL expiration time in seconds (default 1 hour)
            
        Returns:
            Presigned URL or None
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            print(f"Error generating presigned URL: {e}")
            return None
    
    def list_documents(self, contract_id):
        """
        List all documents for a contract
        
        Args:
            contract_id: Unique contract identifier
            
        Returns:
            List of S3 object keys
        """
        try:
            prefix = f"contracts/{contract_id}/"
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            if 'Contents' not in response:
                return []
            
            return [obj['Key'] for obj in response['Contents']]
        except Exception as e:
            print(f"Error listing documents: {e}")
            return []
    
    def delete_document(self, s3_key):
        """
        Delete a contract document from S3
        
        Args:
            s3_key: S3 object key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except Exception as e:
            print(f"Error deleting from S3: {e}")
            return False
