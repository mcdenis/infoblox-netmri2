###########################################################################
## Export of Script Module: interop_utils
## Language: Python
## Category: Internal
## Description: Utilities for building API wrappers.
###########################################################################
class _deps:
    import collections.abc
    import inspect
    import typing


def get_api_args(
    function_or_method,
    locals_: dict[str, _deps.typing.Any],
    exclude: _deps.collections.abc.Iterable[str] = tuple(),
) -> dict[str, _deps.typing.Any]:
    """
    Get a dictionary of arguments intended to an external API from a local
    Python function or method call.

    An argument equal to the default value of the parameter is removed. This
    assumes that the Python function or method has the same defaults as the
    external API.

    The underscore at the end of a parameter name, if any, is removed. This
    allows defining a parameter ending with an underscore when its name
    conflicts with a Python built-in.

    The locals dict is filtered to exclude names that are not parameters of the
    specified Python function or method. Therefore, it is possible to call this
    utility "late" in the specified function or method (after additional locals
    have been created.) Nevertheless, a name can still be updated so it is
    better to use this utility "earlier" in the function or method definition.

    ## Usage
    ```
    def get_device_from_netmri(netmri,
                               DeviceVendor = "",
                               DeviceIPAddress = "",
                               sort_: tuple()):
        api_args = get_api_args(my_func, locals(), ("netmri",)) # the `netmri` arg is not intended to be sent to the external API.
    ```
    """

    py_params = _deps.inspect.signature(function_or_method).parameters
    return {
        k.removesuffix("_"): v
        for k, v in locals_.items()
        if k in py_params and k not in exclude and v != py_params[k].default
    }
