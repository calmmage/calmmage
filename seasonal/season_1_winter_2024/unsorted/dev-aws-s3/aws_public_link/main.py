import os
from lib import App
from dotenv import load_dotenv

load_dotenv()

app = App()

object_key = os.getenv("S3_OBJECT_KEY")

url = app.generate_s3_presigned_url(object_key=object_key, expiration=3600)


print(url)

# debugging

# response = app.s3_conn.get_bucket_policy(Bucket=app.config.s3_bucket_name)
# print(response['Policy'])
