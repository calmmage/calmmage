# Local Job Runner

Scans and executes all jobs in a directory with concurrent execution and live progress updates.

## Job Output Format

Jobs can provide structured status information using these output formats:

### FINAL STATUS
```
🎯 FINAL STATUS: <status> - <optional description>
```

Valid status values:
- `success` - Job completed successfully with meaningful work
- `fail` - Job failed or encountered errors
- `no_change` - Job ran successfully but no changes were made
- `hanging` - Job appears to be stuck or hanging
- `requires_attention` - Job needs manual intervention

Examples:
```bash
echo "🎯 FINAL STATUS: success - Updated 15 files"
echo "🎯 FINAL STATUS: no_change - No files needed updating"
echo "🎯 FINAL STATUS: fail - Missing required environment variable"
```

### FINAL NOTES
```
📝 FINAL NOTES: <descriptive text about what happened>
```

Examples:
```bash
echo "📝 FINAL NOTES: Processed 150 images, 5 had warnings"
echo "📝 FINAL NOTES: Database backup completed to /backups/daily_20250725.sql"
```

## Job Structure

- Jobs are Python files in the configured jobs directory
- Jobs starting with `_` are disabled (skipped unless `--include-disabled`)
- Jobs run from the main project directory with configurable timeout
- Output is captured and analyzed for status parsing and AI summaries

## Usage

```bash
# Run all enabled jobs
python job_runner.py

# Include disabled jobs
python job_runner.py --include-disabled

# Custom jobs directory
python job_runner.py --jobs-dir /path/to/jobs

# Custom log directory
python job_runner.py --log-dir /path/to/logs
```

## Configuration

- **Timeout**: 5 minutes (300 seconds) per job
- **Python executable**: Uses `$CALMMAGE_VENV_PATH/bin/python` if available
- **Logs**: Saved to `~/Library/Logs/CalmmageScheduler/`
- **Concurrency**: All jobs run simultaneously with live progress updates