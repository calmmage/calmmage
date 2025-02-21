## SpecStory

## Automating Zoom Recordings to YouTube/Google Drive (2/16/2025, 7:58:14 PM)

_**User**_

I need to build a service for auto-downloading zoom recordings and uploading them to
youtube / google drive

Bonus points: be able to share it to friends easily

We're using google app scripts for that

i aleady did the first part - extract info from gmail

@notes.md

let's proceed:
Let's formulate a plan

1) find emails from zoom about recordings
   -> extract link and password
   1.5) Maybe I can get them from zoom api instead?
2) Download via zoom api
3) Upload to google drive
   3.5) Maybe upload to YouTube, not drive?

Considerations:
a) one-time bulk export
-> need try-except for videos that expired
b) rolling monitoring - need trigger & filer.



---

_**Assistant**_

I'll help create a structured plan for your Zoom recording automation service. Let me
organize the information and create a todo list based on your requirements.

````markdown:todo.md
# Core Features

1. "find emails from zoom about recordings -> extract link and password"
   - Already implemented in notes.md
   - Consider adding error handling for expired links

2. "Download via zoom api"
   - Research Zoom API authentication
   - Implement recording download endpoint
   - Compare email-based vs API-based approaches
   
3. "Upload to google drive/YouTube"
   - Implement Google Drive upload first (simpler)
   - Add YouTube upload as optional enhancement
   
4. "rolling monitoring"
   - Add time-based trigger
   - Track processed recordings
   - Filter out already processed items

# Implementation Notes

Email vs API approaches:
- Email: already working, but links may expire
- Zoom API: more reliable, but requires setup
- Consider supporting both methods

Deployment options:
- Package as Google Apps Script for easy sharing
- Store credentials securely
- Provide simple setup instructions

# Next Steps
Focus on implementing the download functionality first, then proceed with upload features.
````

I've organized the plan focusing on core features while keeping it minimal. The next
step would be to choose between continuing with the email-based approach or switching to
the Zoom API. Which path would you prefer to explore first?

---

_**User**_

Wtf. Just write the code

---

_**Assistant**_

Let's start with implementing the download functionality using the email-based approach
since we already have the recording info extraction working.

Here's the code to download recordings and save them to Google Drive:

````javascript:Code.gs
// Download recording and save to Drive
function downloadAndSaveRecording(recordingInfo) {
  const { downloadLink, password, meetingTopic, date } = recordingInfo;
  
  // Create folder structure YYYY/MM/recordings
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const folderName = `${year}/${month}/recordings`;
  const folder = createFolderPath(folderName);
  
  // Format filename with date and topic
  const fileName = `${date.toISOString().split('T')[0]} - ${meetingTopic}.mp4`;
  
  try {
    // Download recording using password
    const options = {
      'method': 'get',
      'headers': {
        'Cookie': `download_pw=${password}`
      },
      'muteHttpExceptions': true
    };
    
    const response = UrlFetchApp.fetch(downloadLink, options);
    if (response.getResponseCode() === 200) {
      // Save to Drive
      const blob = response.getBlob().setName(fileName);
      const file = folder.createFile(blob);
      Logger.log(`Saved recording: ${fileName}`);
      return file.getId();
    } else {
      throw new Error(`Failed to download: ${response.getResponseCode()}`);
    }
  } catch (e) {
    Logger.log(`Error downloading ${fileName}: ${e.toString()}`);
    throw e;
  }
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
````

This code:

1. Downloads recordings using the link and password from email
2. Saves files to Google Drive in YYYY/MM/recordings folder structure
3. Names files with date and meeting topic
4. Includes a trigger to check for new recordings hourly

To use it:

1. Add this code to your Google Apps Script project
2. Run `createTrigger()` once to set up automatic monitoring
3. Or run `processNewRecordings()` manually for one-time processing

Want to test it with a single recording first?

---

_**User**_

Hm, do you know about the zoom api?

@https://devforum.zoom.us/t/how-can-i-get-cloud-recordings-video-using-zoom-api/94828

Where do I put the zoom api key? @Zoom API Recordings

---

_**Assistant**_

Yes, let's switch to using the Zoom API which will be more reliable. First, we need to
set up the API credentials and configuration:

````javascript:Config.gs
// Store API credentials and configuration
function getZoomConfig() {
  const scriptProperties = PropertiesService.getScriptProperties();
  return {
    accountId: scriptProperties.getProperty('ZOOM_ACCOUNT_ID'),
    clientId: scriptProperties.getProperty('ZOOM_CLIENT_ID'),
    clientSecret: scriptProperties.getProperty('ZOOM_CLIENT_SECRET'),
    userId: scriptProperties.getProperty('ZOOM_USER_ID') // your zoom user email
  };
}

// Set up API credentials
function setupZoomCredentials(accountId, clientId, clientSecret, userId) {
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperties({
    'ZOOM_ACCOUNT_ID': accountId,
    'ZOOM_CLIENT_ID': clientId, 
    'ZOOM_CLIENT_SECRET': clientSecret,
    'ZOOM_USER_ID': userId
  });
}
````

And here's the updated recording download code using the Zoom API:

````javascript:Code.gs
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
````

To use this:

1. Create a Server-to-Server OAuth app in Zoom Marketplace
2. Get your Account ID, Client ID and Client Secret
3. Run this to set up credentials:

```javascript
setupZoomCredentials(
  'your_account_id',
  'your_client_id',
  'your_client_secret',
  'your_zoom_email'
);
```

4. Run `processZoomRecordings()` to download recordings

This approach is more reliable than email-based downloads since it:

- Doesn't depend on email notifications
- Gets recordings directly from Zoom
- Doesn't require handling passwords
- Can access recordings immediately after they're available

Want me to explain any part in more detail?

---



---

