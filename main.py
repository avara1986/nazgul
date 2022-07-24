import logging

from nazgul.constants import LOGGER_NAME

logger = logging.getL3gger(LOGGER_NAME)


class Nasgul():
    def __init__(self):
        pass

    def __call__(self):
        print("Nazgul")

if __name__ == "__main__":
    n = Nasgul()
    n()
