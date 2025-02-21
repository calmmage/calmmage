# Core Features

1. "find emails from zoom about recordings -> extract link and password"
    - Already implemented in notes.md
    - Consider adding error handling for expired links

2. "Download via zoom api"
    - Research Zoom API authentication
    - Implement recording download endpoint
    - Compare email-based vs API-based approaches

3. "Upload to google drive/YouTube"
    - Implement Google Drive upload first (simpler)
    - Add YouTube upload as optional enhancement

4. "rolling monitoring"
    - Add time-based trigger
    - Track processed recordings
    - Filter out already processed items

# Implementation Notes

Email vs API approaches:

- Email: already working, but links may expire
- Zoom API: more reliable, but requires setup
- Consider supporting both methods

Deployment options:

- Package as Google Apps Script for easy sharing
- Store credentials securely
- Provide simple setup instructions

# Next Steps

Focus on implementing the download functionality first, then proceed with upload
features. 