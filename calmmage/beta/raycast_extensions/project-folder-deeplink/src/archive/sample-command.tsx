// Command: Open hardcoded path in the selected tool

import { tools, toolNameDict, openPathInApp} from '../core';
import { ActionPanel, List, Action } from "@raycast/api";

const hardcodedPath = "/Users/calm/work/code/structured/tools/calmmage/calmmage/beta/raycast_extensions/project-folder-deeplink/dev";


const openHardcodedPathInTool = (tool: string) => {
    return openPathInApp(hardcodedPath, tool);
}

// Command 1: Open path from clipboard in a tool
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
                  onAction={() => openHardcodedPathInTool(tool)}
                />
              </ActionPanel>
            }
          />
        ))}
      </List>
    );
  }