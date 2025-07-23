from pydantic import SecretStr
from pydantic_settings import BaseSettings
import boto3


class AppConfig(BaseSettings):
    s3_bucket_name: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: SecretStr
    # s3_expiration: int = 3600

    class Config:
        env_prefix = ""
        env_file = ".env"


class App:
    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)
        self._s3_client = None

    @property
    def s3_conn(self):
        if self._s3_client is None:
            self._s3_client = boto3.client(
                "s3",
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key.get_secret_value(),
                region_name=self.config.aws_region,
                # THIS WAS MANDATORY TO MAKE IT WORK
                endpoint_url=f"https://s3.{self.config.aws_region}.amazonaws.com",
            )
        return self._s3_client

    def generate_s3_presigned_url(self, object_key, expiration=3600):
        url = self.s3_conn.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.config.s3_bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return url
