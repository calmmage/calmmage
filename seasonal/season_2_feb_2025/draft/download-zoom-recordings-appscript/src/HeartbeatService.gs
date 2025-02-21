// Constants
const DEFAULT_SERVICE_REGISTRY_URL = 'https://service-registry.calmmage.com';

// Send a single heartbeat to the service registry
function sendHeartbeat(serviceKey) {
  try {
    // Normalize service key (remove spaces, convert to lowercase)
    serviceKey = serviceKey.replace(/\s+/g, '-').toLowerCase();
    
    const options = {
      'method': 'post',
      'contentType': 'application/json',
      'payload': JSON.stringify({
        'service_key': serviceKey
      })
    };
    
    const response = UrlFetchApp.fetch(`${DEFAULT_SERVICE_REGISTRY_URL}/heartbeat`, options);
    
    if (response.getResponseCode() === 200) {
      Logger.log(`Heartbeat sent successfully for ${serviceKey}`);
      return true;
    } else {
      Logger.log(`Failed to send heartbeat for ${serviceKey}: HTTP ${response.getResponseCode()}`);
      return false;
    }
  } catch (e) {
    Logger.log(`Error sending heartbeat for ${serviceKey}: ${e.toString()}`);
    return false;
  }
} 