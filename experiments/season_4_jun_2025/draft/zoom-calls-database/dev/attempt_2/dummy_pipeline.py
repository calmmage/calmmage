from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional
import boto3
from pyairtable import Api
from dotenv import load_dotenv
import json


class DummyRecord(BaseModel):
    # parsed info
    name: str
    large_file_url: Optional[str] = None
    small_file: Optional[Path] = None
    text_field: Optional[str] = None

    # raw data
    _s3_large_file_key: Optional[str] = None
    _large_file_path: Optional[Path] = None


class ZoomCallManagerConfig(BaseSettings):
    # airtable settings
    airtable_pat: SecretStr
    airtable_base_id: str
    airtable_table_id: str

    # s3 settings
    s3_bucket_name: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: SecretStr

    class Config:
        env_prefix = ""
        env_file = ".env"


class ZoomCallManager:
    def __init__(self, **kwargs):
        self.config = ZoomCallManagerConfig(**kwargs)
        self._s3_client = None
        self._airtable_api = None
        self._airtable_table = None

    def main(
        self,
        name="Test Dummy Record",
        large_file=Path(__file__).parent / "dummy_file.txt",
        small_file=Path(__file__).parent / "dummy_file.txt",
        text_field="This is a test dummy record",
    ):
        # based on that, create DummyRecord object
        dummy_record = DummyRecord(
            name=name,
            small_file=small_file,
            text_field=text_field,
            _large_file_path=large_file,
        )

        # then upload it to s3
        large_file_key = self._upload_to_s3(large_file)
        dummy_record._s3_large_file_key = large_file_key

        large_file_url = self._generate_presigned_s3_url(large_file_key)
        dummy_record.large_file_url = large_file_url

        self._write_to_airtable(dummy_record)
        # then upload it to airtable

    # ---------------------------
    # AWS S3
    # ---------------------------

    def _upload_to_s3(self, file: Path) -> str:
        """Upload file to S3 and return the object key"""
        object_key = file.name
        try:
            self.s3_conn.upload_file(str(file), self.config.s3_bucket_name, object_key)
            print(f"Successfully uploaded {file} to S3 as {object_key}")
            return object_key
        except Exception as e:
            print(f"Failed to upload {file} to S3: {e}")
            raise

    def _create_s3_bucket(self) -> bool:
        """Create S3 bucket if it doesn't exist"""
        try:
            # Check if bucket exists
            self.s3_conn.head_bucket(Bucket=self.config.s3_bucket_name)
            print(f"Bucket {self.config.s3_bucket_name} already exists")
            return True
        except Exception:
            # Bucket doesn't exist, create it
            try:
                if self.config.aws_region == "us-east-1":
                    # us-east-1 doesn't need LocationConstraint
                    self.s3_conn.create_bucket(Bucket=self.config.s3_bucket_name)
                else:
                    # Other regions need LocationConstraint
                    self.s3_conn.create_bucket(
                        Bucket=self.config.s3_bucket_name,
                        CreateBucketConfiguration={
                            "LocationConstraint": self.config.aws_region
                        },
                    )
                print(f"Successfully created bucket: {self.config.s3_bucket_name}")
                return True
            except Exception as e:
                print(f"Failed to create bucket {self.config.s3_bucket_name}: {e}")
                return False

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

    def _generate_presigned_s3_url(
        self,
        object_key,
        expiration=3600,  # max 12 hours
    ):
        url = self.s3_conn.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.config.s3_bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return url

    #     # ---------------------------
    #     # Airtable
    #     # ---------------------------
    @property
    def airtable_conn(self):
        if self._airtable_api is None:
            self._airtable_api = Api(self.config.airtable_pat.get_secret_value())
        return self._airtable_api

    @property
    def airtable_table(self):
        if self._airtable_table is None:
            base = self.airtable_conn.base(self.config.airtable_base_id)
            self._airtable_table = base.table(self.config.airtable_table_id)
        return self._airtable_table

    def _write_to_airtable(self, dummy_record: DummyRecord):
        """Write dummy record to airtable"""
        # data = dummy_record.model_dump()

        data = {
            "Name": dummy_record.name,
            "Large File URL": dummy_record.large_file_url,
            # "Small File": dummy_record.small_file,
            "Text Field": dummy_record.text_field,
            "_data": json.dumps(
                {
                    "_s3_large_file_key": dummy_record._s3_large_file_key,
                    "_large_file_path": dummy_record._large_file_path,
                }
            ),
        }

        record = self.airtable_table.create(data)

        # upload attachment to airtable separately
        if dummy_record.small_file:
            self._upload_file_to_airtable(
                record["id"], "Small File", dummy_record.small_file
            )

    def _upload_file_to_airtable(
        self, record_id: str, field_name: str, file_path: Path
    ):
        """Upload a file directly to Airtable using the upload_attachment method"""
        try:
            result = self.airtable_table.upload_attachment(
                record_id=record_id, field=field_name, filename=str(file_path)
            )
            print(
                f"Successfully uploaded {file_path} directly to Airtable field '{field_name}'"
            )
            return result
        except Exception as e:
            print(f"Failed to upload {file_path} directly to Airtable: {e}")
            raise

    def _read_from_airtable(self):
        """Read all records from Airtable"""
        try:
            records = self.airtable_table.all()
            print(f"Successfully read {len(records)} records from Airtable")
            return records
        except Exception as e:
            print(f"Failed to read from Airtable: {e}")
            raise

    def _find_in_airtable(self, **kwargs):
        """Find records in Airtable based on field values"""
        try:
            records = self.airtable_table.all()
            matching_records = []

            for record in records:
                fields = record.get("fields", {})
                match = True

                for key, value in kwargs.items():
                    # Convert key to proper field name (capitalize first letter)
                    field_name = key.replace("_", " ").title()
                    if field_name == "Name":
                        field_name = "Name"

                    if fields.get(field_name) != value:
                        match = False
                        break

                if match:
                    matching_records.append(record)

            print(f"Found {len(matching_records)} matching records in Airtable")
            return matching_records
        except Exception as e:
            print(f"Failed to search Airtable: {e}")
            raise


#     def _refresh_airtable_s3_links(self):
#         """
#         Refresh S3 presigned URLs for all Airtable records.
#         Assumes S3 object keys are stored in _data field as JSON.
#         """
#         print("🔄 Refreshing S3 URLs for all Airtable records...")

#         # Get all records
#         all_records = self._read_from_airtable()
#         updated_count = 0

#         for record in all_records:
#             record_id = record['id']
#             fields = record.get('fields', {})

#             # Parse _data field to get S3 object keys
#             data_json = fields.get('_data', '{}')
#             try:
#                 data = json.loads(data_json) if isinstance(data_json, str) else {}
#             except json.JSONDecodeError:
#                 data = {}

#             # Check if we have S3 object keys stored
#             video_s3_key = data.get('video_s3_key')
#             audio_s3_key = data.get('audio_s3_key')

#             updates = {}

#             # Generate new presigned URLs if we have S3 keys
#             if video_s3_key:
#                 try:
#                     new_video_url = self._get_s3_presigned_url(video_s3_key)
#                     updates["Video URL"] = new_video_url
#                     print(f"  📹 Updated video URL for record {record_id}")
#                 except Exception as e:
#                     print(f"  ❌ Failed to update video URL for {record_id}: {e}")

#             if audio_s3_key:
#                 try:
#                     new_audio_url = self._get_s3_presigned_url(audio_s3_key)
#                     updates["Audio URL"] = new_audio_url
#                     print(f"  🔊 Updated audio URL for record {record_id}")
#                 except Exception as e:
#                     print(f"  ❌ Failed to update audio URL for {record_id}: {e}")

#             # Update the record if we have changes
#             if updates:
#                 try:
#                     self.airtable_table.update(record_id, updates)
#                     updated_count += 1
#                 except Exception as e:
#                     print(f"  ❌ Failed to update record {record_id}: {e}")

#         print(f"✅ Refreshed URLs for {updated_count} records")
#         return updated_count


if __name__ == "__main__":
    load_dotenv()

    zcm = ZoomCallManager()

    # zcm.check_connections()
    zcm.main()
