import {getPreferenceValues} from "@raycast/api";
import {exec, ExecException} from "child_process";
import {getFinderDir} from "./utils/get-finder-dir";
import {checkPathExists} from "./utils/path-utils";
import {getClipboardPath} from "./utils/clipboard-utils";
import {logWithHUD, logWithToast} from "./utils/raycast-utils";
import fs from "fs";

export interface App {
  key: string; // unique key
  title: string; // title to display
  name: string; // name of the app to call
  forceUseFolder: boolean; // if true - switch to parent folder if file is selected
}

const preferences = getPreferenceValues<Preferences>();

export const appsDict: { [key: string]: App } = {
  // todo: this is hacky way to add default app to the list of apps. 
  //  Should I rework this to avoid issues in the future?
  "" : { key: "", name: "", title: `Default (${preferences.defaultApp})`, forceUseFolder: false },
  // "subl": { key: "subl", name: "Sublime Text", title: "Sublime", forceUseFolder: false },
  "vscode": { key: "vscode", name: "Visual Studio Code", title: "VS Code", forceUseFolder: false },
  // "pycharm": { key: "pycharm", name: "PyCharm Professional Edition", title: "PyCharm", forceUseFolder: false },
  "warp": { key: "warp", name: "Warp", title: "Warp", forceUseFolder: true },
  "finder": { key: "finder", name: "Finder", title: "Finder", forceUseFolder: true },
  "auto": { key: "auto", name: "", title: "Auto", forceUseFolder: false },
};

const extraApps = preferences.extraApps?.split(',').map(app => app.trim()) || [];

for (const app of extraApps) {
  const key = app.split(" ")[0].toLowerCase();
  const name = app;
  const title = app.split(" ")[0];

  appsDict[key] = { key, title, name, forceUseFolder: false } as App;
}

// export function getAppsDict() {
//   return appsDict;
// }

// todo: if mode is 'auto' - use the appByRegexp to determine the app
// {'**.ts, **.tsx': 'vscode', '**.py': 'pycharm', 

// '**/.*': 'sublime'
// by default - sublime? Finder? 

// todo: add a preference to get the extra regesps from the user
// format: "**.ts: vscode, ..."
// Define a simple dictionary type
type AppRegexDict = { [pattern: string]: string };

const appByRegex: AppRegexDict = {
  // '**.ts': 'vscode',
  '**.tsx': 'vscode',
  // '**.py': 'pycharm',
  '**/.*': 'sublime',
  'default': 'sublime'
};

// // Example extra rules from preferences (mocked for demonstration)
// const preferences = {
//   extraRules: '**.ts:atom, **.py:pycharm'
// };

const extraRules = preferences.extraRules.split(',').map(rule => rule.trim());

for (const rule of extraRules) {
  const [pattern, app] = rule.split(':').map(part => part.trim());
  appByRegex[pattern] = app;
}

export function getAppByRegexp(filePath: string): string {
  for (const pattern in appByRegex) {
    // Convert glob pattern to RegExp pattern
    // todo: detect regexp style and abort if it's already a valid regexp. Or just apply both?
    let safePattern = pattern.replace(/\./g, '\\.');

    // Then, replace '**' with a broad match pattern
    // Use a placeholder for '**' that won't be affected by the next replacement
    safePattern = safePattern.replace(/\*\*/g, '<<double-star>>');

    // Replace '*' with a pattern to match any character except directory separators
    safePattern = safePattern.replace(/\*/g, '[^/\\\\]*');

    // Restore the '**' replacement with a pattern to match any sequence of characters
    safePattern = safePattern.replace(/<<double-star>>/g, '.*');

    const regex = new RegExp('^' + safePattern + '$');
    console.log(`Checking ${filePath} against ${regex}`);

    if (regex.test(filePath)) {
      return appByRegex[pattern];
    }
  }
  console.log(`No match found for ${filePath}`);
  // Default if no match is found
  // return appByRegex['default'];
  return '';
}

// export const isAppKeyValid = (key: string): boolean => {
//   return key !== "" && appsDict.hasOwnProperty(key);
// };

export const isValidAppKey = (key: string): boolean => key !== "" && Object.hasOwn(appsDict, key);


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

export const checkPathIsDirectory = (path: string) => {
  return fs.statSync(path).isDirectory();
}

export const openPathInApp = async (path: string, app: string) => {
  // check if path exists
  if (!checkPathExists(path)) {
    // todo: rewrite all logs to display output in Raycast
    const message = `Path does not exist: ${path}`;
    await logWithToast(message, "No path selected / Path does not exist");
    return;
  }
  if (!app) {
    app = preferences.defaultApp;
  }
  if (app == 'auto') {
    app = getAppByRegexp(path);
    if (!app) {
      app = preferences.defaultAutoApp;
    }
  }
  const appObj = getApp(app);
  await logWithHUD(`Opening ${path} in ${appObj.title}`);
  if (appObj.forceUseFolder && !checkPathIsDirectory(path)) {
    // console.error(`Error opening ${path} in ${appObj.title}: Path is not a directory`);
    path = path.split('/').slice(0, -1).join('/');

  }
  const command = `open -a "${appObj.name}" "${path}"`;

  exec(command, (error: ExecException | null, stdout: string, stderr: string) => {
    if (error) {
      console.error(`Error opening ${path} in ${appObj.title}: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Error opening ${path} in ${appObj.title}: ${stderr}`);
      return;
    }
    console.log(`Opened ${path} in ${appObj.title}`);
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
