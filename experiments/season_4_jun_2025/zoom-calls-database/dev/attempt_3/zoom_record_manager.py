from datetime import datetime
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional, List
from tqdm import tqdm

# import boto3
from pyairtable import Api
from pyairtable.api.types import RecordDict
from dotenv import load_dotenv

# import json
from google_drive_utils import get_client
from zoom_record import ZoomRecord
from loguru import logger

# from dev.zoom_records_discovery.main import create_zoom_record
from discover_zoom_records import get_zoom_records


# class DummyRecord(BaseModel):
#     # parsed info
#     name: str
#     large_file_url: Optional[str] = None
#     small_file: Optional[Path] = None
#     text_field: Optional[str] = None

#     # raw data
#     _s3_large_file_key: Optional[str] = None
#     _large_file_path: Optional[Path] = None


class ZoomRecordManagerConfig(BaseSettings):
    # airtable settings
    airtable_pat: SecretStr
    airtable_base_id: str
    airtable_table_id: str

    # s3 settings
    # s3_bucket_name: str
    # aws_region: str
    # aws_access_key_id: str
    # aws_secret_access_key: SecretStr

    path_to_zoom_records: Path

    google_drive_client_secrets_file: Path
    google_drive_credentials_file: Path

    class Config:
        env_prefix = ""
        env_file = ".env"


class ZoomRecordManager:
    def __init__(self, **kwargs):
        self.config = ZoomRecordManagerConfig(**kwargs)
        # self._s3_client = None
        self._airtable_api = None
        self._airtable_table = None
        self._google_drive_client = None

    def main(self):
        # step 1: discover zoom records
        records = get_zoom_records(self.config.path_to_zoom_records)

        existing_records = {
            record.name: record for record in self._read_from_airtable()
        }

        # step 2: create zoom records
        to_write = []
        for name, record in tqdm(records.items()):
            # check if record already exists in airtable
            if name in existing_records:
                logger.info(f"Record {name} already exists in airtable")
                continue

            try:
                zoom_record = self.create_zoom_record(name=name, **record)

                # step 3: upload files to google drive
                # to_write.append(zoom_record)
                self._write_to_airtable(zoom_record)
            except Exception as e:
                logger.error(f"Failed to write {name} to airtable: {e}")
                continue

            # time.sleep(0.1)

        # self.bulk_write_to_airtable(to_write)

    def bulk_write_to_airtable(self, records: List[ZoomRecord]):
        # bulk write to airtable
        items = []

        for record in records:
            items.append(self._prepare_airtable_record(record))

        return self.airtable_table.batch_create(items)

    def create_zoom_record(
        self,
        name: str,
        date: datetime,
        video: Path,
        audio: Optional[Path] = None,
        chat_logs: Optional[Path] = None,
        transcript: Optional[Path] = None,
    ) -> ZoomRecord:
        record = ZoomRecord(
            name=name,
            _video_path=video,
            _audio_path=audio,
            _chat_logs_path=chat_logs,
            _transcript_path=transcript,
            date=date,
        )

        # now, i need to get Google Drive URLs for the files (they are already in Drive)
        record.video_url = self._get_google_drive_url(video)
        if audio:
            record.audio_url = self._get_google_drive_url(audio)
        if chat_logs:
            record.chat_logs_url = self._get_google_drive_url(chat_logs)
        if transcript:
            record.transcript_url = self._get_google_drive_url(transcript)

        return record

    # ---------------------------
    # Google Drive
    # ---------------------------

    @property
    def google_drive_client(self):
        if self._google_drive_client is None:
            self._google_drive_client = get_client(
                self.config.google_drive_client_secrets_file,
                self.config.google_drive_credentials_file,
            )
        return self._google_drive_client

    def _get_google_drive_url(self, file_path: Path):
        from google_drive_utils import find_file

        file = find_file(file_path.name, self.google_drive_client)
        assert file is not None, f"File {file_path.name} not found in Google Drive"
        return file["alternateLink"]

    # def main(self,
    #          name = "Test Dummy Record",
    #          large_file = Path(__file__).parent / "dummy_file.txt",
    #          small_file = Path(__file__).parent / "dummy_file.txt",
    #          text_field = "This is a test dummy record"
    #          ):
    #     # based on that, create DummyRecord object
    #     dummy_record = DummyRecord(
    #         name=name,
    #         small_file=small_file,
    #         text_field=text_field,
    #         _large_file_path=large_file,
    #     )

    #     # then upload it to s3
    #     large_file_key = self._upload_to_s3(large_file)
    #     dummy_record._s3_large_file_key = large_file_key

    #     large_file_url = self._generate_presigned_s3_url(large_file_key)
    #     dummy_record.large_file_url = large_file_url

    #     self._write_to_airtable(dummy_record)
    #     # then upload it to airtable

    # ---------------------------
    # AWS S3
    # ---------------------------

    # def _upload_to_s3(self, file: Path) -> str:
    #     """Upload file to S3 and return the object key"""
    #     object_key = file.name
    #     try:
    #         self.s3_conn.upload_file(
    #             str(file),
    #             self.config.s3_bucket_name,
    #             object_key
    #         )
    #         print(f"Successfully uploaded {file} to S3 as {object_key}")
    #         return object_key
    #     except Exception as e:
    #         print(f"Failed to upload {file} to S3: {e}")
    #         raise

    # def _create_s3_bucket(self) -> bool:
    #     """Create S3 bucket if it doesn't exist"""
    #     try:
    #         # Check if bucket exists
    #         self.s3_conn.head_bucket(Bucket=self.config.s3_bucket_name)
    #         print(f"Bucket {self.config.s3_bucket_name} already exists")
    #         return True
    #     except Exception:
    #         # Bucket doesn't exist, create it
    #         try:
    #             if self.config.aws_region == 'us-east-1':
    #                 # us-east-1 doesn't need LocationConstraint
    #                 self.s3_conn.create_bucket(Bucket=self.config.s3_bucket_name)
    #             else:
    #                 # Other regions need LocationConstraint
    #                 self.s3_conn.create_bucket(
    #                     Bucket=self.config.s3_bucket_name,
    #                     CreateBucketConfiguration={'LocationConstraint': self.config.aws_region}
    #                 )
    #             print(f"Successfully created bucket: {self.config.s3_bucket_name}")
    #             return True
    #         except Exception as e:
    #             print(f"Failed to create bucket {self.config.s3_bucket_name}: {e}")
    #             return False

    # @property
    # def s3_conn(self):
    #     if self._s3_client is None:
    #         self._s3_client = boto3.client(
    #             's3',
    #             aws_access_key_id=self.config.aws_access_key_id,
    #             aws_secret_access_key=self.config.aws_secret_access_key.get_secret_value(),
    #             region_name=self.config.aws_region,
    #             # THIS WAS MANDATORY TO MAKE IT WORK
    #             endpoint_url=f'https://s3.{self.config.aws_region}.amazonaws.com'
    #         )
    #     return self._s3_client

    # def _generate_presigned_s3_url(
    #         self,
    #         object_key,
    #         expiration=3600 # max 12 hours
    #         ):

    #     url = self.s3_conn.generate_presigned_url(
    #         ClientMethod='get_object',
    #         Params={'Bucket': self.config.s3_bucket_name, 'Key': object_key},
    #         ExpiresIn=expiration
    #     )
    #     return url

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

    def _prepare_airtable_record(self, record: ZoomRecord) -> dict:
        return {
            "Name": record.name,
            "Date": record.date.strftime("%Y-%m-%d"),
            "Video URL": record.video_url,
            "Audio URL": record.audio_url,
            "Chat Logs URL": record.chat_logs_url,
            "Transcript URL": record.transcript_url,
            "AI Transcript": record.ai_transcript,
        }

    def _write_to_airtable(self, record: ZoomRecord) -> RecordDict:
        data = self._prepare_airtable_record(record)
        item = self.airtable_table.create(data)
        logger.debug(f"Successfully wrote {record.name} to Airtable")
        return item

    # def _write_to_airtable(self, dummy_record: DummyRecord):
    #     """Write dummy record to airtable"""
    #     # data = dummy_record.model_dump()

    #     data = {
    #         "Name": dummy_record.name,
    #         "Large File URL": dummy_record.large_file_url,
    #         # "Small File": dummy_record.small_file,
    #         "Text Field": dummy_record.text_field,
    #         "_data": json.dumps({
    #             "_s3_large_file_key": dummy_record._s3_large_file_key,
    #             "_large_file_path": dummy_record._large_file_path
    #         })
    #     }

    #     record = self.airtable_table.create(data)

    #     # upload attachment to airtable separately
    #     if dummy_record.small_file:
    #         self._upload_file_to_airtable(record["id"], "Small File", dummy_record.small_file)

    def _upload_file_to_airtable(
        self, record_id: str, field_name: str, file_path: Path
    ):
        """Upload a file directly to Airtable using the upload_attachment method"""
        try:
            result = self.airtable_table.upload_attachment(
                record_id=record_id, field=field_name, filename=str(file_path)
            )
            logger.info(
                f"Successfully uploaded {file_path} directly to Airtable field '{field_name}'"
            )
            return result
        except Exception as e:
            logger.error(f"Failed to upload {file_path} directly to Airtable: {e}")
            raise

    def _read_from_airtable(self) -> List[ZoomRecord]:
        """Read all records from Airtable"""
        try:
            items = self.airtable_table.all()

            records = []
            for item in items:
                record = ZoomRecord(
                    **{
                        key.lower().replace(" ", "_"): value
                        for key, value in item["fields"].items()
                    }
                )
                records.append(record)

            logger.debug(f"Successfully read {len(records)} records from Airtable")
            return records
        except Exception as e:
            logger.error(f"Failed to read from Airtable: {e}")
            raise

    # def _find_in_airtable(self, **kwargs):
    #     """Find records in Airtable based on field values"""
    #     try:
    #         records = self.airtable_table.all()
    #         matching_records = []

    #         for record in records:
    #             fields = record.get('fields', {})
    #             match = True

    #             for key, value in kwargs.items():
    #                 # Convert key to proper field name (capitalize first letter)
    #                 field_name = key.replace('_', ' ').title()
    #                 if field_name == 'Name':
    #                     field_name = 'Name'

    #                 if fields.get(field_name) != value:
    #                     match = False
    #                     break

    #             if match:
    #                 matching_records.append(record)

    #         print(f"Found {len(matching_records)} matching records in Airtable")
    #         return matching_records
    #     except Exception as e:
    #         print(f"Failed to search Airtable: {e}")
    #         raise


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

    zcm = ZoomRecordManager()

    # zcm.check_connections()
    zcm.main()
