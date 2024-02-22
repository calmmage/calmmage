
import { getPath, tools, toolNameDict, checkPathExists, openPathInTool, getClipboardPath} from './common';
import { Toast, showToast, ActionPanel, List, Action } from "@raycast/api";

import { LaunchProps } from "@raycast/api";

const openPathFromUserInTool = async (path: string, tool: string) => {
    // get clipboard path if no path provided
    if (!path) {
        path = await getPath();
    }

    // check exists
    if (!checkPathExists(path)) {
        await showToast({
            style: Toast.Style.Failure,
            title: "No path selected / path does not exist",
            message: "Please provide / copy a valid path to the clipboard first",
        });
        return;
    }

    return openPathInTool(path, tool);
}

// Command:  open the provided dir in the selected tool
export default function OpenDir(props: LaunchProps<{ arguments?: Arguments.OpenDir }>) {
    const path = props.arguments?.path || "";
    // if (!checkPathExists(path)) {
    // todo: check if path exists and if not - get path from clipboard (sync!!)
    return (
      <List>
        <List.Section title={`Opening ${path || "dir"}`} >
        {tools.map((tool) => (
          <List.Item
            key={tool}
            title={toolNameDict[tool]}
            // todo: add icons for each tool
            // https://developers.raycast.com/api-reference/user-interface/icons-and-images
            // icon="list-icon.png"
            actions={
              <ActionPanel>
                <Action
                  title={`Open in ${toolNameDict[tool]}`}
                  onAction={() => openPathFromUserInTool(path, tool)}
                />
              </ActionPanel>
            }
          />
        ))}
          </List.Section>
      </List>
    );
  }  
