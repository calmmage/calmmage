# Todos
## dev_env_updater

### 0 - rename dev_env_updater
figure out some better new name.
I've renamed dev_env to config/
so..

### 1 - update the path assumptions for the new locations:
CALMMAGE_DIR="$(realpath "~/calmmage")"
CALMMAGE_VENV_PATH="$(realpath "$CALMMAGE_DIR/.venv")"

### 2 - integrate the dev_env_updater into the setup / sync automation / scripts
- one time setup - as per calmmage/config/README.md
- sync automation (fix broken state) - add to calmmage/config/README.md

### 3 - add the dev_env_updater to makefile
- figure out a proper way 