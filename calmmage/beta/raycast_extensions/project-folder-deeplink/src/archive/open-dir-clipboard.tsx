import { tools, toolNameDict, openPathInTool} from '../core';
import { Toast, showToast, ActionPanel, List, Action } from "@raycast/api";
import { checkPathExists } from "../utils/path_utils";
import { getClipboardPath } from "../utils/clipboard_utils";

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

    return openPathInTool(path, tool);
}

// Command: open the path in clipboard in the selected tool
export default function Command() {
    return (
      <List>
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
                  onAction={() => openPathFromClipboardInTool(tool)}
                />
              </ActionPanel>
            }
          />
        ))}
      </List>
    );
  }