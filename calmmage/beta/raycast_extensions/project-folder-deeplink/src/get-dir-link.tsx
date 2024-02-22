
import { appsDict, getApp, getAppByRegexp, getPath, isValidAppKey } from './core';

import { LaunchProps } from "@raycast/api";
import { checkPathExists } from "./utils/path-utils";
import { createTinyURL, generateDeeplink } from "./utils/url-utils";
import { copyHyperlinkToClipboard } from "./utils/clipboard-utils";
import { logWithHUD, logWithToast } from './utils/raycast-utils';

export default async function GetDirLink(props: LaunchProps<{ arguments?: Arguments.GetDirLink }>) {
    let path = props.arguments?.path || "";
    // if path is empty - get path from clipboard / current dir 
    if (!path) {
        path = await getPath();
        // console.log("Path not provided - getting path from clipboard");    
        // try {
        //     path = await getClipboardPath();
        // } catch (error) {
        //     console.log(`Could not get path from clipboard. Reason: ${error}`);
        //     await showToast({
        //         style: Toast.Style.Failure,
        //         title: "Failed to get path from clipboard",
        //         message: "error: " + error,
        //     });
        //     return;
        // }
    }
    // check if path exists
    if (!checkPathExists(path)) {
        await logWithToast("Please provide or copy a valid path to the clipboard first", "No path provided / path does not exist");
        return;
    }

    let app = props.arguments?.app || "";
    let deeplink = undefined;
    // let name = `Open ${path}`;
    // let name = `Open ${path}`.replace('/', '\\');
    let name = `Open ${path.split('/').pop() || 'dir'}`;
    if (!app || app === "auto") {
        app = getAppByRegexp(path);
        if (!app) {
            console.log(`Could not find app for path: ${path}`);
            deeplink = generateDeeplink({path: path}, "open-dir");
        } else {
            console.log(`Found app for path: ${path} - ${app}`)
            if (!isValidAppKey(app)) {
                logWithToast(`Invalid app key: ${app}, available keys: ${Object.keys(appsDict)}`, "Invalid app key");
                return;
            }
            deeplink = generateDeeplink({path: path, app: app}, "open-dir-manual");
            name += ` in ${getApp(app).title}`;
        }
    } else {
        if (!isValidAppKey(app)) {
            logWithToast(`Invalid app key: ${app}, available keys: ${Object.keys(appsDict)}`, "Invalid app key");
            return;
        }
        deeplink = generateDeeplink({path: path, app: app}, "open-dir-manual");
        name += ` in ${getApp(app).title}`;
    } 
    // console.log(`generating TinyURL`);
    const tinyurl = await createTinyURL(deeplink);
    // console.log(`TinyURL: ${tinyurl}`);
    await copyHyperlinkToClipboard(name, tinyurl);
    
    logWithHUD(`Copied link to ${path}: ${tinyurl}`);
}
