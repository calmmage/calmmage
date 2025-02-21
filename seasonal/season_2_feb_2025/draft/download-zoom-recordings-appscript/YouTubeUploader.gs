// Upload video to YouTube
function uploadToYouTube(videoBlob, title, description = '') {
  try {
    const youtube = YouTube.Videos.insert({
      snippet: {
        title: title,
        description: description || `Zoom recording from ${title.split(' - ')[0]}`
      },
      status: {
        privacyStatus: 'unlisted'
      }
    }, 'snippet,status', videoBlob);
    
    Logger.log(`Video uploaded to YouTube: ${youtube.id}`);
    return youtube.id;
  } catch (e) {
    Logger.log(`Error uploading to YouTube: ${e.toString()}`);
    throw e;
  }
}

// Enable YouTube API
function enableYouTubeService() {
  try {
    const service = ScriptApp.getService('YouTube');
    if (!service) {
      Logger.log('YouTube API service is not enabled. Please enable it in Advanced Google Services.');
      return false;
    }
    return true;
  } catch (e) {
    Logger.log('Error checking YouTube service: ' + e.toString());
    return false;
  }
} 