import { Detail } from "@raycast/api";
import { readFileSync } from "fs";

export default function Command() {
  // const markdownContent = readFileSync("resources/sample_markdown.md", "utf-8");
  const path= "/Users/calm/work/code/structured/tools/calmmage/calmmage/beta/raycast_extensions/hello-world-package/src/resources/sample_markdown.md"
  console.log("path", path)
  // const markdownContent = "# Hey! 👋"
  const markdownContent = readFileSync(path, "utf-8");
  console.log("markdownContent", markdownContent)
  
  return <Detail markdown={markdownContent} />;
}
