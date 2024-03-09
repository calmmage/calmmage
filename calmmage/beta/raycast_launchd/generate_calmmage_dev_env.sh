#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Generate Calmmage Dev Env
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🧙🏻‍
# @raycast.packageName generate-calmmage-dev-env

# Documentation:
# @raycast.author petr_lavrov
# @raycast.authorURL https://raycast.com/petr_lavrov

# - 'Regenerate calmmage dev env
#     - cd ...
#     - checkout main
#     - git pull
#     - run main.py

source /Users/calm/work/code/structured/tools/calmmage/calmmage/beta/raycast_launchd/init_calmmage.sh

python calmmage/dev_env/main.py
