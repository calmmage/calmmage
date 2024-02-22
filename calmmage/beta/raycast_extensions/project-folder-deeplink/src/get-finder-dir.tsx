import { getSelectedFinderItems, getFrontmostApplication } from "@raycast/api";
// import {open} from "@raycast/api";
// import { runAppleScript } from "@raycast/utils";
import fs from "node:fs/promises";
// import path from "node:path";
// import { newTab } from "./uri";

// const getSelectedPathFinderItems = async () => {
//   const script = `
//     tell application "Path Finder"
//       set thePaths to {}
//       repeat with pfItem in (get selection)
//         set the end of thePaths to POSIX path of pfItem
//       end repeat
//       return thePaths
//     end tell
//   `;

//   const paths = await runAppleScript(script);
//   return paths.split(",");
// };

// const fallback = async (): Promise<boolean> => {
//   const app = await getFrontmostApplication();

//   if (app.name !== "Finder") {
//     return false;
//   }

//   const currentDirectory = await runAppleScript(
//     `tell application "Finder" to get POSIX path of (target of front window as alias)`
//   );

//   if (!currentDirectory) {
//     return false;
//   }

// //   await open(newTab(currentDirectory));

//   return true;
// };

export const getFinderDir = async () => {
    console.log("Getting dir from Finder"); // Add console log message here
//   try {
    let selectedItems: { path: string }[] = [];

    const app = await getFrontmostApplication();

    if (app.name === "Finder") {
      selectedItems = await getSelectedFinderItems();
    // } else if (app.name === "Path Finder") {
    //   const paths = await getSelectedPathFinderItems();
    //   selectedItems = paths.map((p) => ({ path: p }));
    }

    if (selectedItems.length === 0) {
      // const ranFallback = await fallback();

      // if (ranFallback === false) {
      //   await showToast({
      //     style: Toast.Style.Failure,
      //     title: "No directory selected",
      //     message: "Please select a directory in Finder or Path Finder first",
      //   });
      // }

      return "";
    }
    
    const results = await Promise.all(selectedItems.map((item) => fs.stat(item.path).then((info) => ({ item, info }))));
    
    //    output the resulting path - just the first one for now
    return results[0].item.path;
// } catch (error: any) {
//     const errorMessage = error.toString() as string;
//     await showToast({
//         style: Toast.Style.Failure,
//         title: "Could not get selected directory",
//         message: errorMessage,
//     });
//     return undefined;
//   }
}