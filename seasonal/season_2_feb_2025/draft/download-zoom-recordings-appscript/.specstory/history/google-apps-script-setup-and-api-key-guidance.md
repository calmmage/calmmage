## SpecStory

## Google Apps Script Setup and API Key Guidance (2/16/2025, 7:58:14 PM)

_**User**_

Guide me through next steps.

What do I do?

I'm on Google app script website.

I have one file with the code that I can run.
It works.

How do I set up the API key / token? Do I hardcode it in my file or is there a system
for then in AppScript?
Should I send you a screenshot?

Do I copy code from both code.gs and config.gs to my script in Google App Script? Or is
there multi-file setup possible in the google scripts?
Should I send you screenshot or do you know?

@Code.gs @Config.gs

@notes.md @todo.md

---

_**Assistant**_

Let me help you with setting up your Google Apps Script project step by step.

1. First, regarding file organization: Yes, Google Apps Script supports multiple files!
   You can create separate files by:

- Click the "+" button next to "Files" in the left sidebar
- Select "Script" to add a new .gs file
- Name it "Config" for your configuration file

2. You should create two files:

- Code.gs (your main code)
- Config.gs (for configuration)

Copy the respective code into each file.

3. For API credentials, Google Apps Script provides a secure way to store sensitive data
   using Script Properties. Here's how to set them up:

a. In the Google Apps Script editor:

- Click on "Project Settings" (⚙️ icon)
- Go to "Script Properties" tab
- Click "Add Script Property"
- Add each property:
    - ZOOM_ACCOUNT_ID
    - ZOOM_CLIENT_ID
    - ZOOM_CLIENT_SECRET
    - ZOOM_USER_ID

b. Or use the provided `setupZoomCredentials` function:

````javascript
function setupCredentialsExample() {
  setupZoomCredentials(
    'your_account_id',
    'your_client_id',
    'your_client_secret',
    'your_zoom_email'
  );
}
````

4. To get your Zoom API credentials:

- Go to the Zoom App Marketplace
- Navigate to "Develop" → "Build App"
- Choose "Server-to-Server OAuth"
- Fill in the app information
- Copy the Account ID, Client ID, and Client Secret

Would you like me to explain any of these steps in more detail? Or would a screenshot of
the Google Apps Script interface be helpful?

---

_**User**_

Where do I click?

---

_**Assistant**_

In your screenshot, you need to:

1. Click the "+" button next to "Files" in the left sidebar (it's visible in your
   screenshot, right next to the "AZ" button)

2. When you click it, select "Script" from the dropdown menu that appears

3. Name the new file "Config"

Then you can paste the Config.gs code into this new file.

Would you like me to show you the next steps after you've created the Config file?

---

_**User**_

should I have separate files for "get zoom id / pass from gmail" and "get video from
zoom api" parts of the script?
And like main.gs for complete pipeline?

---

_**Assistant**_

Yes, that's a good approach to organize your code! Let's split it into logical modules:

1. `Main.gs` - Main orchestration/pipeline:

- `processNewRecordings()` function
- `createTrigger()` function

2. `GmailParser.gs` - Email processing:

- `findZoomRecordings()`
- `extractRecordingInfo()`

3. `ZoomApi.gs` - Zoom API interactions:

- `getZoomToken()`
- `getZoomRecordings()`
- `downloadRecording()`

4. `Config.gs` - Configuration:

- `getZoomConfig()`
- `setupZoomCredentials()`

5. `DriveUtils.gs` - Google Drive operations:

- `createFolderPath()`
- File saving functions

This modular structure will make the code more maintainable and easier to debug. Would
you like me to show you how to restructure the code into these files?

---

_**User**_

Also (separately?) for youtube?



---

_**Assistant**_

Yes, definitely keep YouTube functionality separate! Following the single responsibility
principle, let's update the structure:

Core Modules:

1. `Main.gs` - Pipeline orchestration
2. `Config.gs` - All configurations
3. `GmailParser.gs` - Email processing
4. `ZoomApi.gs` - Zoom operations
5. `DriveUtils.gs` - Drive operations

Optional Upload Modules:

6. `YouTubeUploader.gs` - YouTube specific code

This separation gives you several benefits:

- You can develop and test the core recording download functionality independently
- YouTube upload can be added later without touching the core code
- If YouTube API has issues, it won't affect the main recording backup process

Would you like me to help you split the code into these modules? We can start with the
core modules first and add YouTube support later.

---

_**User**_

Can you please summarize all the info above as a single response?
I will be copying it elsewhere.

Separately include all messages I sent - with full text as is - just for context

---

_**Assistant**_

First, your messages for context:

```
Guide me through next steps.
What do I do?
I'm on Google app script website.
I have one file with the code that I can run. 
It works.
How do I set up the API key / token? Do I hardcode it in my file or is there a system for then in AppScript?
Should I send you a screenshot?
Do I copy code from both code.gs and config.gs to my script in Google App Script? Or is there multi-file setup possible in the google scripts?
Should I send you screenshot or do you know?
```

```
[Screenshot showing Google Apps Script interface]
Where do I click?
```

```
should I have separate files for "get zoom id / pass from gmail" and "get video from zoom api" parts of the script?
And like main.gs for complete pipeline?
```

```
Also (separately?) for youtube?
```

Summary of Setup Instructions:

1. File Structure in Google Apps Script:

- Click "+" next to "Files" in left sidebar
- Select "Script" for new .gs file
- Create following modules:

Core Modules:

```
1. Main.gs         - Pipeline orchestration
2. Config.gs       - All configurations
3. GmailParser.gs  - Email processing
4. ZoomApi.gs      - Zoom operations
5. DriveUtils.gs   - Drive operations
6. YouTubeUploader.gs (optional) - YouTube specific code
```

2. API Credentials Setup:

- Option 1: Script Properties
    - Go to "Project Settings" (⚙️)
    - "Script Properties" tab
    - Add: ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, ZOOM_USER_ID

- Option 2: Use provided function

```javascript
function setupCredentialsExample() {
  setupZoomCredentials(
    'your_account_id',
    'your_client_id',
    'your_client_secret',
    'your_zoom_email'
  );
}
```

3. Get Zoom API Credentials:

- Visit Zoom App Marketplace
- Develop → Build App
- Choose "Server-to-Server OAuth"
- Fill app information
- Copy Account ID, Client ID, and Secret

This modular structure keeps code organized, maintainable, and allows independent
development of core and optional features.

---



---

