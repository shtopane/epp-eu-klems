def _raise_if_variable_none(variable, variable_name: str) -> None:
    """Raise a ValueError if the variable is None.
    
    Args:
        variable (Any): The variable to check.
        variable_name (str): The name of the variable.
    """
    if variable is None:
        raise ValueError(f"The {variable_name} argument must not be None.")
    
def _raise_data_info_invalid(data_info):
    if not isinstance(data_info, dict):
        raise TypeError("The data_info argument must be a dictionary.")