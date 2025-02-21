// Get OAuth token for Zoom API
function getZoomToken() {
  const config = getZoomConfig();
  const credentials = Utilities.base64Encode(`${config.clientId}:${config.clientSecret}`);
  
  const options = {
    'method': 'post',
    'headers': {
      'Authorization': `Basic ${credentials}`
    },
    'payload': {
      'grant_type': 'account_credentials',
      'account_id': config.accountId
    }
  };
  
  const response = UrlFetchApp.fetch('https://zoom.us/oauth/token', options);
  const token = JSON.parse(response.getContentText());
  return token.access_token;
}

// Get recordings using Zoom API
function getZoomRecordings() {
  const config = getZoomConfig();
  const token = getZoomToken();
  
  // Get recordings from last 30 days
  const from = new Date();
  from.setDate(from.getDate() - 30);
  
  const options = {
    'method': 'get',
    'headers': {
      'Authorization': `Bearer ${token}`
    }
  };
  
  const url = `https://api.zoom.us/v2/users/${config.userId}/recordings?from=${from.toISOString().split('T')[0]}`;
  const response = UrlFetchApp.fetch(url, options);
  return JSON.parse(response.getContentText());
}

// Process and save recordings
function processZoomRecordings() {
  const recordings = getZoomRecordings();
  
  recordings.meetings.forEach(meeting => {
    meeting.recording_files.forEach(recording => {
      if (recording.file_type === 'MP4') {
        try {
          const fileName = `${meeting.start_time.split('T')[0]} - ${meeting.topic}.mp4`;
          downloadRecording(recording.download_url, fileName);
        } catch (e) {
          Logger.log(`Error downloading ${meeting.topic}: ${e.toString()}`);
        }
      }
    });
  });
}

// Download and save recording
function downloadRecording(downloadUrl, fileName) {
  const token = getZoomToken();
  const options = {
    'method': 'get',
    'headers': {
      'Authorization': `Bearer ${token}`
    }
  };
  
  // Create folder structure
  const date = new Date();
  const folder = createFolderPath(`${date.getFullYear()}/${(date.getMonth() + 1).toString().padStart(2, '0')}/recordings`);
  
  const response = UrlFetchApp.fetch(downloadUrl, options);
  const blob = response.getBlob().setName(fileName);
  folder.createFile(blob);
  Logger.log(`Saved recording: ${fileName}`);
}

// Create nested folder structure
function createFolderPath(folderPath) {
  const parts = folderPath.split('/');
  let parent = DriveApp.getRootFolder();
  
  for (const part of parts) {
    const folders = parent.getFoldersByName(part);
    if (folders.hasNext()) {
      parent = folders.next();
    } else {
      parent = parent.createFolder(part);
    }
  }
  
  return parent;
}

// Main function to process new recordings
function processNewRecordings() {
  const recordings = findZoomRecordings();
  if (!recordings) return;
  
  recordings.forEach(recording => {
    try {
      downloadAndSaveRecording(recording);
    } catch (e) {
      Logger.log(`Failed to process recording: ${e.toString()}`);
    }
  });
}

// Add trigger to run every hour
function createTrigger() {
  ScriptApp.newTrigger('processNewRecordings')
    .timeBased()
    .everyHours(1)
    .create();
} 