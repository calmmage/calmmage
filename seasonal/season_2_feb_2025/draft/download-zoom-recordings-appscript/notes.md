```
// Main function to find and process Zoom recording emails
function findZoomRecordings() {
  const searchQuery = 'from:no-reply@zoom.us subject:"Теперь доступны облачные записи - " newer_than:30d';

  const results = [];
  
  try {
    // Search for Zoom recording emails
    const threads = GmailApp.search(searchQuery);
    Logger.log(`Found ${threads.length} email threads`);
    
    threads.forEach((thread) => {
      const messages = thread.getMessages();
      
      messages.forEach((message) => {
        try {
          const recording = extractRecordingInfo(message);
          if (recording) {
            results.push(recording);
          }
        } catch (e) {
          Logger.log(`Error processing message ${message.getId()}: ${e.toString()}`);
        }
      });
    });
    
    return results;
    
  } catch (e) {
    Logger.log(`Fatal error: ${e.toString()}`);
    return null;
  }
}

// Extract recording information from email
function extractRecordingInfo(message) {
  const subject = message.getSubject();
  const body = message.getPlainBody();
  
  // Basic info object
  const recordingInfo = {
    date: message.getDate(),
    subject: subject,
    meetingTopic: subject.replace('Cloud Recording - ', '').trim(),
    downloadLink: null,
    password: null,
    emailId: message.getId()
  };
  
  // Extract download link
  const linkMatch = body.match(/https:\/\/[\w-]+\.zoom\.us\/rec\/share\/[\w-]+/);
  if (linkMatch) {
    recordingInfo.downloadLink = linkMatch[0];
    Logger.log(`Found downloadLink: ${recordingInfo.downloadLink}`)
  }
  
  // Extract password
  const passwordMatch = body.match(/Код доступа: (\S+)/);
  if (passwordMatch) {
    recordingInfo.password = passwordMatch[1];
    Logger.log(`Found password: ${recordingInfo.password}` )
  }
  
  // Only return if we found both link and password
  if (recordingInfo.downloadLink && recordingInfo.password) {
    return recordingInfo;
  }
  
  Logger.log(`Could not extract complete info from email ${message.getId()}`);
  return null;
}

// Test function to run and check results
function testExtraction() {
  const recordings = findZoomRecordings();
  Logger.log('Found recordings:');
  Logger.log(JSON.stringify(recordings, null, 2));
}
```