import { Clipboard, showToast, Toast } from "@raycast/api";
import fs from "fs";
// import { ActionPanel, List, Action } from "@raycast/api";
import { exec, ExecException } from "child_process";
import { getFinderDir } from "./get-finder-dir";
import { showHUD } from "@raycast/api";


export const checkPathExists = (path: string) => {
  console.log(`Checking if path exists: "${path}"`);
  path = path.trim();
  if (path.includes("\n")) {
    console.log("Path contains multiple lines, returning false");
    return false;
  }

  if (path === "") {
    console.log("Path is empty, returning false");
    return false;
  }
  // console.log(`Path is not empty, proceeding: ${path}`);
  // todo: figure out how to handle this better 
  //  - for now realpathSync is used to resolve symlinks 
  //  - but on missing paths it always throws an error
  //  so it's either true or an error - clunky. But works.
  try {
    return fs.existsSync(fs.realpathSync(path));
  } catch (error) {
    console.log(`Error checking path: ${error}`);
    return false;
  }
}

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
  
  //todo: check if path exists (broken now)
  if (!checkPathExists(path)) {
  //   // todo: rewrite all logs to display output in Raycast
    const message = `Path does not exist: ${path}`;
    console.log(message);
    showToast({
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

export const getClipboardPath = async () => {
  try {
    let path = await Clipboard.readText() || "";
    path = path.trim();
    if (path) {
      // strip any leading/trailing whitespace
      return path;
    } else {
      const msg = "Clipboard content is empty";
      console.log(msg);
      throw new Error(msg);
      // return "";
    }
  } catch (error) {
    const msg = `Could not read from clipboard. Reason: ${error}`;
    console.log(msg);
    throw new Error(msg);
    // return "";
  }
}

export const copyToClipboard = async (text: string) => {
  try {
    await Clipboard.copy(text);
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

export function generateDeeplink(path: string, tool: string): string {
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

export async function copyHtmlToClipboard(html: string) {
  const htmlContent: Clipboard.Content = {
    html: html,
  };
  await Clipboard.copy(htmlContent);
// console.log('HTML copied to clipboard');
}
  
export async function copyHyperlinkToClipboard(name: string, link: string) {
    // const hyperlink = `[${name}](${link})`;
    const hyperlink = `<a href="${link}">${name}</a>`;
    await copyHtmlToClipboard(hyperlink);
    // console.log(`Copied to clipboard: ${hyperlink}`);
    }