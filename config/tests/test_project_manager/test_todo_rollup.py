from datetime import datetime, timedelta

from freezegun import freeze_time


def test_rollup_excludes_today(
    sample_project_dir, sample_todos, pm_with_custom_editor, pm_config
):
    """Test that rollup excludes today's todo file"""
    # Run rollup
    result = pm_with_custom_editor.rollup_todos(sample_project_dir)

    # Check that rolled up file was created
    assert result is not None
    assert result.exists()

    # Check that today's file still exists
    today = datetime.now()
    today_file = sample_todos / today.strftime(pm_config.todo_filename_template)
    assert today_file.exists(), "Today's todo file should not be rolled up"

    # Check content of rolled up file
    content = result.read_text()
    assert (
        "Today's task" not in content
    ), "Today's tasks should not be in rolled up content"
    assert (
        "Yesterday's task" in content
    ), "Yesterday's tasks should be in rolled up content"
    assert (
        "Task from 2 days ago" in content
    ), "Older tasks should be in rolled up content"


def test_rollup_preserves_existing_todo_md(
    sample_project_dir, sample_todos, pm_with_custom_editor
):
    """Test that rollup preserves existing todo.md content"""
    # Create existing todo.md
    existing_content = "# Existing todos\n\n- Old task\n"
    todo_md = sample_todos / "todo.md"
    todo_md.write_text(existing_content)

    # Run rollup
    result = pm_with_custom_editor.rollup_todos(sample_project_dir)

    # Check that existing content is preserved
    content = result.read_text()
    assert existing_content in content, "Existing todo.md content should be preserved"
    assert "Yesterday's task" in content, "New content should be added"


def test_rollup_with_custom_date(sample_project_dir, pm_with_custom_editor, pm_config):
    """Test rollup with custom date to simulate historical work"""
    dev_dir = sample_project_dir / pm_config.todo_subfolder
    dev_dir.mkdir(parents=True, exist_ok=True)

    # Create todos with custom dates
    base_date = datetime(2024, 1, 15)  # Fixed date for testing

    def create_todo_at(days_offset: int, content: str):
        date = base_date + timedelta(days=days_offset)
        filename = date.strftime(pm_config.todo_filename_template)
        (dev_dir / filename).write_text(content)
        return filename

    # Create sample todos
    create_todo_at(-2, "- Old task")
    create_todo_at(-1, "- Recent task")
    create_todo_at(0, "- Current task")

    # Run rollup (simulating running on the base date)
    with freeze_time(base_date):
        result = pm_with_custom_editor.rollup_todos(sample_project_dir)

    # Verify results
    assert result is not None
    content = result.read_text()
    assert "Current task" not in content
    assert "Recent task" in content
    assert "Old task" in content


# def test_new_todo_with_rollup(
#     sample_project_dir, sample_todos, pm_with_custom_editor, monkeypatch, pm_config, mock_pd_config
# ):
#     """Test that new-todo command triggers rollup"""
#
#     # Mock ProjectDiscoverer
#     class MockProjectDiscoverer:
#         def __init__(self):
#             self.config = MockProjectDiscovererConfig.from_yaml(None)
#
#         def get_current_project(self):
#             return sample_project_dir
#
#         def quick_search(self, *args, **kwargs):
#             return [sample_project_dir]
#
#     # Mock show_result_menu
#     def mock_show_result_menu(*args, **kwargs):
#         return sample_project_dir
#
#     # Apply mocks before importing
#     monkeypatch.setattr("dev_env.tools.project_manager.pm_cli.pd", MockProjectDiscoverer())
#     monkeypatch.setattr(
#         "dev_env.tools.project_manager.pm_cli.show_result_menu", mock_show_result_menu
#     )
#     monkeypatch.setattr("dev_env.tools.project_manager.pm_cli.pm", pm_with_custom_editor)
#
#     # Now import the CLI app
#     from tools.project_manager.pm_cli import app
#     from typer.testing import CliRunner
#
#     runner = CliRunner()
#
#     # Run new-todo command through the app
#     result = runner.invoke(app, ["new-todo", "--text", "New task"])
#
#     assert result.exit_code == 0, f"Command failed with: {result.stdout}"
#
#     # Check that rollup happened
#     todo_md = sample_todos / "todo.md"
#     assert todo_md.exists()
#     content = todo_md.read_text()
#     assert "Yesterday's task" in content
#     assert "Task from 2 days ago" in content
#
#     # Check that today's file was created with new task
#     today = datetime.now()
#     today_file = sample_todos / today.strftime(pm_config.todo_filename_template)
#     assert today_file.exists()
#     assert "New task" in today_file.read_text()
