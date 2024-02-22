import { getPreferenceValues } from "@raycast/api";
import { exec, ExecException } from "child_process";
import { getFinderDir } from "./utils/get-finder-dir";
import { checkPathExists } from "./utils/path-utils";
import { getClipboardPath } from "./utils/clipboard-utils";
import { logWithHUD, logWithToast } from "./utils/raycast-utils";

export interface App {
  key: string; // unique key
  title: string; // title to display
  name: string; // name of the app to call
}

const preferences = getPreferenceValues<Preferences>();

export const appsDict: { [key: string]: App } = {
  // todo: this is hacky way to add default app to the list of apps. 
  //  Should I rework this to avoid issues in the future?
  "" : { key: "", name: "", title: `Default (${preferences.defaultApp})` },
  // "subl": { key: "subl", name: "Sublime Text", title: "Sublime" },
  "vscode": { key: "vscode", name: "Visual Studio Code", title: "VS Code" },
  // "pycharm": { key: "pycharm", name: "PyCharm Professional Edition", title: "PyCharm" },
  // "warp": { key: "warp", name: "Warp", title: "Warp" },
  "finder": { key: "finder", name: "Finder", title: "Finder" }
};

const extraApps = preferences.extraApps?.split(',').map(app => app.trim()) || [];

for (const app of extraApps) {
  const key = app.split(" ")[0].toLowerCase();
  const name = app;
  const title = app.split(" ")[0];

  appsDict[key] = { key, title, name } as App;
}

export function getAppsDict() {
  return appsDict;
}

export const getApp = (key: string): App => {
  const preferences = getPreferenceValues<Preferences>();
  // If key is empty, return the default app
  if (!key) {
    return appsDict[preferences.defaultApp];
  }

  // If key is not in appsDict, throw an error and show available keys
  if (!appsDict[key]) {
    const availableKeys = Object.keys(appsDict).join(", ");
    throw new Error(`Invalid key. Available keys are: ${availableKeys}`);
  }

  // Return the app corresponding to the key
  return appsDict[key];
};

export const openPathInApp = async (path: string, tool: string) => {
  // check if path exists
  if (!checkPathExists(path)) {
    // todo: rewrite all logs to display output in Raycast
    const message = `Path does not exist: ${path}`;
    await logWithToast(message, "No path selected / Path does not exist");
    return;
  }

  const app = getApp(tool);
  await logWithHUD(`Opening ${path} in ${app.title}`);
  const command = `open -a "${app.name}" ${path}`;

  exec(command, (error: ExecException | null, stdout: string, stderr: string) => {
    if (error) {
      console.error(`Error opening ${path} in ${app.title}: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Error opening ${path} in ${app.title}: ${stderr}`);
      return;
    }
    console.log(`Opened ${path} in ${app.title}`);
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


};
