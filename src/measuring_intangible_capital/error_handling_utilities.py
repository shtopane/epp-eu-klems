def raise_variable_none(variable, variable_name: str) -> None:
    """Raise a ValueError if the variable is None.
    
    Args:
        variable (Any): The variable to check.
        variable_name (str): The name of the variable.
    """
    if variable is None:
        raise ValueError(f"The {variable_name} argument must not be None.")
    
def raise_data_info_invalid(data_info):
    """Raise a TypeError if the data_info argument is not a dictionary.

    Args:
        data_info (dict): The data_info argument.

    Raises:
        TypeError: If the data_info argument is not a dictionary.
    """
    if not isinstance(data_info, dict):
        raise TypeError("The data_info argument must be a dictionary.")

def raise_variable_wrong_type(variable, type, variable_name: str):
    """Raise a ValueError if the variable is not of the specified type.

    Args:
        variable (Any): the variable to check.
        type (Any): the type to check against.(e.g. pd.DataFrame, str, etc.)
        variable_name (str): the name of the variable to be shown in the error message.

    Raises:
        ValueError: If the variable is not of the specified type.
    """
    if not isinstance(variable, type):
        raise ValueError(f"{variable_name} must be of type {type}.")

def raise_country_code_invalid(country_code: str, codes: list[str]):
    """Raise a ValueError if the country code is not in a specified list.

    Args:
        country_code (str): country code to check.
        codes (list[str]): list of country codes to check against.

    Raises:
        ValueError: If the country code is not in the specified list.
    """
    if country_code not in codes:
        raise ValueError(
            f"The country code {country_code} is not valid. Please use one of {codes}."
        )