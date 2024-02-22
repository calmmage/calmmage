import { checkPathExists, copyHyperlinkToClipboard, getClipboardPath } from './common';
import { generateDeeplink, toolNameDict } from './common';
import { LaunchProps, showHUD, showToast, Toast } from "@raycast/api";
import axios from 'axios';
import dotenv from 'dotenv';

// dotenv.config(); // Load environment variables from .env file
const filepath = "/Users/calm/work/code/structured/tools/calmmage/calmmage/beta/raycast_extensions/project-folder-deeplink/src/.env"
dotenv.config({ path: filepath })

// todo: set up the extension in the beginning - store token there
async function createTinyURL(longUrl: string): Promise<string> {
    console.log(`found api token: ${process.env.TINYURL_API_TOKEN}`)
    const response = await axios.post('https://api.tinyurl.com/create', {
        url: longUrl
    }, {
        headers: {
            'Authorization': `Bearer ${process.env.TINYURL_API_TOKEN}`,
            'Content-Type': 'application/json'
        }
    });
    
    return response.data.data.tiny_url;
}

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
    console.log(`Getting deeplink for ${path} in ${tool}`);
    const deeplink = generateDeeplink(path, tool);
    console.log(`generating TinyURL`);
    const tinyurl = await createTinyURL(deeplink);
    console.log(`TinyURL: ${tinyurl}`);
    let name = `Open ${path}`;
    // let name = `Open ${path}`.replace('/', '\\');
    // let name = path.split('/').pop() || 'dir';
    name = `Open ${name}`;
    if (tool) {
        name += ` in ${toolNameDict[tool]}`;
    }
    await copyHyperlinkToClipboard(name, tinyurl);
    
    console.log(`Copied to clipboard: ${tinyurl}: ${deeplink}`);
    showHUD(`Created deeplink to ${path}`);
}
