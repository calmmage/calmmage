// TODO: Replace these hardcoded values with actual values from the Raycast API or system values
// const AUTHOR = "petr_lavrov";
import axios from "axios";
import { getPreferenceValues } from "@raycast/api";

const OWNER = "engineering-friends";
const DEEPLINK_TEMPLATE = `raycast://extensions/{owner}/{extension}/{command}?arguments={arguments}`;
const EXTENSION_NAME = "project-folder-deeplink";

export function generateDeeplink(argumentsObject: object, command: string): string {
  // URL-encode the arguments object
  const argumentsString = encodeURIComponent(JSON.stringify(argumentsObject));

  // Generate the base deeplink string
  return DEEPLINK_TEMPLATE
    .replace("{owner}", OWNER)
    .replace("{extension}", EXTENSION_NAME)
    .replace("{command}", command)
    .replace("{arguments}", argumentsString);
}

export async function createTinyURL(longUrl: string): Promise<string> {
const preferences = getPreferenceValues<Preferences>();
  const response = await axios.post("https://api.tinyurl.com/create", {
    url: longUrl
  }, {
    headers: {
      "Authorization": `Bearer ${preferences.tinyurlApiToken}`,
      "Content-Type": "application/json"
    }
  });

  return response.data.data.tiny_url;
}