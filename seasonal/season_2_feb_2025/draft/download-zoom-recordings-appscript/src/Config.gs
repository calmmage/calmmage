// Get Zoom configuration from Script Properties
function getZoomConfig() {
  const scriptProperties = PropertiesService.getScriptProperties();
  return {
    accountId: scriptProperties.getProperty('ZOOM_ACCOUNT_ID'),
    clientId: scriptProperties.getProperty('ZOOM_CLIENT_ID'),
    clientSecret: scriptProperties.getProperty('ZOOM_CLIENT_SECRET'),
    userId: scriptProperties.getProperty('ZOOM_USER_ID')
  };
}

// Setup Zoom credentials in Script Properties
function setupZoomCredentials(accountId, clientId, clientSecret, userId) {
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperties({
    'ZOOM_ACCOUNT_ID': accountId,
    'ZOOM_CLIENT_ID': clientId,
    'ZOOM_CLIENT_SECRET': clientSecret,
    'ZOOM_USER_ID': userId
  });
  Logger.log('Zoom credentials have been set up successfully');
} 