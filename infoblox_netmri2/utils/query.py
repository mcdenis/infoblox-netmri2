###########################################################################
## Export of Script Module: netmri_query
## Language: Python
## Category: Internal
## Description: Common implementation of NetMRI API wrappers.
###########################################################################
class _deps:
    import collections.abc
    import inspect
    import typing

    from infoblox_netmri.easy import NetMRIEasy

    from . import interop
    from . import json_bug_patch
    from . import paging


def index(
    function_or_method: _deps.collections.abc.Callable[
        ..., _deps.paging.Page[_deps.collections.abc.Iterator[_deps.typing.Any]]
    ],
    locals: dict[str, _deps.typing.Any],
    controller_name: str,
) -> _deps.paging.Page[_deps.collections.abc.Iterator[_deps.typing.Any]]:
    """
    Query a NetMRI resource using an index-styled NetMRI API method and return a
    Python typed result.

    This function is a generic implementation of Python querying functions
    including the `index` functions in the modules
    `netmri_settings_cred_cli_grids` and `netmri_settings_cred_snmp_v2_grids`.
    It is intended for code reuse.

    ## Usage

    1. Declare a dataclass with fields **matching** the attributes of the
       elements managed by the NetMRI API method.

    2. Declare a function with the same name as the NetMRI API method and those
       basic parameters:
        * `netmri`: a NetMRI Easy instance connected to the NetMRI system to
          query;
        * `model`: the type of the elements returned by the NetMRI API. Set the
          default value to the class declared in step 1.

    3. Add a parameter for every parameter of the NetMRI API method (e.g.
       `start`, `limit`, `sort`) and match the default values.

    4. In the function body, return the output of this function, passing the
       specialized NetMRI API wrapper, the specialized wrapper's locals and the
       technical name of the NetMRI controller defining the NetMRI method.
       Example:

       ```
       return _deps.netmri_query.index(index,
                                       locals(),
                                       _CONTROLLER_TECHNICAL_NAME)
       ```

    ---------------------------------------------------------------------------

    :param function_or_method: the specialized Python callable wrapping the
        NetMRI API.
    :param locals: the local namespace of the API wrapper. Must include the
        names `netmri` and `model`.
    :param model: the type of the elements returned by the NetMRI API.
    :param netmri: the NetMRI Easy instance to use for querying NetMRI.
    :param controller_name: the technical name of the NetMRI API method.
    """

    # Arguments of the specialized function that we need in this abstraction.
    netmri: _deps.NetMRIEasy = locals["netmri"]
    model: type[_deps.typing.Any] = locals["model"]

    # Create a dict with the arguments for the NetMRI API, except NetMRI's
    # `select` parameter, which we implement through our own `model` parameter
    # to leverage static type checking.
    netmri_args = _deps.interop.get_api_args(
        function_or_method, locals, exclude=("netmri", "model")
    )

    # Generate `select` argument from specified `model`. Do this only if
    # specified model is not the full model (as documented in our docstring, we
    # assume the default value of the `model` parameter is the full model.)
    # Afore mentioned condition not only reduces the request size, but also
    # bypasses an apparent bug in NetMRI 7.5.4.104695, where the latter returns
    # an error when `select` contains `id`.
    if model != _deps.inspect.signature(function_or_method).parameters["model"].default:
        netmri_args["select"] = tuple(_deps.typing.get_type_hints(model).keys())

    # Create a version of netmri.client.api_request that is functionally
    # identical to the original, but retries if it encounters a JSON decode
    # error. This workarounds a bug in NetMRI.
    api_request = _deps.json_bug_patch.json_bug_patch(5)(netmri.client.api_request)

    # Send request.
    #
    # Super important: even though the NetMRI's HTTP API
    # `settings_cred_cli_grids/index` mandates no argument, `netmri_args`
    # cannot be None, nor an empty string, nor an empty list. If it is, we get
    # an HTTP 500 response. Very weird, because "manually" making an HTTP
    # request with `netmri.client.session.get/post(...)` and passing no data
    # works just fine. Anyway, with `netmri.client.api_request`, we MUST pass a
    # dict, which may be empty.
    response = _deps.typing.cast(
        dict[str, _deps.typing.Any],
        api_request(f"{controller_name}/{function_or_method.__name__}", netmri_args),
    )

    return _deps.paging.page_from_response(response, controller_name, model)
