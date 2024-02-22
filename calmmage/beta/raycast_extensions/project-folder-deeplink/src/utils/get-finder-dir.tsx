import { getSelectedFinderItems, getFrontmostApplication } from "@raycast/api";
import { runAppleScript } from "@raycast/utils";
import fs from "node:fs/promises";
import { logWithToast } from "./raycast-utils";

const getOpenedFinderDir = async (): Promise<string> => {
  const app = await getFrontmostApplication();

  if (app.name !== "Finder") {
    logWithToast("Finder is not currently the focused app", "No directory selected")
    return "";
  }

  const currentDirectory = await runAppleScript(
    `tell application "Finder" to get POSIX path of (target of front window as alias)`
  );

  if (!currentDirectory) {
    logWithToast("Could not get current directory from Finder", "No directory selected")
    return "";
  }

  return currentDirectory;
};

export const getFinderDir = async () => {
  console.log("Getting dir from Finder"); // Add console log message here
  let selectedItems: { path: string }[] = [];

  const app = await getFrontmostApplication();

  if (app.name === "Finder") {
    selectedItems = await getSelectedFinderItems();
  }

  if (selectedItems.length > 0) {
    const results = await Promise.all(selectedItems.map((item) => fs.stat(item.path).then((info) => ({ item, info }))));
    // output the resulting path - just the first one for now
    return results[0].item.path;
  } else {
    return await getOpenedFinderDir();
  }
}