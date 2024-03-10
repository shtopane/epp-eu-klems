[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/EVOsE4mq)

# Project for the course Effective Programming Practices, University of Bonn WSe 2023/2024



[![image](https://img.shields.io/github/actions/workflow/status/shtopane/measuring_intangible_capital/main.yml?branch=main)](https://github.com/shtopane/measuring_intangible_capital/actions?query=branch%3Amain)
[![image](https://codecov.io/gh/shtopane/measuring_intangible_capital/branch/main/graph/badge.svg)](https://codecov.io/gh/shtopane/measuring_intangible_capital)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/shtopane/measuring_intangible_capital/main.svg)](https://results.pre-commit.ci/latest/github/shtopane/measuring_intangible_capital/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Replication of "Measuring intangible capital and its contribution to economic growth in Europe"
https://ideas.repec.org/p/ris/eibpap/2009_003.html  
The paper uses a methodology for measuring intangible capital and intangible investment in several European countries: Austria, Denmark, Slovakia, Greece and the Czech Republic. Additionally, data on United States, United Kingdom, Germany, France, Italy and Spain is included from different sources in the analysis.

Categories for measurement are *computerized information, innovative property and economic competencies*.

1. Computerized information

Software and databases. Software is largely included in GDP, data bases are not.

2. Innovative property

Scientific(R&D) and artistic works. Nowadays, included in GDP measurements.

3. Economic competencies

This is the widest category covering human capital formation through training, managerial improvements and company workflow improvements.

This project reproduces figures 1-5 of the paper.

For figure 6a and 6b the data is available, there was just not enough time.

For figures 7 to 8 data on venture capital and market capitalization is missing.

### Data

EU KLEMS database, latest edition(2023)

https://euklems-intanprod-llee.luiss.it/

World Development Indicators(GDP per capita, PPP (current international $))

https://www.worldbank.org/en/home

### Project structure
The project in done in 3 parts: `data_management`, `analysis` and `plotting`

In the `data_management` folder the EU KLEMS data files are downloaded for the countries included in the analysis. The downloaded files are `national_accounts`, `growth_accounts`, `capital_accounts`, `intangible_analytics` and `labour_accounts`. The data is stored as excel file.

In each excel file, each of the variables included is a separate excel sheet. Instructions on which files are read and which variables is selected can be found in `eu_klems_data_info.yml` file.

The EU KLEMS website provides data for all countries in one file but the overall size is over 600MB. That's why I opted for downloading the files for the countries analyzed.

Data on GDP per capita is included as a separate excel file.

Both data sets are cleared with the help of `yaml` files.

In the `analysis` folder are performed the main calculations.

In the `plotting` folder data is prepared for plotting and plots are produced.

### Results
Resulting figures can be seen under `bld/figures`


## Usage
### Locally
To get started, create and activate the environment with

```console
$ conda/mamba env create -f environment.yml
$ conda activate measuring_intangible_capital
```

To build the project, type

```console
$ pytask
```

To run tests
```console
$ pytest
```

### GitHub Codespace
Open in a codespace and 
```console
$ conda/mamba env create -f environment.yml
$ conda activate measuring_intangible_capital
```

For building see building [Locally](#locally)

### Pip
To run the project with pip and venv, type

```console
$ python3 -m venv .venv
```
On Unix or MacOS, run:
```console
$ source .venv/bin/activate
```
On Windows, run:
```console
$ .\.venv\Scripts\activate
```

Finally, type
```console
$ pip install -r requirements.txt
```

For building see building [Locally](#locally)

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
