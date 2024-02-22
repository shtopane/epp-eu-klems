"""All the general configuration of the project."""

from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

EU_KLEMS_WEBSITE = "https://euklems-intanprod-llee.luiss.it/download/"
EU_KLEMS_DATA_DOWNLOAD_PATH = BLD.joinpath("original_data").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

COUNTRY_CODES = ["AT", "CZ", "DK", "EL", "SK"]

# Create sub directories for every country in the bld folder
for country_code in COUNTRY_CODES:
    # Download data and cleaned data
    Path(EU_KLEMS_DATA_DOWNLOAD_PATH / country_code).mkdir(parents=True, exist_ok=True)
    Path(BLD / "python" / "data_clean" / country_code).mkdir(parents=True, exist_ok=True)

__all__ = ["BLD", "SRC", "TEST_DIR"]
