"""All the general configuration of the project."""

from pathlib import Path
from typing import Literal

import numpy as np

# DATA Related constants
FILES_TO_EXCLUDE = ["growth_accounts.xlsx", "growth%20accounts"]
FILES_TO_DOWNLOAD_NAMES = [
    "National Accounts",
    "Capital",
    "Labour",
    "Intangibles",
    "Growth Accounts Basic",
]
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

# Analysis variables
COUNTRY_CODES = ["AT", "CZ", "DK", "EL", "SK"]

COUNTRY_CODES_EXTENDED = ["US", "UK", "DE", "FR", "IT", "ES"]

COUNTRY_CODES_MAP = {"AUT": "AT", "CZE": "CZ", "DNK": "DK", "GRC": "EL", "SVK": "SK"}
COUNTRY_CODES_MAP_EXTENDED = {
    "GBR": "UK",
    "USA": "US",
    "FRA": "FR",
    "DEU": "DE",
    "ITA": "IT",
    "ESP": "ES",
}

COUNTRY_CODES_LESS_SK = ["AT", "CZ", "DK", "EL"]
COUNTRIES = ["Austria", "Czech Republic", "Denmark", "Greece", "Slovakia"]
COUNTRIES_EXTENDED = [
    "United States",
    "United Kingdom",
    "Germany",
    "France",
    "Italy",
    "Spain",
]

PLOT_COLORS_BY_COUNTRY = ["gray", "darkgray", "lavender", "lightsteelblue", "royalblue"]
PLOT_COLORS_AGGREGATE_CATEGORIES = ["gray", "darkgray", "lavender"]

PLOT_COLORS_BY_COUNTRY_EXTENDED = [
    "gray",
    "lavender",
    "royalblue",
    "lightsteelblue",
    "darkgray",
    "black",
]

COUNTRY_COLOR_MAP = dict(zip(COUNTRIES, PLOT_COLORS_BY_COUNTRY))
COUNTRY_COLOR_MAP_EXTENDED = dict(
    zip(COUNTRIES_EXTENDED, PLOT_COLORS_BY_COUNTRY_EXTENDED),
)

ALL_COUNTRY_CODES = COUNTRY_CODES + COUNTRY_CODES_EXTENDED
ALL_COUNTRIES = COUNTRIES + COUNTRIES_EXTENDED
ALL_COUNTRY_COLOR_MAP = {**COUNTRY_COLOR_MAP, **COUNTRY_COLOR_MAP_EXTENDED}
ALL_COUNTRY_CODES_MAP = {**COUNTRY_CODES_MAP, **COUNTRY_CODES_MAP_EXTENDED}
ALL_PLOT_COLORS_BY_COUNTRY = PLOT_COLORS_BY_COUNTRY + PLOT_COLORS_BY_COUNTRY_EXTENDED
ALL_COUNTRY_CODES_LESS_SK = COUNTRY_CODES_LESS_SK + COUNTRY_CODES_EXTENDED

# Columns on investment which make up intangible investment.
# Each of this type is aggregated up to @see INTANGIBLE_AGGREGATE_CATEGORIES
INTANGIBLE_DETAIL_CATEGORIES = [
    "brand",
    "design",
    "new_financial_product",
    "entertainment_and_artistic",
    "organizational_capital",
    "research_and_development",
    "software_and_databases",
    "training",
]

INTANGIBLE_DETAIL_CATEGORIES_TYPE = Literal[
    "brand",
    "design",
    "new_financial_product",
    "entertainment_and_artistic",
    "organizational_capital",
    "research_and_development",
    "software_and_databases",
    "training",
]
# Columns on intangible investment as classified by CHS (2005)
INTANGIBLE_AGGREGATE_CATEGORIES = [
    "computerized_information",
    "innovative_property",
    "economic_competencies",
]

INTANGIBLE_AGGREGATE_CATEGORIES_TYPE = Literal[
    "computerized_information",
    "innovative_property",
    "economic_competencies",
]

CAPITAL_ACCOUNT_INDUSTRY_CODE = "MARKT"
NATIONAL_ACCOUNT_INDUSTRY_CODE = "TOT"

LABOUR_COMPOSITION_COLUMNS = [
    "intangible",
    "labour_composition",
    "tangible_ICT",
    "tangible_nonICT",
]
MPF_COLUMN = "mfp"
LABOUR_COMPOSITION_COLUMNS_EXTENDED = [*LABOUR_COMPOSITION_COLUMNS, MPF_COLUMN]

LABOUR_COMPOSITION_PLOT_COLORS = [
    "royalblue",
    "gray",
    "lightsteelblue",
    "darkgray",
    "lavender",
]

# TESTING: Create a random number generator to be used in test files.
RNG_FOR_TESTING = np.random.default_rng(seed=92595)
