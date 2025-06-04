import boto3
from dotenv import load_dotenv
import os

load_dotenv()


def create_bucket():
    # Get credentials from environment
    access_key = os.getenv("S3_ACCESS_KEY_ID")
    secret_key = os.getenv("S3_SECRET_ACCESS_KEY")
    region = os.getenv("S3_REGION", "us-east-1")
    bucket_name = os.getenv("S3_BUCKET_NAME")

    if not all([access_key, secret_key, bucket_name]):
        print("Missing required environment variables:")
        print("- S3_ACCESS_KEY_ID")
        print("- S3_SECRET_ACCESS_KEY")
        print("- S3_BUCKET_NAME")
        return False

    # Create S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket {bucket_name} already exists")
        return True
    except Exception:
        # Bucket doesn't exist, create it
        try:
            if region == "us-east-1":
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": region},
                )
            print(f"✅ Successfully created bucket: {bucket_name}")
            return True
        except Exception as e:
            print(f"❌ Failed to create bucket {bucket_name}: {e}")
            return False


if __name__ == "__main__":
    print("Creating S3 bucket...")
    create_bucket()
