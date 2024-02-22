import { showHUD, showToast, Toast } from "@raycast/api";
import { exec, ExecException } from "child_process";
import { getFinderDir } from "./get-finder-dir";
import dotenv from "dotenv";
import { checkPathExists } from "./utils/path_utils";
import { filepath } from "./utils/url_utils";
import { getClipboardPath } from "./utils/clipboard_utils";


export const tools = [
  "subl",
  "pycharm",
  "vscode",
  // "terminal", 
  "warp",
  "finder"
];

export const appNameDict: { [key: string]: string } = {
  "subl": "Sublime Text",
  "vscode": "Visual Studio Code",
  "pycharm": "PyCharm Professional Edition",
  // "terminal": "Terminal",
  "warp": "Warp",
  "finder": "Finder"
};

export const toolNameDict: { [key: string]: string } = {
  "subl": "Sublime",
  "vscode": "VS Code",
  "pycharm": "PyCharm",
  // "terminal": "Terminal",
  "warp": "Warp",
  "finder": "Finder"
};

// todo: add a way to set the default tool via Raycast
export const defaultTool = "vscode";

export const openPathInTool = async (path: string, tool: string) => {
  
  // check if path exists
  if (!checkPathExists(path)) {
    // todo: rewrite all logs to display output in Raycast
    const message = `Path does not exist: ${path}`;
    console.log(message);
    await showToast({
      title: "Path does not exist",
      message: message,
      style: Toast.Style.Failure
    });
    return;
  }

  let appName = appNameDict[tool];
  let toolName = toolNameDict[tool];
  if (!appName) {
    appName = appNameDict[defaultTool];
    toolName = toolNameDict[defaultTool];
    console.log(`Using default tool: ${toolName}`);
  }

  await showHUD(`Opening ${path} in ${toolName}`);
  console.log(`Opening ${path} in ${toolName}`);
  const command = "open -a \"" + appName + "\" " + path;

  exec(command, (error: ExecException | null, stdout: string, stderr: string) => {
    if (error) {
      console.error(`Error opening ${path} in ${appName}: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Error opening ${path} in ${appName}: ${stderr}`);
      return;
    }
    console.log(`Opened ${path} in ${appName}`);
  });

};

// export const isValidPath = (path: string) => {
//   // Check that a string is a valid path - 

//   return fs
//     .stat(path)
//     .then(() => true)
//     .catch(() => false);
// }

export const getPath = async () => {
  // discover path from available sources
  // 1. clipboard
  console.log("Getting path from clipboard");
  let path = await getClipboardPath();
  console.log("Path from clipboard: ", path);
  // check if path exists
  if (checkPathExists(path)) {
    return path;
  }
  
  console.log("Path from clipboard does not exist, getting path from Finder");
  // 2. selected items in Finder or Path Finder
  path = await getFinderDir();
  if (checkPathExists(path)) {
    return path;
  }

  console.log("Path from Finder does not exist, empty path");
  // 3. ask user
  // todo: implement this
  return "";


}

    
dotenv.config({ path: filepath })
    
