// Create nested folder structure
function createFolderPath(folderPath) {
  const parts = folderPath.split('/');
  let parent = DriveApp.getRootFolder();
  
  for (const part of parts) {
    const folders = parent.getFoldersByName(part);
    if (folders.hasNext()) {
      parent = folders.next();
    } else {
      parent = parent.createFolder(part);
    }
  }
  
  return parent;
}

// Save file to Drive
function saveFileToDrive(blob, folderPath) {
  const date = new Date();
  const folder = createFolderPath(`${date.getFullYear()}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${folderPath}`);
  
  const file = folder.createFile(blob);
  Logger.log(`Saved file: ${blob.getName()} to ${folderPath}`);
  return file;
} 