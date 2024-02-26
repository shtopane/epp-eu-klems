"""All the general configuration of the project."""

from pathlib import Path
from typing import Literal

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

EU_KLEMS_WEBSITE = "https://euklems-intanprod-llee.luiss.it/download/"
EU_KLEMS_DATA_DOWNLOAD_PATH = BLD.joinpath("original_data").resolve()
DATA_CLEAN_PATH = BLD.joinpath("python", "data_clean").resolve()
BLD_PYTHON = BLD.joinpath("python").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

# Data Config
FILES_TO_EXCLUDE = ["growth_accounts.xlsx", "growth%20accounts"]

# EU KLEMS File names
EU_KLEMS_FILE_NAMES = [
    "capital_accounts",
    "intangible_analytical",
    "labour_accounts",
    "national_accounts",
]

# Shared variables
COUNTRY_CODES = ["AT", "CZ", "DK", "EL", "SK"]
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

# Create sub directories for every country in the bld folder
for country_code in COUNTRY_CODES:
    # Download data and cleaned data
    Path(EU_KLEMS_DATA_DOWNLOAD_PATH / country_code).mkdir(parents=True, exist_ok=True)
    Path(BLD / "python" / "data_clean" / country_code).mkdir(parents=True, exist_ok=True)

__all__ = ["BLD", "SRC", "TEST_DIR"]
