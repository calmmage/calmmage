
import { openPathInApp } from './core';
import { LaunchProps} from "@raycast/api";
import { exitCommand } from "./utils/raycast-utils";

// Command:  open the provided dir in the selected tool
export default async function OpenDirManual(props: LaunchProps<{ arguments?: Arguments.OpenDirManual }>) {
    const app = props.arguments?.app || "";
    // if app is not prodived - use default one
    const path = props.arguments?.path || "";

    // exit navigation mode
    setTimeout(() => {
        exitCommand();
    }, 1000);

    await openPathInApp(path, app);
}
