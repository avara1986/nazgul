import os
import pathlib

# DEBUG DB
NAZGUL_CONFIG_PATH_DEBUG = pathlib.Path(__file__).parent.resolve() / "db"
DB_PATH_DEBUG = str(NAZGUL_CONFIG_PATH_DEBUG / "nazgul.db")
# PROD DB
NAZGUL_CONFIG_PATH = pathlib.Path(os.environ.get("HOME")) / ".config" / "nazgul"
DB_PATH = str(NAZGUL_CONFIG_PATH / "nazgul.db")

LOGGER_NAME = "nazgul"

CHECKIN = "checkin"
CHECKOUT = "checkout"
