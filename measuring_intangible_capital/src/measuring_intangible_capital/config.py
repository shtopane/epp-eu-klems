"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

DATA = SRC.joinpath("..", "..", "data").resolve()
EU_KLEMS_WEBSITE = "https://euklems-intanprod-llee.luiss.it/download/"

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

# EL is Greece
COUNTRY_CODES = ["AT", "CZ", "DK", "EL", "SK"]

__all__ = ["BLD", "SRC", "TEST_DIR"]
