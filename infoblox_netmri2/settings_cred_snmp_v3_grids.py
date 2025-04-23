###########################################################################
## Export of Script Module: netmri_settings_cred_snmp_v3_grids
## Language: Python
## Category: Internal
## Description: Provides access to the 'Settings Cred SNMP V3 Grids' controller of the NetMRI API.\n\nRequires the 'netmri_paging' and the 'netmri_query' libraries.
###########################################################################
class _deps:
    import collections.abc
    import dataclasses
    import typing

    from infoblox_netmri.easy import NetMRIEasy

    from .utils import paging
    from .utils import query


@_deps.dataclasses.dataclass
class Model:
    id: int
    Collector: str
    Priority: int
    Protocol: str
    Password: str
    SNMPAuthPW: str
    # Indeed, three following attributes are None when unspecified in NetMRI's
    # GUI.
    SNMPAuthProto: _deps.typing.Optional[str]
    SNMPPrivPW: _deps.typing.Optional[str]
    SNMPPrivProto: _deps.typing.Optional[str]
    Origination: str
    Vendor: str
    Type: str
    PasswordID: int
    UnitID: int
    Successful: int
    Invalid: int


LIMIT_MAX: int = 1000


# TODO use __name__?
_CONTROLLER_TECHNICAL_NAME = "settings_cred_snmp_v3_grids"


_TModel = _deps.typing.TypeVar("_TModel")


def index(
    netmri: _deps.NetMRIEasy,
    model: type[_TModel] = Model,  # replaces the "select" param of the NetMRI API.
    /,
    *,
    UnitID: int = 0,
    start: int = 0,
    limit: int = LIMIT_MAX,
    sort: tuple[str, ...] = ("id",),
    dir_: tuple[str, ...] = ("asc",),
    refresh_ind: bool = False,
    async_ind: bool = False,
) -> _deps.paging.Page[_deps.collections.abc.Iterator[_TModel]]:
    """
    Positional Parameters
    ---------------------
    1. NetMRI Easy object bound to the NetMRI instance to query.
    2. (optional) Class of the object to return. Attributes of the class
       indicate which attributes are retrieved from NetMRI. The class must have
       an `__init__` method with parameters matching the class attributes. This
       parameter defaults to the `Model` class of this module, which provides
       all the attributes available by NetMRI. Tip: To easily define a class
       that retrieves a smaller set of attributes, use Python's
       `dataclasses.dataclass` decorator.

    Keyword Parameters
    ------------------
    Same as the `settings_cred_snmp_v3_grids/index` method of the NetMRI API,
    minus `select`, as the selected attributes are deducted from the specified
    model (second positional argument.)
    """

    return _deps.query.index(index, locals(), _CONTROLLER_TECHNICAL_NAME)
