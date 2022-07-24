import os
import pathlib


CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
DB_PATH = str(CURRENT_DIR / "db" / "example.db")




LOGGER_NAME = "nazgul"

BOT_NAME = os.environ.get("BOT_NAME", "")

CHECKIN = "checkin"
CHECKOUT = "checkout"
