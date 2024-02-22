import { Toast, closeMainWindow, showHUD, showToast } from "@raycast/api";
import { PopToRootType } from "@raycast/api";
import { showFailureToast } from "@raycast/utils";


// ------------------------------
// show hud
// ------------------------------
export async function logWithHUD(message: string) {
    console.log(message);
    await showHUD(message);
}


// ------------------------------
// show toast
// ------------------------------
export async function logWithToast(message: string, title: string = "Info") {
    console.log(title + ": " + message);
    await showToast({
        style: Toast.Style.Failure,
        title: title,
        message: message,
    });
}

// ------------------------------
// show failure toast
// ------------------------------
export async function logWithFailureToast(error: Error) {
    console.error(error);
    await showFailureToast(error);
}

// ------------------------------
// close main window
// ------------------------------
export function exitCommand() {
    closeMainWindow({ clearRootSearch: true , popToRootType: PopToRootType.Immediate});
}

// ------------------------------
// get preferences value
// ------------------------------
// export function getPreferencesValue(key: string) {
//     const preferences = getPreferenceValues<Preferences>();
    
//     return preferences[key];
// }
