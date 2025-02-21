// Constants
const EMAIL_SUBJECT_PATTERNS = {
  en: ['Zoom Cloud Recording', 'is now available'],
  ru: ['Облачная запись Zoom', 'теперь доступна']
};

// Find Zoom recording notification emails
function findZoomEmails(maxResults = 10) {
  const queries = EMAIL_SUBJECT_PATTERNS.map(([part1, part2]) => 
    `subject:("${part1}" "${part2}")`
  ).join(' OR ');
  
  return GmailApp.search(queries, 0, maxResults);
}

// Send notification with video links
function sendVideoLinks(topic, date, driveLink, youtubeLink, originalThread) {
  const subject = `Zoom Recording Processed: ${topic}`;
  let body = `Your Zoom recording from ${date} has been processed:\n\n`;
  
  if (driveLink) {
    body += `Google Drive: ${driveLink}\n`;
  }
  if (youtubeLink) {
    body += `YouTube: ${youtubeLink}\n`;
  }
  
  body += '\nOriginal recording will be automatically deleted from Zoom after 30 days.';
  
  if (originalThread) {
    // Reply to original email
    originalThread.replyAll(body);
    Logger.log(`Replied to original email thread for: ${topic}`);
  } else {
    // Send new email to user
    const userEmail = Session.getEffectiveUser().getEmail();
    GmailApp.sendEmail(userEmail, subject, body);
    Logger.log(`Sent new email notification for: ${topic}`);
  }
}

// Find original notification email for a recording
function findOriginalEmail(topic, date) {
  const dateStr = new Date(date).toISOString().split('T')[0];
  const searchQuery = `subject:"${topic}" before:${dateStr}`;
  
  const threads = GmailApp.search(searchQuery, 0, 1);
  return threads.length > 0 ? threads[0] : null;
}

// Process email notification for a recording
function notifyVideoProcessed(date, topic, driveLink = '', youtubeLink = '') {
  try {
    const originalThread = findOriginalEmail(topic, date);
    sendVideoLinks(topic, date, driveLink, youtubeLink, originalThread);
    return true;
  } catch (e) {
    Logger.log(`Error sending notification for ${topic}: ${e.toString()}`);
    return false;
  }
} 