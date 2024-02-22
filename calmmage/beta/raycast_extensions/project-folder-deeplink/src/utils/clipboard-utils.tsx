import { Clipboard } from "@raycast/api";

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
};
export const copyToClipboard = async (text: string) => {
  try {
    await Clipboard.copy(text);
  } catch (error) {
    console.log(`Could not write to clipboard. Reason: ${error}`);
  }
};

export async function copyHtmlToClipboard(html: string) {
  const htmlContent: Clipboard.Content = {
    html: html
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