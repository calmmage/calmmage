
import { openPathInTool } from './core';
import { LaunchProps} from "@raycast/api";

// Command:  open the provided dir in the selected tool
export default function Command(props: LaunchProps<{ arguments?: Arguments.OpenDirManual }>) {
    const tool = props.arguments?.tool || "";
    // if tool is not prodived - use default one
    const path = props.arguments?.path || "";
    openPathInTool(path, tool);
    // // todo: go back in the navigation / cancel view
    // // try https://developers.raycast.com/api-reference/user-interface/navigation
    // return setTimeout(() => {
    //   useNavigation().pop();
    // }, 1000);
}
