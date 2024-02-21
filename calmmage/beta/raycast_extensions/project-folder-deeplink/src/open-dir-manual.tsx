
import { openPathInTool } from './common';
import { LaunchProps } from "@raycast/api";
import OpenDir from './open-dir';

// Command:  open the provided dir in the selected tool
export default function Command(props: LaunchProps<{ arguments?: Arguments.OpenDirManual }>) {
    const tool = props.arguments?.tool || "";
    // todo: if tool is not prodived - show a selection menu. 
    if (!tool) {
      console.log("Tool not provided - showing the tool selection menu");
      return OpenDir(props);
    }
    const path = props.arguments?.path || "";
    openPathInTool(path, tool);
  }  
