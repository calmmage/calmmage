import { Detail } from "@raycast/api";
// import { readFileSync } from "fs";

export default function Command() {
  // const markdownContent = readFileSync("resources/sample_markdown.md", "utf-8");
  const markdownContent = "# Hey! 👋"
  return <Detail markdown={markdownContent} />;
}
