import { appsDict, openPathInApp } from "../core";
import { Toast, showToast, ActionPanel, List, Action } from "@raycast/api";
import { checkPathExists } from "../utils/path-utils";
import { getClipboardPath } from "../utils/clipboard-utils";
// import { usePromise } from "@raycast/utils";

const openPathFromClipboardInTool = async (tool: string) => {
    // get clipboard path
    const path = await getClipboardPath();

    // check exists
    if (!checkPathExists(path)) {
        await showToast({
            style: Toast.Style.Failure,
            title: "No directory selected / path does not exist",
            message: "Please copy a valid directory path to the clipboard first",
        });
        return;
    }

    return openPathInApp(path, tool);
}


// ------------------------------
// usePromise example:
// ------------------------------
// import { Detail, ActionPanel, Action } from "@raycast/api";
// import { usePromise } from "@raycast/utils";
// import { useEffect, useState } from "react";

// async function getClipboardPath() {
//   // Async logic to get clipboard path
// }

// export default function Command() {
//   const [clipboardData, setClipboardData] = useState("");
//   const { isLoading, data, revalidate } = usePromise(getClipboardPath, []);

//   useEffect(() => {
//     if (data) {
//       setClipboardData(data);
//     }
//   }, [data]);

//   return (
//     <Detail
//       isLoading={isLoading}
//       markdown={clipboardData}
//       actions={
//         <ActionPanel>
//           <Action title="Reload" onAction={() => revalidate()} />
//         </ActionPanel>
//       }
//     />
//   );
// }


// Command: open the path in clipboard in the selected tool
export default function Command() {
    // const path = usePromise(getClipboardPath, { loadingMessage: "Getting path from clipboard" });

    return (
      <List>
          <List.Section title={`Opening dir from clipboard`} >
              {Object.values(appsDict).map((app) => (
                <List.Item
                  key={app.key}
                  title={app.title}
                  // todo: add icons for each tool
                  // https://developers.raycast.com/api-reference/user-interface/icons-and-images
                  // icon="list-icon.png"
                  actions={
                      <ActionPanel>
                          <Action
                            title={`Open in ${app.title}`}
                            onAction={() => {
                                openPathFromClipboardInTool(app.key);
                                // closeMainWindow();
                            }
                            }
                          />
                      </ActionPanel>
                  }
                />
              ))}
          </List.Section>
      </List>
    );
  }