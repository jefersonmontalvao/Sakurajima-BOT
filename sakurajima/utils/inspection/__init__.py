from inspect import currentframe

__all__ = ['get_var_name']


def get_var_name(var) -> str or list:
    """
    This function return the variable name.
    This is made testing if variable name in actual frame has the same value of
    "var" param, so if you have two variables with the same value, this function cant
    understand this and have a chance4 to return the wrong name from the another variable.
    """
    callers_local_vars = currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]
