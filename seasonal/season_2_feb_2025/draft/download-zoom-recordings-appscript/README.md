# Zoom Recording Downloader (Google Apps Script)

Automatically downloads Zoom cloud recordings to Google Drive and optionally uploads
them to YouTube.
Includes heartbeat monitoring integration with service-registry.calmmage.com.

## Features

- Automatic download of Zoom cloud recordings
- Organized folder structure in Google Drive (Year/Month/recordings)
- Optional YouTube upload support
- Heartbeat monitoring
- Hourly automatic execution
- Historical data processing with resume capability

## Setup Instructions

### 1. Create Google Apps Script Project

1. Go to [Google Apps Script](https://script.google.com/)
2. Click "New Project"
3. Create the following files (click "+" next to "Files"):
    - `Config.gs`
    - `ZoomApi.gs`
    - `DriveUtils.gs`
    - `YouTubeUploader.gs`
    - `HeartbeatService.gs`
    - `Main.gs`
4. Copy the code from this repository into each corresponding file

### 2. Set Up Zoom API Credentials

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Click "Develop" → "Build App"
3. Choose "Server-to-Server OAuth" app type
4. Fill in the app information
5. Note down:
    - Account ID
    - Client ID
    - Client Secret
    - Your Zoom user email (User ID)

### 3. Configure Script Properties

1. In Google Apps Script, click on "Project Settings" (⚙️)
2. Go to "Script Properties" tab
3. Required properties:
    - `ZOOM_ACCOUNT_ID`: Your Zoom account ID
    - `ZOOM_CLIENT_ID`: Your Zoom client ID
    - `ZOOM_CLIENT_SECRET`: Your Zoom client secret
    - `ZOOM_USER_ID`: Your Zoom user email

4. Optional tracking properties:
   - `SHEET_TRACKING_ENABLED`: Set to 'true' to enable tracking in Google Sheets
   - `SHEET_ID`: (Auto-set) ID of the tracking spreadsheet. Only set manually if you
     want to use an existing sheet

Note: When you enable tracking using `enableTracking()`, the script will automatically:

1. Create a new tracking spreadsheet
2. Set the `SHEET_ID` property
3. Set `SHEET_TRACKING_ENABLED` to 'true'

Alternatively, you can run this function in the script editor:

```javascript
function setupCredentials() {
  setupZoomCredentials(
    'your_account_id',
    'your_client_id',
    'your_client_secret',
    'your_zoom_email'
  );
}
```

### 4. Enable YouTube Upload (Optional)

If you want to use YouTube upload functionality:

1. In Google Apps Script, click on "Services" (+ button)
2. Find and add "YouTube Data API v3"
3. Save and authorize when prompted

### 5. Set Up Automatic Execution

1. Run `createTrigger()` function to set up hourly execution
2. Authorize the script when prompted for permissions

## Usage

### Manual Execution

The script provides several manual execution functions:

- `manualRunDriveOnly()`: Download recordings to Drive only
- `manualRunYoutubeOnly()`: Upload recordings to YouTube only
- `manualRunBoth()`: Download to Drive and upload to YouTube
- `testHeartbeat()`: Test the heartbeat monitoring connection

### Historical Data Processing

To process historical recordings:

```javascript
// Process all recordings from a specific date
function processLastYear() {
  const startDate = '2023-01-01'; // Format: YYYY-MM-DD
  return processHistoricalData(startDate, null, true, false); // true for Drive, false for YouTube
}

// Process recordings between specific dates
function processDateRange() {
  const startDate = '2023-01-01';
  const endDate = '2023-12-31';
  return processHistoricalData(startDate, endDate, true, false);
}
```

### Handling Interruptions

If the script stops mid-execution (due to timeout, API limits, etc.):

1. The script automatically saves progress after each successful recording
2. To resume from the last processed recording:
   ```javascript
   resumeProcessing(true, false); // true for Drive, false for YouTube
   ```

### Progress Tracking

- The script logs progress for each meeting processed
- Check the execution logs to see:
    - Total number of meetings found
    - Current progress (X/Y meetings processed)
    - Last processed date
    - Any errors or skipped recordings

### API Limits and Timeouts

- Google Apps Script has a maximum execution time of 6 minutes
- YouTube API has daily quota limits
- To handle these limitations:
    1. Process smaller date ranges (e.g., month by month)
    2. Use `resumeProcessing()` to continue after interruptions
    3. For YouTube uploads, spread the workload across multiple days

### Automatic Execution

By default, the script:

- Runs every hour
- Sends a heartbeat to service-registry.calmmage.com
- Downloads new recordings to Google Drive
- Creates organized folder structure (Year/Month/recordings)

### Monitoring

The script sends heartbeats to service-registry.calmmage.com every hour. You can monitor
the service status there.

### Progress Tracking (Optional)

The script can track all processed recordings in a Google Sheet:

1. Enable tracking:
   ```javascript
   function setupTracking() {
     enableTracking();  // This will create a new sheet and enable tracking
   }
   ```

2. The tracking sheet will include:
   - Recording date and topic
   - Drive and YouTube links
   - Processing timestamp
   - Unique recording ID

3. Benefits:
   - Prevents duplicate processing
   - Easy access to all video links
   - Processing history

4. To disable tracking:
   ```javascript
   function stopTracking() {
     disableTracking();
   }
   ```

## Troubleshooting

### Common Issues

1. **"YouTube API service is not enabled"**
    - Solution: Enable YouTube Data API v3 in Services

2. **"Authorization is required"**
    - Solution: Run any manual function and approve the permissions

3. **Zoom API errors**
    - Verify your Zoom credentials in Script Properties
    - Check if your Server-to-Server OAuth app is active

### Logs

- Check execution logs in Apps Script dashboard
- All operations are logged using `Logger.log()`
- Errors include detailed messages for debugging

## Security Notes

- Never share your Zoom API credentials
- Script Properties securely store sensitive information
- YouTube uploads are set to "unlisted" by default

## Development

### Quick Setup (Recommended)

1. Clone this repository:
   ```bash
   git clone https://your-repository-url.git
   cd your-repository-name
   ```

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

The script will:

- Install clasp if needed
- Set up the project structure
- Configure git hooks for automatic pushing
- Guide you through the remaining setup steps

### Manual Setup with clasp

If you prefer manual setup:

1. Install clasp globally:
   ```bash
   npm install -g @google/clasp
   ```

2. Login to Google:
   ```bash
   clasp login
   ```

3. Clone this repository:
   ```bash
   git clone https://your-repository-url.git
   cd your-repository-name
   ```

4. Create a new Google Apps Script project:
   ```bash
   clasp create --title "Zoom Recording Downloader" --type standalone
   ```

5. Push code to Google Apps Script:
   ```bash
   clasp push
   ```

6. Open the project in browser:
   ```bash
   clasp open
   ```

### Git Hooks (Automated with setup.sh)

The setup script installs two git hooks:

1. `pre-commit`: Ensures all .gs files are in the src/ directory
2. `post-commit`: Automatically pushes changes to Google Apps Script

To disable automatic pushing, remove or modify `.git/hooks/post-commit`

### Authentication on macOS

1. First-time setup:
   ```bash
   # Install Node.js and npm (if not already installed)
   brew install node

   # Run setup script
   ./setup.sh
   ```

2. Google Authentication:
   - Run `clasp login`
   - Your default browser will open
   - Login with your Google account
   - Grant necessary permissions
   - Authentication tokens are stored in ~/.clasprc.json

### Local Development

1. Enable Apps Script API:
   - Visit https://script.google.com/home/usersettings
   - Turn on "Google Apps Script API"

2. Configure .claspignore:
   ```
   # Ignore files not needed in Apps Script
   **/.git/**
   **/node_modules/**
   README.md
   package.json
   ```

3. Watch for changes (auto-push):
   ```bash
   clasp push --watch
   ```

### Repository Structure

```
.
├── .clasp.json          # clasp configuration
├── appsscript.json      # Apps Script manifest
├── src/
│   ├── Config.gs
│   ├── ZoomApi.gs
│   ├── DriveUtils.gs
│   ├── YouTubeUploader.gs
│   ├── HeartbeatService.gs
│   ├── SheetsTracker.gs
│   └── Main.gs
└── README.md
``` 