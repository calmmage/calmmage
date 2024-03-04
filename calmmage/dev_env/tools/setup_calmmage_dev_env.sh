required_env_vars = [
"CALMMAGE_PROJECT_TEMPLATES_DIR",
# "OPENAI_API_KEY",
# "GITHUB_API_TOKEN"
]

# env_file_path

# request value from user and save it to
for env_var in required_env_vars:
    if env_var not in os.environ:
        raise Exception(f"Missing required environment variable: {env_var}")
        # add the var to zshrc?

# make sure env file is loaded in .zshrc?
# todo: simply include it in my calmmage .zshrc
# how?
# .env file should have vars definitions like this:
# export CALMMAGE_PROJECT_TEMPLATES_DIR="/Users/username/Projects/calmage/templates"
# and then bashrc should have this line:
# source /path/to/.env
