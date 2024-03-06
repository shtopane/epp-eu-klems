"""All the general configuration of the project."""

from pathlib import Path
from typing import Literal

# DATA Related constants
FILES_TO_EXCLUDE = ["growth_accounts.xlsx", "growth%20accounts"]
FILES_TO_DOWNLOAD_NAMES = ['National Accounts', 'Capital', 'Labour', 'Intangibles', 'Growth Accounts Basic']
EU_KLEMS_WEBSITE = "https://euklems-intanprod-llee.luiss.it/download/"
EU_KLEMS_FILE_NAMES = [
    "capital_accounts",
    "intangible_analytical",
    "labour_accounts",
    "national_accounts",
    "growth_accounts",
]

# Paths
SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()
EU_KLEMS_DATA_DOWNLOAD_PATH = BLD.joinpath("original_data").resolve()
DATA_CLEAN_PATH = BLD.joinpath("python", "data_clean").resolve()
BLD_PYTHON = BLD.joinpath("python").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

# Analysis variables
COUNTRY_CODES = ["AT", "CZ", "DK", "EL", "SK"]
COUNTRY_CODES_LESS_SK = ["AT", "CZ", "DK", "EL"]
COUNTRIES = ["Austria", "Czech Republic", "Denmark", "Greece", "Slovakia"]
PLOT_COLORS_BY_COUNTRY = ["gray", "darkgray", "lavender", "lightsteelblue", "royalblue"]
COUNTRY_COLOR_MAP = dict(zip(COUNTRY_CODES, PLOT_COLORS_BY_COUNTRY))

INTANGIBLE_AGGREGATE_CATEGORIES = [
    "computerized_information",
    "innovative_property",
    "economic_competencies",
]

INTANGIBLE_AGGREGATE_CATEGORIES_TYPE = Literal['computerized_information', 'innovative_property', 'economic_competencies']

CAPITAL_ACCOUNT_INDUSTRY_CODE = "MARKT"
NATIONAL_ACCOUNT_INDUSTRY_CODE = "TOT"

__all__ = ["BLD", "SRC", "TEST_DIR"]
