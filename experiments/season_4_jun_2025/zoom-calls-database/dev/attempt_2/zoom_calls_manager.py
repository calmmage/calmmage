from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional
import boto3
from dotenv import load_dotenv
from datetime import datetime


class ZoomCall(BaseModel):
    # parsed info
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    chat_logs: Optional[str] = None
    ai_transcript: Optional[str] = None
    ai_summary: Optional[str] = None

    # metadata
    call_date: Optional[datetime] = None
    name: str

    # raw data
    _s3_video_key: Optional[str] = None
    _s3_audio_key: Optional[str] = None
    _video_path: Optional[Path] = None
    _audio_path: Optional[Path] = None


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

    #     def _upload_zoom_calls(self, zoom_calls: list[ZoomCall]):
    #         """Upload a bunch of zoom call records to Airtable with S3 tracking"""
    #         for call in zoom_calls:
    #             # Prepare basic data
    #             data = {
    #                 "AI Summary": call.ai_summary,
    #             }

    #             # Prepare _data field with S3 keys for URL refresh
    #             s3_data = {}

    #             # Upload video to S3 and get URL
    #             if call._video_path:
    #                 video_key = self._upload_to_s3(call._video_path)
    #                 video_url = self._get_s3_presigned_url(video_key)
    #                 data["Video URL"] = video_url
    #                 s3_data["video_s3_key"] = video_key

    #             # Upload audio to S3 and get URL
    #             if call._audio_path:
    #                 audio_key = self._upload_to_s3(call._audio_path)
    #                 audio_url = self._get_s3_presigned_url(audio_key)
    #                 data["Audio URL"] = audio_url
    #                 s3_data["audio_s3_key"] = audio_key

    #             # Store S3 keys in _data field for future URL refreshing
    #             data["_data"] = json.dumps(s3_data)

    #             # Create record first
    #             record = self._write_to_airtable(data)
    #             record_id = record['id']

    #             # Upload attachments directly (different files)
    #             if call.ai_transcript:
    #                 # Create temporary transcript file
    #                 import tempfile
    #                 with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    #                     f.write(call.ai_transcript)
    #                     transcript_path = Path(f.name)

    #                 try:
    #                     self._upload_file_to_airtable(record_id, "AI Transcript", transcript_path)
    #                 finally:
    #                     transcript_path.unlink(missing_ok=True)

    #             if call.chat_logs:
    #                 # Create temporary chat file
    #                 import tempfile
    #                 with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    #                     f.write(call.chat_logs)
    #                     chat_path = Path(f.name)

    #                 try:
    #                     self._upload_file_to_airtable(record_id, "Chat", chat_path)
    #                 finally:
    #                     chat_path.unlink(missing_ok=True)

    #     def _get_airtable_schema(self):
    #         """Get and display the Airtable table schema"""
    #         try:
    #             schema = self.airtable_table.schema()
    #             print("\n📋 Airtable Table Schema:")
    #             print(f"Table Name: {schema.name}")
    #             print("Fields:")
    #             for field in schema.fields:
    #                 print(f"  - {field.name}: {field.type}")
    #                 # Only show options for field types that have them
    #                 if hasattr(field, '__dict__') and 'options' in field.__dict__:
    #                     print(f"    Options: {field.__dict__['options']}")
    #             return schema
    #         except Exception as e:
    #             print(f"Failed to get Airtable schema: {e}")
    #             return None

    #     def _upload_file_to_airtable(self, record_id: str, field_name: str, file_path: Path):
    #         """Upload a file directly to Airtable using the upload_attachment method"""
    #         try:
    #             result = self.airtable_table.upload_attachment(
    #                 record_id=record_id,
    #                 field=field_name,
    #                 filename=str(file_path)
    #             )
    #             print(f"Successfully uploaded {file_path} directly to Airtable field '{field_name}'")
    #             return result
    #         except Exception as e:
    #             print(f"Failed to upload {file_path} directly to Airtable: {e}")
    #             raise

    #     def _debug_aws_config(self):
    #         """Debug AWS configuration to help troubleshoot credentials"""
    #         print("🔍 AWS Configuration Debug:")
    #         print(f"  Access Key ID: {self.config.s3_access_key_id}")
    #         print(f"  Region: {self.config.s3_region}")
    #         print(f"  Bucket: {self.config.s3_bucket_name}")
    #         print(f"  Secret Key: {'*' * len(self.config.s3_secret_access_key)}...")

    #         # Test basic S3 connection
    #         try:
    #             response = self.s3_conn.list_buckets()
    #             print(f"  ✅ S3 Connection: Can list {len(response['Buckets'])} buckets")
    #         except Exception as e:
    #             print(f"  ❌ S3 Connection Failed: {e}")
    #             print("  💡 Check your AWS credentials in .env file:")
    #             print("     - S3_ACCESS_KEY_ID")
    #             print("     - S3_SECRET_ACCESS_KEY")
    #             print("     - S3_REGION")

    #     def check_connections(self):
    #         print("🔧 Testing connections independently...")

    #         # Test AWS configuration first
    #         self._debug_aws_config()

    #         # Test Airtable connection independently
    #         print("\n📋 Testing Airtable connection...")
    #         try:
    #             schema = self._get_airtable_schema()
    #             if schema:
    #                 print(f"  ✅ Airtable Connected: Table '{schema.name}' found")

    #                 # Find attachment fields
    #                 attachment_fields = []
    #                 for field in schema.fields:
    #                     if field.type == 'multipleAttachments':
    #                         attachment_fields.append(field.name)
    #                         print(f"  📎 Found attachment field: {field.name}")

    #                 if not attachment_fields:
    #                     print("  ⚠️  No attachment fields found - check your table schema")

    #             else:
    #                 print("  ❌ Failed to get Airtable schema")
    #                 return
    #         except Exception as e:
    #             print(f"  ❌ Airtable connection failed: {e}")
    #             return

    #         # Test Airtable record creation and file upload (independent of S3)
    #         print("\n📝 Testing Airtable record creation...")
    #         try:
    #             # Create a simple record first
    #             basic_data = {
    #                 "Name": "Test Record - Direct Upload",
    #                 "AI Summary": "Testing direct file upload to Airtable",
    #                 "_data": json.dumps({"test": True})
    #             }

    #             record = self._write_to_airtable(basic_data)
    #             record_id = record['id']
    #             print(f"  ✅ Record created: {record_id}")

    #             # Test direct file uploads (completely independent of S3)
    #             print("\n📎 Testing direct file uploads to Airtable...")

    #             # Create test files
    #             transcript_file = Path("test_transcript.txt")
    #             transcript_file.write_text("""
    # ZOOM CALL TRANSCRIPT
    # ====================
    # [00:00] Alice: Hello everyone, welcome to today's meeting
    # [00:15] Bob: Thanks for organizing this Alice
    # [00:30] Carol: Happy to be here
    # [00:45] Alice: Let's start with the agenda...
    # [01:00] Bob: The project is on track, 80% complete
    # [01:30] Carol: QA testing is scheduled for next week
    # [02:00] Alice: Any blockers to discuss?
    # [02:15] Bob: Need approval for the deployment window
    # [02:30] Carol: I'll follow up with the stakeholders
    # [02:45] Alice: Great! Meeting recording will be shared
    # """)

    #             chat_file = Path("test_chat.txt")
    #             chat_file.write_text("""
    # ZOOM CHAT LOG
    # =============
    # [00:05] Bob: Can everyone hear me ok?
    # [00:20] Carol: Audio is clear 👍
    # [00:35] Alice: Perfect, let's get started
    # [01:15] Bob: Sharing project dashboard link: https://dashboard.company.com
    # [01:45] Carol: Thanks! Very helpful
    # [02:00] Alice: @everyone please review the specs before Friday
    # [02:30] Bob: Will do!
    # [02:35] Carol: Already on my calendar 📅
    # [02:50] Alice: Thanks team, great session!
    # """)

    #             # Upload files directly to Airtable attachment fields
    #             uploaded_count = 0

    #             if "AI Transcript" in attachment_fields:
    #                 try:
    #                     print("  📎 Uploading transcript...")
    #                     result = self._upload_file_to_airtable(record_id, "AI Transcript", transcript_file)
    #                     print(f"  ✅ Transcript uploaded successfully")
    #                     uploaded_count += 1
    #                 except Exception as e:
    #                     print(f"  ❌ Transcript upload failed: {e}")

    #             if "Chat" in attachment_fields:
    #                 try:
    #                     print("  📎 Uploading chat log...")
    #                     result = self._upload_file_to_airtable(record_id, "Chat", chat_file)
    #                     print(f"  ✅ Chat uploaded successfully")
    #                     uploaded_count += 1
    #                 except Exception as e:
    #                     print(f"  ❌ Chat upload failed: {e}")

    #             print(f"\n🎉 Successfully uploaded {uploaded_count} files to Airtable!")

    #             # Verify by reading the record back
    #             updated_record = self.airtable_table.get(record_id)
    #             fields = updated_record.get('fields', {})

    #             for field_name in attachment_fields:
    #                 if field_name in fields and fields[field_name]:
    #                     attachments = fields[field_name]
    #                     print(f"  📎 {field_name}: {len(attachments)} file(s) attached")
    #                     for i, attachment in enumerate(attachments):
    #                         filename = attachment.get('filename', 'unknown')
    #                         size = attachment.get('size', 0)
    #                         print(f"    {i+1}. {filename} ({size} bytes)")

    #             # Clean up test files
    #             transcript_file.unlink(missing_ok=True)
    #             chat_file.unlink(missing_ok=True)

    #         except Exception as e:
    #             print(f"  ❌ Airtable test failed: {e}")
    #             import traceback
    #             traceback.print_exc()

    #         # Only test S3 if credentials are working
    #         print("\n☁️ Testing S3 (optional)...")
    #         try:
    #             sample_file = Path("dummy_file.txt")
    #             sample_file.write_text("This is a test file for S3 upload")

    #             if not self._create_s3_bucket():
    #                 print("  ⚠️  S3 bucket creation failed - check AWS permissions")
    #                 return

    #             res = self._upload_to_s3(sample_file)
    #             print(f"  ✅ S3 upload successful: {res}")

    #             presigned_url = self._get_s3_presigned_url(res)
    #             print(f"  ✅ Presigned URL generated (length: {len(presigned_url)})")

    #             sample_file.unlink(missing_ok=True)

    #         except Exception as e:
    #             print(f"  ❌ S3 test failed: {e}")
    #             print("  💡 S3 is optional - Airtable direct uploads work without it!")

    #         print("\n✅ Connection tests completed!")

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
#     @property
#     def airtable_conn(self):
#         if self._airtable_api is None:
#             self._airtable_api = Api(self.config.airtable_pat.get_secret_value())
#         return self._airtable_api

#     @property
#     def airtable_table(self):
#         if self._airtable_table is None:
#             base = self.airtable_conn.base(self.config.airtable_base_id)
#             self._airtable_table = base.table(self.config.airtable_table_id)
#         return self._airtable_table

#     def _write_to_airtable(self, data: dict):
#         """
#         Write data to Airtable
#         field_descriptions = {
#             "Name": "A text field to store the name or title of the Zoom call.",
#             "_data": "A field (type unclear from UI) for internal metadata or computed data.",
#             "Call Date": "A date field to store the date of the Zoom call.",
#             "Video URL": "A URL field to store the link to the Zoom call video recording.",
#             "Audio URL": "A URL field to store the link to the Zoom call audio recording.",
#             "AI Transcript": "An attachment or text field to store the AI-generated transcript of the call.",
#             "AI Summary": "A field (type unclear from UI) to store an AI-generated summary of the call.",
#             "Chat": "An attachment or text field to store the chat log from the Zoom call."
#         }
#         """
#         try:
#             record = self.airtable_table.create(data)
#             print(f"Successfully created Airtable record: {record['id']}")
#             return record
#         except Exception as e:
#             print(f"Failed to write to Airtable: {e}")
#             raise

#     def _read_from_airtable(self):
#         """Read all records from Airtable"""
#         try:
#             records = self.airtable_table.all()
#             print(f"Successfully read {len(records)} records from Airtable")
#             return records
#         except Exception as e:
#             print(f"Failed to read from Airtable: {e}")
#             raise

#     def _find_in_airtable(self, **kwargs):
#         """Find records in Airtable based on field values"""
#         try:
#             records = self.airtable_table.all()
#             matching_records = []

#             for record in records:
#                 fields = record.get('fields', {})
#                 match = True

#                 for key, value in kwargs.items():
#                     # Convert key to proper field name (capitalize first letter)
#                     field_name = key.replace('_', ' ').title()
#                     if field_name == 'Name':
#                         field_name = 'Name'

#                     if fields.get(field_name) != value:
#                         match = False
#                         break

#                 if match:
#                     matching_records.append(record)

#             print(f"Found {len(matching_records)} matching records in Airtable")
#             return matching_records
#         except Exception as e:
#             print(f"Failed to search Airtable: {e}")
#             raise

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

    zcm.check_connections()
