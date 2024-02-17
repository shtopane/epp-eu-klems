"""All the general configuration of the project."""

from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

EU_KLEMS_WEBSITE = "https://euklems-intanprod-llee.luiss.it/download/"
EU_KLEMS_DATA_DOWNLOAD_PATH = BLD.joinpath("original_data").resolve()
BLD_PYTHON_PATH = BLD.joinpath("python").resolve()
BLD_PYTHON_DATA_PATH = BLD_PYTHON_PATH.joinpath("data").resolve()

# EU_KLEMS_INVESTMENT_TYPES_MAPPING = {
#     "I_OIPP": "other_intangibles",
#     "I_RD": "research_development",
#     "I_Soft_DB": "software_databases",
#     "VA_CP": "value_added"
# }
TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

# EL is Greece
COUNTRY_CODES = ["AT", "CZ", "DK", "EL", "SK"]

for country_code in COUNTRY_CODES:
    # Create sub directories for every country in the original data directory
    Path(EU_KLEMS_DATA_DOWNLOAD_PATH / country_code).mkdir(parents=True, exist_ok=True)
    # Create sub directories for every country in the python data directory
    Path(BLD / "python" / "data" / country_code).mkdir(parents=True, exist_ok=True)

__all__ = ["BLD", "SRC", "TEST_DIR"]
