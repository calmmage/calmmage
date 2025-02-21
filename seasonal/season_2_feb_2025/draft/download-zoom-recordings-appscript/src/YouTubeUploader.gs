// Upload video to YouTube
function uploadToYouTube(driveFile, title, description = '') {
  if (!isYouTubeEnabled()) {
    throw new Error(
      'YouTube API is not enabled. Please enable YouTube Data API v3:\n' +
      '1. Click "+" next to Services\n' +
      '2. Find and add "YouTube Data API v3"\n' +
      '3. Enable it in Google Cloud Console if prompted'
    );
  }

  try {
    // Get file content as blob
    const blob = DriveApp.getFileById(driveFile.getId()).getBlob();
    
    // Upload to YouTube
    const youtube = YouTube.Videos.insert({
      snippet: {
        title: title,
        description: description || `Zoom recording from ${title.split(' - ')[0]}`
      },
      status: {
        privacyStatus: 'unlisted'
      }
    }, 'snippet,status', blob);
    
    Logger.log(`Video uploaded to YouTube: ${youtube.id}`);
    return youtube.id;
  } catch (e) {
    Logger.log(`Error uploading to YouTube: ${e.toString()}`);
    throw e;
  }
}

// Check if YouTube API is enabled
function isYouTubeEnabled() {
  try {
    // Try to access the YouTube service - will throw if not enabled
    return Boolean(YouTube?.Videos);
  } catch (e) {
    Logger.log('YouTube API not enabled: ' + e.toString());
    return false;
  }
} 