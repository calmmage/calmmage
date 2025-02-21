// Constants and configuration
const SHEET_TRACKING_ENABLED = 'SHEET_TRACKING_ENABLED';
const SHEET_ID = 'SHEET_ID';

// Initialize or get the tracking sheet
function getTrackingSheet() {
  const scriptProperties = PropertiesService.getScriptProperties();
  const sheetId = scriptProperties.getProperty(SHEET_ID);
  
  if (!sheetId) {
    return createTrackingSheet();
  }
  
  try {
    return SpreadsheetApp.openById(sheetId).getActiveSheet();
  } catch (e) {
    Logger.log(`Error opening sheet: ${e}. Creating new one.`);
    return createTrackingSheet();
  }
}

// Create new tracking sheet
function createTrackingSheet() {
  const spreadsheet = SpreadsheetApp.create('Zoom Recordings Tracker');
  const sheet = spreadsheet.getActiveSheet();
  
  // Set up headers
  sheet.getRange('A1:F1').setValues([[
    'Date', 'Meeting Topic', 'Recording ID', 'Drive Link', 'YouTube Link', 'Processing Date'
  ]]);
  
  // Save sheet ID
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperty(SHEET_ID, spreadsheet.getId());
  
  Logger.log(`Created new tracking sheet: ${spreadsheet.getUrl()}`);
  return sheet;
}

// Check if recording was processed
function isRecordingProcessed(recordingId) {
  if (!isTrackingEnabled()) return false;
  
  const sheet = getTrackingSheet();
  const data = sheet.getDataRange().getValues();
  
  // Skip header row
  for (let i = 1; i < data.length; i++) {
    if (data[i][2] === recordingId) {
      return true;
    }
  }
  
  return false;
}

// Track processed recording
function trackRecording(date, topic, recordingId, driveLink = '', youtubeLink = '') {
  if (!isTrackingEnabled()) return;
  
  const sheet = getTrackingSheet();
  sheet.appendRow([
    date,
    topic,
    recordingId,
    driveLink,
    youtubeLink,
    new Date().toISOString()
  ]);
}

// Check if tracking is enabled
function isTrackingEnabled() {
  const scriptProperties = PropertiesService.getScriptProperties();
  return scriptProperties.getProperty(SHEET_TRACKING_ENABLED) === 'true';
}

// Enable tracking
function enableTracking() {
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperty(SHEET_TRACKING_ENABLED, 'true');
  
  // Create sheet if doesn't exist
  getTrackingSheet();
  Logger.log('Sheet tracking enabled');
}

// Disable tracking
function disableTracking() {
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperty(SHEET_TRACKING_ENABLED, 'false');
  Logger.log('Sheet tracking disabled');
}

// Get sheet URL
function getTrackingSheetUrl() {
  if (!isTrackingEnabled()) return null;
  
  const scriptProperties = PropertiesService.getScriptProperties();
  const sheetId = scriptProperties.getProperty(SHEET_ID);
  
  if (!sheetId) return null;
  
  try {
    return SpreadsheetApp.openById(sheetId).getUrl();
  } catch (e) {
    Logger.log(`Error getting sheet URL: ${e}`);
    return null;
  }
} 