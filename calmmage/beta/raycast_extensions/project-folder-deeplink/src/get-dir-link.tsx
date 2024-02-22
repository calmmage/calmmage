
import { getApp } from './core';

import { LaunchProps, showHUD, showToast, Toast } from "@raycast/api";
import { checkPathExists } from "./utils/path-utils";
import { createTinyURL, generateDeeplink } from "./utils/url-utils";
import { copyHyperlinkToClipboard, getClipboardPath } from "./utils/clipboard-utils";

export default async function GetDirLink(props: LaunchProps<{ arguments?: Arguments.GetDirLink }>) {
    let path = props.arguments?.path || "";
    // if path is empty - get path from clipboard / current dir 
    if (!path) {
        console.log("Path not provided - getting path from clipboard");    
        try {
            path = await getClipboardPath();
        } catch (error) {
            console.log(`Could not get path from clipboard. Reason: ${error}`);
            await showToast({
                style: Toast.Style.Failure,
                title: "Failed to get path from clipboard",
                message: "error: " + error,
            });
            return;
        }
    }
    // check if path exists
    if (!checkPathExists(path)) {
        console.log("Path does not exist, empty path");
        await showToast({
            style: Toast.Style.Failure,
            title: "No directory selected / path does not exist",
            message: "Please provide or copy a valid path to the clipboard first",
        });
        return;
    }

    const tool = props.arguments?.tool || "";
    let deeplink = undefined;
    let app = undefined;
    let name = `Open ${path}`;
    // let name = `Open ${path}`.replace('/', '\\');
    // let name = path.split('/').pop() || 'dir';
    name = `Open ${name}`;
    if (tool) {
        try {
            app = getApp(tool);
            deeplink = generateDeeplink({path: path, tool: tool}, "open-dir-manual");
            name += ` in ${app.title}`;
        } catch (error) {
            console.log(`Could not get app for tool: ${tool}. Reason: ${error}`);
            await showToast({
                style: Toast.Style.Failure,
                title: "Could not get app for tool",
                message: "tool: " + tool + ", error: " + error,
            });
            return;
        }
    } else {
        deeplink = generateDeeplink({path: path}, "open-dir");
    }
    // console.log(`generating TinyURL`);
    const tinyurl = await createTinyURL(deeplink);
    // console.log(`TinyURL: ${tinyurl}`);
    await copyHyperlinkToClipboard(name, tinyurl);
    
    console.log(`Copied to clipboard: ${tinyurl}: ${deeplink}`);
    showHUD(`Copied link to ${path}`);
}
