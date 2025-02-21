// First Run Setup
function firstRun() {
  const scriptProperties = PropertiesService.getScriptProperties();
  const startDate = scriptProperties.getProperty('FIRST_RUN_START_DATE');
  
  if (!startDate) {
    throw new Error(
      'Please set FIRST_RUN_START_DATE in Script Properties before running.\n' +
      'Format: YYYY-MM-DD (example: 2024-01-01)'
    );
  }
  
  // Validate date format
  if (!/^\d{4}-\d{2}-\d{2}$/.test(startDate)) {
    throw new Error('Invalid FIRST_RUN_START_DATE format. Please use YYYY-MM-DD format.');
  }
  
  // Process recordings from start date - Drive only for first run
  return processHistoricalData(startDate, null, true, false /* uploadToYoutube disabled */);
} 

// Hourly execution with heartbeat
function hourlyRun() {
  // Send heartbeat first
  sendHeartbeat('zoom-recording-downloader');
  
  // First, process new recordings to Drive
  const result = processZoomRecordings(true, false);  // Drive only
  
  // Then upload new files to YouTube if enabled
  if (isYouTubeEnabled()) {
    uploadNewRecordingsToYouTube();
  }
}

// Upload new recordings to YouTube
function uploadNewRecordingsToYouTube() {
  const folder = getOrCreateFolder('Zoom Recordings');
  const files = folder.getFiles();
  
  while (files.hasNext()) {
    const file = files.next();
    
    // Skip if already uploaded to YouTube (check properties)
    if (file.getDescription()?.includes('YouTube ID:')) {
      continue;
    }
    
    try {
      const videoId = uploadToYouTube(file, file.getName());
      
      // Mark as uploaded
      const currentDesc = file.getDescription() || '';
      file.setDescription(currentDesc + `\nYouTube ID: ${videoId}`);
      
      Logger.log(`Uploaded ${file.getName()} to YouTube: ${videoId}`);
    } catch (e) {
      Logger.log(`Failed to upload ${file.getName()} to YouTube: ${e.toString()}`);
    }
  }
}

// Process recordings with specified upload options and date range
function processZoomRecordings(uploadToDrive = true, uploadToYoutube = false, fromDate = null, toDate = null) {
  // Check YouTube availability upfront if needed
  if (uploadToYoutube && !isYouTubeEnabled()) {
    throw new Error(
      'YouTube upload was requested but YouTube API is not enabled.\n' +
      'Please enable YouTube Data API v3 before running with YouTube upload.'
    );
  }

  // Default to last 30 days if no date provided
  const defaultFrom = new Date();
  defaultFrom.setDate(defaultFrom.getDate() - 30);
  
  const from = fromDate ? new Date(fromDate) : defaultFrom;
  const to = toDate ? new Date(toDate) : new Date();
  
  Logger.log(`Input dates - fromDate: ${fromDate}, toDate: ${toDate}`);
  Logger.log(`Parsed dates - from: ${from.toISOString()}, to: ${to.toISOString()}`);
  
  if (from > to) {
    throw new Error(`Invalid date range: start date (${from.toISOString()}) is after end date (${to.toISOString()})`);
  }
  
  Logger.log(`Fetching recordings from ${from.toISOString().split('T')[0]} to ${to.toISOString().split('T')[0]}`);
  const recordings = getZoomRecordings(from, to);
  
  // Store total for progress tracking
  const totalMeetings = recordings.meetings.length;
  let processedMeetings = 0;
  
  // Store progress in script properties
  const scriptProperties = PropertiesService.getScriptProperties();
  const lastProcessedDate = scriptProperties.getProperty('LAST_PROCESSED_DATE');
  
  recordings.meetings.sort((a, b) => new Date(a.start_time) - new Date(b.start_time));
  
  Logger.log(`Processing ${totalMeetings} meetings in order:`);
  recordings.meetings.forEach((m, i) => {
    Logger.log(`${i + 1}. ${m.start_time} - ${m.topic} (${m.recording_files.length} files)`);
  });
  
  for (const meeting of recordings.meetings) {
    Logger.log(`\nProcessing meeting: ${meeting.start_time} - ${meeting.topic}`);
    
    // Skip if already processed (for resumption)
    if (lastProcessedDate && new Date(meeting.start_time) <= new Date(lastProcessedDate)) {
      Logger.log(`Skipping already processed meeting: ${meeting.topic}`);
      processedMeetings++;
      continue;
    }

    // First process video recordings (with potential YouTube upload)
    const videoRecordings = meeting.recording_files.filter(r => r.file_type === 'MP4');
    Logger.log(`Processing ${videoRecordings.length} video recordings`);
    
    for (const recording of videoRecordings) {
      if (isTrackingEnabled() && isRecordingProcessed(recording.id)) {
        Logger.log(`Skipping already processed video: ${recording.id}`);
        continue;
      }

      const fileName = `${meeting.start_time.split('T')[0]} - ${meeting.topic}${
        videoRecordings.length > 1 ? ` (${recording.recording_type})` : ''
      }.mp4`;
      
      const blob = downloadRecording(recording.download_url, fileName);
      let driveLink = '';
      let youtubeLink = '';
      
      if (uploadToDrive) {
        const file = saveFileToDrive(blob, meeting.start_time);
        driveLink = file.getUrl();
        Logger.log(`Saved video to Drive: ${driveLink}`);
      }
      
      if (uploadToYoutube) {
        try {
          const videoId = uploadToYouTube(blob, fileName);
          youtubeLink = `https://youtu.be/${videoId}`;
          Logger.log(`Uploaded to YouTube: ${youtubeLink}`);
        } catch (e) {
          if (e.toString().includes('Unauthorized')) {
            throw new Error(
              'YouTube API authorization failed. Please:\n' +
              '1. Check that YouTube API is enabled in Advanced Services\n' +
              '2. Re-authorize the script with your Google account\n' +
              '3. Make sure you have a YouTube channel set up\n' +
              '\nOriginal error: ' + e.toString()
            );
          }
          throw e;  // Re-throw other errors
        }
      }
      
      // Track in sheet if enabled
      if (isTrackingEnabled()) {
        trackRecording(
          meeting.start_time,
          meeting.topic,
          recording.id,
          driveLink,
          youtubeLink,
          'MP4',
          recording.recording_type
        );
        Logger.log('Tracked in sheet');
      }
      
      // Send email notification
      notifyVideoProcessed(meeting.start_time, meeting.topic, driveLink, youtubeLink);
      Logger.log('Email notification sent');
      
      // Update progress after successful processing
      scriptProperties.setProperty('LAST_PROCESSED_DATE', meeting.start_time);
    }

    // Then process audio recordings (Drive-only)
    const audioRecordings = meeting.recording_files.filter(r => r.file_type === 'M4A');
    Logger.log(`Processing ${audioRecordings.length} audio recordings`);
    
    for (const recording of audioRecordings) {
      if (isTrackingEnabled() && isRecordingProcessed(recording.id)) {
        Logger.log(`Skipping already processed audio: ${recording.id}`);
        continue;
      }

      const fileName = `${meeting.start_time.split('T')[0]} - ${meeting.topic}${
        audioRecordings.length > 1 ? ` (${recording.recording_type})` : ''
      }.m4a`;
      
      const blob = downloadRecording(recording.download_url, fileName);
      
      if (uploadToDrive) {
        const file = saveFileToDrive(blob, meeting.start_time);
        const driveLink = file.getUrl();
        Logger.log(`Saved audio to Drive: ${driveLink}`);
        
        if (isTrackingEnabled()) {
          trackRecording(
            meeting.start_time,
            meeting.topic,
            recording.id,
            driveLink,
            '', // no YouTube link for audio
            'M4A',
            recording.recording_type
          );
        }
      }
    }

    processedMeetings++;
    Logger.log(`\nProgress: ${processedMeetings}/${totalMeetings} meetings processed`);
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
  
  Logger.log(`Starting historical data processing from ${startDate} to ${endDate || 'now'}`);
  const result = processZoomRecordings(uploadToDrive, uploadToYoutube, startDate, endDate);
  Logger.log(`Completed historical data processing: ${JSON.stringify(result)}`);
  return result;
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

function processRecording(recording) {
  const downloadUrl = recording.download_url;
  const blob = downloadRecording(downloadUrl);
  if (!blob) {
    Logger.log(`Failed to download recording: ${recording.topic}`);
    return null;
  }
  
  // Save to Drive
  const file = saveFileToDrive(blob, recording.start_time);
  
  // Upload to YouTube if enabled
  if (uploadToYoutube) {
    const videoId = uploadToYouTube(blob, recording.topic);
    Logger.log(`Uploaded to YouTube: ${videoId}`);
  }
  
  return file;
}