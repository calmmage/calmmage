import boto3

session = boto3.Session()
creds = session.get_credentials()
print(f"Access Key: {creds.access_key}")
if creds.access_key != "AKIA2BZMXWJQQUV3Y77E":
    print("Credentials mismatch! Update ~/.aws/credentials or environment variables.")
else:
    # s3 = boto3.client('s3', region_name='eu-north-1')
    # url = s3.generate_presigned_url(
    #     ClientMethod='get_object',
    #     Params={'Bucket': 'dev-zoom-calls-database', 'Key': 'dummy_file.txt'},
    #     ExpiresIn=3600
    # )
    # print("Pre-signed URL:", url)
    import boto3

    s3 = boto3.client(
        "s3",
        region_name="eu-north-1",
        endpoint_url="https://s3.eu-north-1.amazonaws.com",
    )
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": "dev-zoom-calls-database", "Key": "dummy_file.txt"},
        ExpiresIn=3600,
    )
    print("Pre-signed URL:", url)
