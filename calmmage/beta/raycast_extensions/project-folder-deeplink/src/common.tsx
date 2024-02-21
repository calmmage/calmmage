import { Clipboard } from "@raycast/api";
import fs from "fs";
// import { ActionPanel, List, Action } from "@raycast/api";
import { exec, ExecException } from "child_process";
import { getFinderDir } from "./get-finder-dir";

export const tools = [
  "pycharm",
  "vscode",
  // "terminal", 
  "warp", 
  "subl",
  "finder"
];

export const appNameDict: { [key: string]: string } = {
  "vscode": "Visual Studio Code",
  "pycharm": "PyCharm Professional Edition",
  // "terminal": "Terminal",
  "warp": "Warp",
  "subl": "Sublime Text",
  "finder": "Finder"
};

export const toolNameDict: { [key: string]: string } = {
  "vscode": "VS Code",
  "pycharm": "PyCharm",
  // "terminal": "Terminal",
  "warp": "Warp",
  "subl": "Sublime",
  "finder": "Finder"
};

// todo: add a way to set the default tool via Raycast
export const defaultTool = "vscode";

export const openPathInTool = (path: string, tool: string) => {
  
  //todo: check if path exists (broken now)
  // if (!fs.existsSync(path)) {
  //   // todo: rewrite all logs to display output in Raycast
  //   console.log(`Path does not exist: ${path}`);
  //   return;
  // }

  let appName = appNameDict[tool];
  let toolName = toolNameDict[tool];
  if (!appName) {
    appName = appNameDict[defaultTool];
    toolName = toolNameDict[defaultTool];
    console.log(`Using default tool: ${toolName}`);
  }

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
    console.log(`Opened ${path} in ${appName}: ${stdout}`);
  });

};

// export const isValidPath = (path: string) => {
//   // Check that a string is a valid path - 

//   return fs
//     .stat(path)
//     .then(() => true)
//     .catch(() => false);
// }

export const checkPathExists = (path: string) => {
  console.log(`Checking if path exists: ${path}`);
  path = path.trim();
  if (path === "") {
    return false;
  }
  console.log(`Path is not empty, proceeding: ${path}`);
  try {
    return fs.existsSync(path) || fs.existsSync(fs.realpathSync(path));
  } catch (error) {
    console.log(`Error checking path: ${error}`);
    return false;
  }
}

export const getClipboardPath = async () => {
  try {
    const path = await Clipboard.readText();
    if (path) {
      // strip any leading/trailing whitespace
      return path.trim();
    } else {
      console.log("Clipboard content is undefined");
      return "";
    }
  } catch (error) {
    console.log(`Could not read from clipboard. Reason: ${error}`);
  }
  return "";
}

export const copyToClipboard = async (text: string) => {
  try {
    await Clipboard.paste(text);
  } catch (error) {
    console.log(`Could not write to clipboard. Reason: ${error}`);
  }
}

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

// TODO: Replace these hardcoded values with actual values from the Raycast API or system values
// const AUTHOR = "petr_lavrov";
const OWNER = "engineering-friends";

const DEEPLINK_TEMPLATE = `raycast://extensions/{owner}/{extension}/{command}?arguments={arguments}`;
const EXTENSION_NAME = "project-folder-deeplink";
const COMMAND_NAME = "open-dir-manual";

// export generateDeeplink
// - raycast://extensions/<author-or-owner―<extension-name↔<command-name>
//     - "author": "petr_lavrov",
//     - "owner": "engineering-friends",
// - raycast://extensions/engineering-friends/project-folder-deeplink/open-dir-manual?arguments=
//     - arguments = URL-encoded JSON object.

export function generateDeeplink(tool: string, path: string): string {
  const argumentsObject = {
    path: path,
    tool: tool
  };

  // URL-encode the arguments object
  const argumentsString = encodeURIComponent(JSON.stringify(argumentsObject));

  // Generate the base deeplink string
  return DEEPLINK_TEMPLATE
    .replace("{owner}", OWNER)
    .replace("{extension}", EXTENSION_NAME)
    .replace("{command}", COMMAND_NAME)
    .replace("{arguments}", argumentsString);
}