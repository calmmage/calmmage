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
function getZoomRecordings(fromDate, toDate = new Date()) {
  const config = getZoomConfig();
  const token = getZoomToken();
  
  const from = new Date(fromDate);  // Ensure we have a Date object
  const to = new Date(toDate);      // Ensure we have a Date object
  
  Logger.log(`Original date range request: ${from.toISOString()} to ${to.toISOString()}`);
  
  // Zoom API has a 30-day limit for listing recordings
  const maxDays = 30;
  let currentFrom = new Date(from);
  let allMeetings = [];
  
  while (currentFrom < to) {
    // Calculate chunk end date (either 30 days from start or final end date)
    let chunkEnd = new Date(currentFrom);
    chunkEnd.setDate(chunkEnd.getDate() + maxDays);
    if (chunkEnd > to) {
      chunkEnd = to;
    }
    
    Logger.log(`Fetching chunk: ${currentFrom.toISOString()} to ${chunkEnd.toISOString()}`);
    
    const options = {
      'method': 'get',
      'headers': {
        'Authorization': `Bearer ${token}`
      }
    };
    
    // Format dates as YYYY-MM-DD for Zoom API
    const fromStr = currentFrom.toISOString().split('T')[0];
    const toStr = chunkEnd.toISOString().split('T')[0];
    
    let nextPageToken = '';
    let page = 1;
    
    do {
      const pageParam = nextPageToken ? `&next_page_token=${nextPageToken}` : '';
      const url = `https://api.zoom.us/v2/users/${config.userId}/recordings?from=${fromStr}&to=${toStr}&page_size=300${pageParam}`;
      Logger.log(`Fetching page ${page} from Zoom API: ${url}`);
      
      const response = UrlFetchApp.fetch(url, options);
      const result = JSON.parse(response.getContentText());
      
      if (result.meetings && result.meetings.length > 0) {
        allMeetings = allMeetings.concat(result.meetings);
        Logger.log(`Added ${result.meetings.length} meetings from page ${page} of chunk ${fromStr} to ${toStr}`);
      }
      
      nextPageToken = result.next_page_token;
      page++;
    } while (nextPageToken);
    
    // Move to next chunk
    currentFrom = new Date(chunkEnd);
    currentFrom.setDate(currentFrom.getDate() + 1);  // Start next chunk from next day
  }
  
  Logger.log(`Found total ${allMeetings.length} recordings across all date chunks`);
  return { meetings: allMeetings };
}

// Download recording from Zoom
function downloadRecording(downloadUrl, fileName) {
  const token = getZoomToken();
  
  // First get download URL that doesn't require auth
  const options = {
    'method': 'get',
    'headers': {
      'Authorization': `Bearer ${token}`
    },
    'followRedirects': false
  };
  
  // Get the direct download URL from the redirect
  const response = UrlFetchApp.fetch(downloadUrl, options);
  if (response.getResponseCode() !== 302) {
    throw new Error('Expected redirect response from Zoom');
  }
  
  const directUrl = response.getHeaders()['Location'];
  Logger.log(`Got direct download URL: ${directUrl}`);
  
  // Return metadata for Drive import
  return {
    name: fileName,
    mimeType: 'video/mp4',
    downloadUrl: directUrl
  };
} 