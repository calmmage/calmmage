
import { getPath, appsDict, openPathInApp} from './core';
import { ActionPanel, List, Action } from "@raycast/api";
import { LaunchProps } from "@raycast/api";
import { exitCommand } from './utils/raycast-utils';

const openPathFromUserInApp = async (path: string, tool: string) => {
  // get clipboard path if no path provided
  if (!path) {
    path = await getPath();
  }

  // exit navigation mode
  setTimeout(() => {
    exitCommand();
  }, 1000);

  await openPathInApp(path, tool);
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


// Command:  open the provided dir in the selected tool
export default function OpenDir(props: LaunchProps<{ arguments?: Arguments.OpenDir }>) {
    const path = props.arguments?.path || "";
    
    // if (!checkPathExists(path)) {
    // todo: check if path exists and if not - get path from clipboard (sync!!)
    // try https://developers.raycast.com/utilities/react-hooks/usepromise

    return (
      <List>
        <List.Section title={`Opening ${path || "dir"}`} >
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
                    openPathFromUserInApp(path, app.key);
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
