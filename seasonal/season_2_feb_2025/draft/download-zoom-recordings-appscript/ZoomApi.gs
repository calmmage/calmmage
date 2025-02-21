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

// Download recording from Zoom
function downloadRecording(downloadUrl, fileName) {
  const token = getZoomToken();
  const options = {
    'method': 'get',
    'headers': {
      'Authorization': `Bearer ${token}`
    }
  };
  
  const response = UrlFetchApp.fetch(downloadUrl, options);
  return response.getBlob().setName(fileName);
} 