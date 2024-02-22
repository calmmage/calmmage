
import { toolNameDict } from './core';
import { LaunchProps, showHUD, showToast, Toast } from "@raycast/api";
import { checkPathExists } from "./utils/path_utils";
import { createTinyURL, generateDeeplink } from "./utils/url_utils";
import { copyHyperlinkToClipboard, getClipboardPath } from "./utils/clipboard_utils";

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
    if (tool) {
        // deeplink = generateDeeplink(path, tool);
        if (!(tool in toolNameDict)) {
            console.log("Invalid tool specified");
            await showToast({
                style: Toast.Style.Failure,
                title: "Invalid tool specified",
                message: "Please provide a valid tool, values: " + Object.keys(toolNameDict).join(", ") + " or leave empty for default tool."
            });
            return;
        }
        deeplink = generateDeeplink({path: path, tool: tool}, "open-dir-manual");
    } else {
        deeplink = generateDeeplink({path: path}, "open-dir");
    }
    // console.log(`generating TinyURL`);
    const tinyurl = await createTinyURL(deeplink);
    // console.log(`TinyURL: ${tinyurl}`);
    let name = `Open ${path}`;
    // let name = `Open ${path}`.replace('/', '\\');
    // let name = path.split('/').pop() || 'dir';
    name = `Open ${name}`;
    if (tool) {
        name += ` in ${toolNameDict[tool]}`;
    }
    await copyHyperlinkToClipboard(name, tinyurl);
    
    console.log(`Copied to clipboard: ${tinyurl}: ${deeplink}`);
    showHUD(`Copied link to ${path}`);
}
