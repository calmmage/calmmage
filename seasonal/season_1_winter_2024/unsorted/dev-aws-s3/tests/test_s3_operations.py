import pytest
from pathlib import Path
from s3_operations import upload_file, download_file, search_files


@pytest.fixture
def sample_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("This is a test file")
    return file_path


def test_upload_file(sample_file):
    # Test with default object name
    assert upload_file(sample_file) is True

    # Test with custom object name
    assert upload_file(sample_file, "custom/path/test.txt") is True


def test_download_file(tmp_path, sample_file):
    # First upload a file
    assert upload_file(sample_file) is True

    # Test download with default path
    download_path = tmp_path / "downloaded_default.txt"
    assert download_file(sample_file.name, download_path) is True
    assert download_path.exists()
    assert download_path.read_text() == "This is a test file"

    # Test download with custom path
    custom_path = tmp_path / "subdir" / "downloaded_custom.txt"
    assert download_file("custom/path/test.txt", custom_path) is True
    assert custom_path.exists()
    assert custom_path.read_text() == "This is a test file"


def test_search_files(sample_file):
    # Upload some test files
    assert upload_file(sample_file) is True
    assert upload_file(sample_file, "folder1/test1.txt") is True
    assert upload_file(sample_file, "folder1/test2.txt") is True
    assert upload_file(sample_file, "folder2/test3.txt") is True

    # Test search with no prefix (should return all files)
    all_files = search_files()
    assert len(all_files) == 4

    # Test search with prefix
    folder1_files = search_files("folder1/")
    assert len(folder1_files) == 2
    assert all(f['key'].startswith("folder1/") for f in folder1_files)

    # Test search with non-existent prefix
    empty_result = search_files("nonexistent/")
    assert len(empty_result) == 0
