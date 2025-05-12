import os
from pathlib import Path
import shutil
from dotenv import dotenv_values
from loguru import logger


def discover_python_executable() -> str:
    """
    Discover the python executable path.
    """
    # 1. check if STABLE_VENV_PATH is set
    stable_venv_path = os.environ.get("STABLE_VENV_PATH")
    if stable_venv_path:
        python_executable_path = Path(stable_venv_path) / "bin" / "python3"
        if python_executable_path.exists():
            logger.info("Found python executable path with STABLE_VENV_PATH")
            return str(python_executable_path)

    # 2. try relpath
    relpath = Path("~/.calmmage/dev_env/.venv/bin/python3").expanduser()
    if relpath.exists():
        logger.info("Found python executable path with relpath")
        return str(relpath)

    # 4. last resort - try to find python3 in PATH
    python3_path = shutil.which("python3")
    if python3_path:
        logger.info("Found python executable path with PATH")
        return python3_path

    raise RuntimeError("No python executable path found")


def discover_telegram_bot_token() -> str:
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if telegram_bot_token:
        return telegram_bot_token

    # check .env
    env_path = Path(".env")
    vals = dotenv_values(env_path)
    telegram_bot_token = vals.get("TELEGRAM_BOT_TOKEN")
    if telegram_bot_token:
        return telegram_bot_token

    # check ~/.env
    env_path = Path("~/.env").expanduser()
    vals = dotenv_values(env_path)
    telegram_bot_token = vals.get("TELEGRAM_BOT_TOKEN")
    if telegram_bot_token:
        return telegram_bot_token

    raise RuntimeError("No telegram bot token found")


if __name__ == "__main__":
    # test find_python_executable
    print(discover_python_executable())
