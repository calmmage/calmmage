# Project Arrangement TODOs

1. Implement GitHub repository discovery
   - Add GitHub API integration
   - Fetch all repositories for the user
   - Handle pagination
   - Store GitHub tokens securely

2. Add search for git repositories outside default paths
   - Implement recursive search in specified directories
   - Add configurable ignore patterns
   - Handle permissions and symbolic links
   - Add progress bar for long searches

3. Implement deduplication logic
   - Compare projects by name and contents
   - Handle cases where same project exists in multiple locations
   - Create report of duplicates

4. Add project metadata and annotations
   - Last commit date
   - Project size
   - Programming languages used
   - README contents summary
   - Custom tags/notes 
