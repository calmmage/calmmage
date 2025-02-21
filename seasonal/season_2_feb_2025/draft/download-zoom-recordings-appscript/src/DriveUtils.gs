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
    // Create file in folder directly from blob
    const file = folder.createFile(fileMetadata.blob);
    file.setName(fileMetadata.name);  // Set proper name
    
    // Add source info as property
    file.setDescription(`Zoom recording downloaded at: ${new Date().toISOString()}`);
    
    Logger.log(`Created file: ${file.getName()} (${file.getSize()} bytes)`);
    return file;
  } catch (e) {
    Logger.log(`Error saving file: ${e.toString()}`);
    throw e;
  }
} 