# Local Job Runner - Job Ideas

## Philosophy
Simple housekeeping tasks that run daily on startup to ensure everything is healthy and organized. Focus on:
- **Quick checks** (services running, repo status)
- **Safe operations** (dry-run first, careful with commits)
- **File organization** (cleanup, sorting, backup)
- **Health monitoring** (what needs attention?)

---

## 🏠 System & Service Management (Local Jobs)

### 1. Docker Health Check
- **Purpose**: Ensure Docker is running for development
- **Actions**:
    - Check if Docker daemon is running
    - Start if stopped
    - Report container status (running/stopped/errors)
- **Safety**: Read-only checks mostly
- **Frequency**: Daily startup

### 2. Cronicle Health Check
- **Purpose**: Ensure Cronicle scheduler is available
- **Actions**:
    - Check if Cronicle is running (ping API)
    - Report job queue status
    - Alert if any jobs failed recently
- **Safety**: Read-only API calls
- **Frequency**: Daily startup

### 3. Development Environment Check
- **Purpose**: Ensure dev tools are ready
- **Actions**:
    - Check Python environments (uv, poetry)
    - Verify essential tools installed
    - Check disk space in work directories
- **Safety**: Read-only checks
- **Frequency**: Daily startup

---

## 📁 Git Repository Management (Local Jobs)

### 4. Git Repository Status Report
- **Purpose**: Daily overview of all repo states
- **Actions**:
    - Scan all repos in workspace
    - Report: uncommitted changes, unpushed commits, branch status
    - List repos needing attention
- **Safety**: **Read-only dry-run** - no commits/pushes
- **Output**: Summary report for manual review
- **Frequency**: Daily startup

### 5. Safe Auto-Commit (Advanced)
- **Purpose**: Preserve work-in-progress safely
- **Logic**:
    - Only if uncommitted changes exist
    - Create new branch: `auto-commit-YYYYMMDD-HHMMSS`
    - Commit with descriptive message
    - **DO NOT** merge or push automatically
- **Safety Checks**:
    - Skip if files contain common secrets patterns
    - Skip if repo is on main/master branch with unpushed commits
    - Dry-run mode to show what would be committed
- **Manual Review**: User reviews auto-commit branches periodically
- **Frequency**: Optional/configurable

---

## 📂 File Organization (Local Jobs)

### 6. Downloads Folder Cleanup
- **Purpose**: Organize and clean downloads automatically
- **Actions**:
    - Move old files (>30 days) to archive
    - Delete temp files (.tmp, .download, .part)
    - Organize by file type into subfolders
- **AI Enhancement**: Use AI to suggest better filenames based on content
- **Safety**: Preserve original names as backup
- **Frequency**: Daily

### 7. Obsidian Notes Organization
- **Purpose**: Keep note vault organized
- **Actions**:
    - Move loose notes to proper folders
    - Update note links and references
    - Archive old daily notes
    - Generate index of orphaned notes
- **Safety**: Backup before changes
- **Frequency**: Daily

### 8. Workspace Cleanup
- **Purpose**: Clean up development workspace
- **Actions**:
    - Remove empty directories
    - Clean up .DS_Store files
    - Archive old log files
    - Clear temp directories
- **Safety**: Only touch known safe paths
- **Frequency**: Daily

---

## 📥 Data Collection & Backup (Cronicle Jobs)

*These are better suited for scheduled Cronicle jobs rather than daily startup jobs*

### 9. Zoom Recordings Backup
- **Purpose**: Auto-download and backup Zoom recordings
- **Actions**: Use existing draft tool
- **Storage**: Upload to Google Drive
- **Frequency**: Daily via Cronicle
- **Status**: Draft tool exists

### 10. Telegram Message Archive
- **Purpose**: Backup important telegram conversations
- **Actions**: Use existing telegram downloader
- **Storage**: Local archive + cloud backup
- **Frequency**: Weekly via Cronicle
- **Status**: Draft tool exists

### 11. Email Archive
- **Purpose**: Backup important emails
- **Actions**:
    - Connect to email providers (Gmail, etc.)
    - Download recent emails
    - Store in searchable format
- **Privacy**: Keep local, encrypted
- **Frequency**: Daily via Cronicle

### 12. Browser Data Backup
- **Purpose**: Backup bookmarks, history, etc.
- **Actions**:
    - Export Chrome bookmarks
    - Export browsing history (privacy-filtered)
    - Save to versioned backup
- **Tools**: Chrome has export APIs/tools
- **Frequency**: Weekly via Cronicle

---

## 🤖 AI-Enhanced Tasks (Future)

### 13. Intelligent File Naming
- **Purpose**: Use AI to suggest better file names
- **Actions**:
    - Analyze file content
    - Suggest descriptive names
    - Assign importance/category tags
- **Safety**: Always preserve original names
- **Local AI**: Use local models for privacy

### 14. Code Quality Monitor
- **Purpose**: AI review of uncommitted changes
- **Actions**:
    - Scan for potential secrets/tokens
    - Check code quality issues
    - Suggest improvements
- **Privacy**: Use local AI models only
- **Integration**: With git auto-commit workflow

---

## 📊 Implementation Priority

### Phase 1: Essential Health Checks (Week 1)
- [ ] Docker health check
- [ ] Cronicle health check
- [ ] Git repository status report (dry-run only)
- [ ] Downloads folder basic cleanup

### Phase 2: File Organization (Week 2-3)
- [ ] Workspace cleanup
- [ ] Obsidian notes organization
- [ ] Enhanced downloads organization

### Phase 3: Advanced Features (Month 2+)
- [ ] Safe auto-commit with AI safety checks
- [ ] AI-powered file naming
- [ ] Integration with existing tools (Telegram, Zoom)

---

## 🛡️ Safety Principles

1. **Dry-run first**: Always show what would be done
2. **Read-only by default**: Prefer reporting over automatic changes
3. **Preserve originals**: Backup before any destructive operations
4. **Manual review**: Critical operations need human approval
5. **Local AI only**: For privacy-sensitive tasks
6. **Fail safely**: Better to skip than break something

---

## 🔗 Integration with Existing Tools

- **Project Manager**: Use for workspace discovery
- **Project Discoverer**: For finding repositories
- **Existing drafts**: Telegram downloader, Zoom tool
- **Calmlib**: For logging and utilities
- **Cronicle**: For longer-running/scheduled tasks

---

## 💡 Usage Scenarios

### Daily Startup Routine
```bash
run_startup_jobs    # Runs all local jobs
job_logs           # Review what happened
```

### Weekly Maintenance
```bash
# Local jobs handle daily cleanup
# Cronicle jobs handle data collection
# Manual review of auto-commit branches
```

### Monthly Review
```bash
# Review AI suggestions
# Clean up auto-commit branches  
# Archive old data
```