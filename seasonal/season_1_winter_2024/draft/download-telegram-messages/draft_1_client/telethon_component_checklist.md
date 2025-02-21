## Extra, do not forget

- [ ] add a simplified way to set up telethon client for just a single user.. ? Nah, i
  think I'm good with just storing the session to disk for now.

## Telethon Manager Component Implementation Checklist

### 1. Create Component Files

- [x] Create `botspot/botspot/components/telethon_manager.py`
    - [x] Move TelethonManager class
    - [x] Add TelethonManagerSettings class
    - [x] Add setup_dispatcher function
    - [x] Add initialization function
    - [x] Add component-specific utilities

### 2. Add Component to Core Files

- [x] Add to `botspot/botspot/core/botspot_settings.py`
    - [x] Import TelethonManagerSettings
    - [x] Add to BotspotSettings class

- [x] Add to `botspot/botspot/core/dependency_manager.py`
    - [x] Add telethon_manager property
    - [x] Add telethon_manager setter

- [x] Add to `botspot/botspot/core/bot_manager.py`
    - [x] Import telethon_manager component
    - [x] Add initialization in __init__
    - [x] Add setup in setup_dispatcher

### 3. Create Example Files

- [x] Create `botspot/examples/components_examples/telethon_manager_example/`
    - [x] Create `main.py` with usage examples
    - [x] Create `README.md` with setup instructions
    - [x] Create example `.env` template as 'sample.env'

### 4. Add Utility Functions

- [x] Add to `botspot/botspot/utils/deps_getters.py`
    - [x] Add get_telethon_manager utility function

### 5. Update Existing Code

- [x] Modify `dev.py`
    - [x] Remove TelethonManager class
    - [x] Update imports
    - [x] Update usage to use component
    - [x] add .env flag and other necessary configs

## Future Improvements

### Command Menu Integration

- [ ] Add support for nested commands in bot_commands_menu component
    - [ ] Allow multiple handlers for the same command
    - [ ] Create a command hierarchy (e.g., telethon/setup, telethon/force_setup)
    - [ ] Update help text to show command hierarchy

### MongoDB Integration

- [ ] Add MongoDB support for session storage
    - [ ] Create session storage interface
    - [ ] Implement file-based storage (current)
    - [ ] Implement MongoDB-based storage
    - [ ] Add auto-detection of MongoDB availability
    - [ ] Add migration tools between storage types

### Command Documentation

- [ ] Add all commands to a central registry
    - [ ] Option 1: Extend bot_commands_menu to show all commands
    - [ ] Option 2: Create a dedicated help command with detailed descriptions
    - [ ] Add command categories (e.g., setup, management, info)
    - [ ] Add command examples and usage notes

### Feature Ideas

- [ ] Add session management commands
    - [ ] List all active sessions
    - [ ] Delete specific sessions
    - [ ] Export/Import sessions
- [ ] Add session backup/restore functionality
- [ ] Add session expiration and auto-refresh
- [ ] Add rate limiting and usage tracking 