import boto3


def generate_s3_presigned_url(bucket_name, object_key, expiration=3600):
    s3 = boto3.client("s3")
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expiration,
    )
    return url
