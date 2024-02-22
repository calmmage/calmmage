import fs from "fs";

export const checkPathExists = (path: string) => {
  console.log(`Checking if path exists: "${path}"`);
  path = path.trim();
  if (path.includes("\n")) {
    console.log("Path contains multiple lines, returning false");
    return false;
  }

  if (path === "") {
    console.log("Path is empty, returning false");
    return false;
  }
  // console.log(`Path is not empty, proceeding: ${path}`);
  // todo: figure out how to handle this better
  //  - for now realpathSync is used to resolve symlinks
  //  - but on missing paths it always throws an error
  //  so it's either true or an error - clunky. But works.
  try {
    return fs.existsSync(fs.realpathSync(path));
  } catch (error) {
    console.log(`Error checking path: ${error}`);
    return false;
  }
};