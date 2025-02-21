// Create folder if it doesn't exist
function getOrCreateFolder(folderName) {
  const folders = DriveApp.getRootFolder().getFoldersByName(folderName);
  if (folders.hasNext()) {
    return folders.next();
  }
  return DriveApp.getRootFolder().createFolder(folderName);
}

// Save file to Drive using URL import
function saveFileToDrive(fileMetadata) {
  const folder = getOrCreateFolder('Zoom Recordings');
  
  try {
    // Download file first since Drive API needs a Blob
    const response = UrlFetchApp.fetch(fileMetadata.downloadUrl);
    const blob = response.getBlob();
    
    // Create file in folder
    const file = folder.createFile(blob);
    file.setName(fileMetadata.name);  // Set proper name
    
    // Add source URL as property
    file.setDescription(`Zoom recording downloaded from: ${fileMetadata.downloadUrl}`);
    
    Logger.log(`Created file: ${file.getName()} (${file.getSize()} bytes)`);
    return file;
  } catch (e) {
    Logger.log(`Error saving file: ${e.toString()}`);
    throw e;
  }
} 