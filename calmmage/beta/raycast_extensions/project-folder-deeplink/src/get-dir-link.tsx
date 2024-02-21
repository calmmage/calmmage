// import { showToast, ToastStyle } from "@raycast/api";
// import { contents, update } from "./util/clipboard";
// // import { encode } from "js-base64";
// export default async () => {
//   try {
//     const clipboard = await contents();
//     const encoded = "data";
//     await update(encoded);
//   } catch (e) {
//     if (typeof e === "string") {
//       await showToast(ToastStyle.Failure, "Encode failed", e);
//     }
//   }
// };


// import clipboardy from 'clipboardy';
import { generateDeeplink, copyToClipboard } from './common';
import { LaunchProps, showHUD } from "@raycast/api";
// import { Detail } from "@raycast/api";
// import OpenDir from './open-dir';

// const generateDeeplink = async (path: string, tool: string) => {
//     const deeplink = ge
  
//       // get clipboard path if no path provided
//       if (!path) {
//           path = await getPath();
//       }
  
//       // check exists
//       if (!checkPathExists(path)) {
//           await showToast({
//               style: Toast.Style.Failure,
//               title: "No path selected / path does not exist",
//               message: "Please provide / copy a valid path to the clipboard first",
//           });
//           return;
//       }
  
//       return openPathInTool(path, tool);
//   }

// Command: get a raycast deeplink to the path in clipboard
// export default function Command() {
//     const path = await getClipboardPath();
//     if (!path) {
//         await showToast({
//             style: Toast.Style.Failure,
//             title: "No path in clipboard",
//             message: "Please copy a valid path to the clipboard first",
//         });
//         return;
//     }
//     return generateDeeplink(path, );
// }



// Command:  open the provided dir in the selected tool
// export default async function Command(props: LaunchProps<{ arguments?: Arguments.OpenDirManual }>) {
    // export async function Command1(props: LaunchProps<{ arguments?: Arguments.GetDirLink }>) {
    //     const tool = props.arguments?.tool || "";
    //     // todo: if tool is not prodived - show a selection menu. 
    //     // if (!tool) {
    //     //   console.log("Tool not provided - showing the tool selection menu");
    //     //   return OpenDir(props);
    //     // } 
    //     const path = props.arguments?.path || "";
    //     // return openPathInTool(path, tool);
    //     const deeplink = await generateDeeplink(path, tool);
    
    //     // todo 1: copy the deeplink to clipboard
    //     await copyToClipboard(deeplink);
    
    //     // todo 2: show a toast with the deeplink? 
    //     // await showToast({
    //     //     style: Toast.Style.Success,
    //     //     title: "Deeplink copied to clipboard",
    //     //     message: deeplink,
    //     // });
    
    //     // todo 3: display the deeplink in the Raycast window
    //     // return deeplink;
    //     return (
    //         <Detail markdown={deeplink} />
    //     )
    //   }  

// function generateDeeplink(path: string, tool: string) {
//     return `raycast://open?path=${path}&tool=${tool}`;
// }

// const copyToClipboard = async(text: string) => {
//     return `Copied to clipboard: ${text}`;
// }


// import clipboardy from 'clipboardy';

// export const copyRichTextToClipboard = (html: string) => {
//     clipboardy.writeSync(html);
// }

// export const copyLinkToClipboard = (text: string, url: string) => {
//     const hyperlink = `[${text}](${url})`;
//     clipboardy.writeSync(hyperlink);
// }

// const copyHyperlinkToClipboard = (text: string, url: string) => {
//     const hyperlink = `[${text}](${url})`;
//     clipboardy.writeSync(hyperlink);
// }

  
// export default async function GetDirLink(props: LaunchProps<{ arguments?: Arguments.GetDirLink }>) {
//     const path = props.arguments?.path || "";
//     const tool = props.arguments?.tool || "";
//     console.log(`Getting deeplink for ${path} in ${tool}`);
//     const deeplink = generateDeeplink(path, tool);
//     // await copyToClipboard(deeplink);
//     copyHyperlinkToClipboard(path, deeplink);
//     console.log(`Copied to clipboard: ${deeplink}`);
//     // return <Detail markdown={deeplink} />;
//     // return <Detail markdown="Hey! test" />;
//     await showHUD(`Created deeplink: ${deeplink}`);
//     console.log(`Showed HUD: Created deeplink: ${deeplink}`);

// }

  
export default async function GetDirLink(props: LaunchProps<{ arguments?: Arguments.GetDirLink }>) {
    const path = props.arguments?.path || "";
    const tool = props.arguments?.tool || "";
    console.log(`Getting deeplink for ${path} in ${tool}`);
    const deeplink = generateDeeplink(path, tool);
    await copyToClipboard(deeplink);
    // copyHyperlinkToClipboard(path, deeplink);
    console.log(`Copied to clipboard: ${deeplink}`);
    // return <Detail markdown={deeplink} />;
    // return <Detail markdown="Hey! test" />;
    await showHUD(`Created deeplink: ${deeplink}`);
    console.log(`Showed HUD: Created deeplink: ${deeplink}`);
    
}