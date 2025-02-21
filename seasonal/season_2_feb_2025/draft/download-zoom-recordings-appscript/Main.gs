// Process recordings with specified upload options and date range
function processZoomRecordings(uploadToDrive = true, uploadToYoutube = false, fromDate = null, toDate = null) {
  // Get date range
  const from = fromDate ? new Date(fromDate) : new Date(Date.now() - 30 * 24 * 60 * 60 * 1000); // default 30 days
  const to = toDate ? new Date(toDate) : new Date();
  
  Logger.log(`Fetching recordings from ${from.toISOString()} to ${to.toISOString()}`);
  const recordings = getZoomRecordings(from, to);
  
  // Store total for progress tracking
  const totalMeetings = recordings.meetings.length;
  let processedMeetings = 0;
  
  // Store progress in script properties
  const scriptProperties = PropertiesService.getScriptProperties();
  const lastProcessedDate = scriptProperties.getProperty('LAST_PROCESSED_DATE');
  
  recordings.meetings.sort((a, b) => new Date(a.start_time) - new Date(b.start_time));
  
  for (const meeting of recordings.meetings) {
    // Skip if already processed (for resumption)
    if (lastProcessedDate && new Date(meeting.start_time) <= new Date(lastProcessedDate)) {
      processedMeetings++;
      continue;
    }
    
    meeting.recording_files.forEach(recording => {
      if (recording.file_type === 'MP4') {
        // Skip if already processed (check in sheet if enabled)
        if (isTrackingEnabled() && isRecordingProcessed(recording.id)) {
          Logger.log(`Skipping already processed recording: ${meeting.topic}`);
          return;
        }
        
        try {
          const fileName = `${meeting.start_time.split('T')[0]} - ${meeting.topic}.mp4`;
          const blob = downloadRecording(recording.download_url, fileName);
          let driveLink = '';
          let youtubeLink = '';
          
          if (uploadToDrive) {
            const file = saveFileToDrive(blob, 'recordings');
            driveLink = file.getUrl();
          }
          
          if (uploadToYoutube) {
            if (enableYouTubeService()) {
              const videoId = uploadToYouTube(blob, fileName);
              youtubeLink = `https://youtu.be/${videoId}`;
            } else {
              Logger.log('YouTube upload skipped - API not enabled');
            }
          }
          
          // Track in sheet if enabled
          if (isTrackingEnabled()) {
            trackRecording(
              meeting.start_time,
              meeting.topic,
              recording.id,
              driveLink,
              youtubeLink
            );
          }
          
          // Update progress after successful processing
          scriptProperties.setProperty('LAST_PROCESSED_DATE', meeting.start_time);
        } catch (e) {
          Logger.log(`Error processing ${meeting.topic}: ${e.toString()}`);
          // Don't update progress on error to allow retry
        }
      }
    });
    
    processedMeetings++;
    Logger.log(`Progress: ${processedMeetings}/${totalMeetings} meetings processed`);
  }
  
  return {
    total: totalMeetings,
    processed: processedMeetings,
    fromDate: from.toISOString(),
    toDate: to.toISOString(),
    sheetUrl: isTrackingEnabled() ? getTrackingSheetUrl() : null
  };
}

// Historical data processing
function processHistoricalData(startDate, endDate = null, uploadToDrive = true, uploadToYoutube = false) {
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.deleteProperty('LAST_PROCESSED_DATE'); // Reset progress for new historical run
  
  return processZoomRecordings(uploadToDrive, uploadToYoutube, startDate, endDate);
}

// Resume from last processed date
function resumeProcessing(uploadToDrive = true, uploadToYoutube = false) {
  const scriptProperties = PropertiesService.getScriptProperties();
  const lastDate = scriptProperties.getProperty('LAST_PROCESSED_DATE');
  
  if (!lastDate) {
    Logger.log('No previous progress found. Starting from beginning.');
    return processZoomRecordings(uploadToDrive, uploadToYoutube);
  }
  
  Logger.log(`Resuming from ${lastDate}`);
  return processZoomRecordings(uploadToDrive, uploadToYoutube, lastDate);
}

// Convenience functions for different upload options
function uploadToDriveOnly() {
  processZoomRecordings(true, false);
}

function uploadToYoutubeOnly() {
  processZoomRecordings(false, true);
}

function uploadToBoth() {
  processZoomRecordings(true, true);
}

// Hourly execution with heartbeat
function hourlyRun() {
  // Send heartbeat first
  sendHeartbeat('zoom-recording-downloader');
  
  // Then process recordings (Drive-only by default)
  uploadToDriveOnly();
}

// Add trigger to run every hour (using hourlyRun function)
function createTrigger() {
  // Delete existing triggers first
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));
  
  // Create new trigger
  ScriptApp.newTrigger('hourlyRun')
    .timeBased()
    .everyHours(1)
    .create();
  
  Logger.log('Trigger has been set up to run every hour (with heartbeat)');
}

// Manual execution functions
function manualRunDriveOnly() {
  uploadToDriveOnly();
}

function manualRunYoutubeOnly() {
  uploadToYoutubeOnly();
}

function manualRunBoth() {
  uploadToBoth();
}

// Manual heartbeat test
function testHeartbeat() {
  return sendHeartbeat('zoom-recording-downloader');
} 