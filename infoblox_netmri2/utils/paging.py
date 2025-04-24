"""
Building blocks for a NetMRI API wrapper with paging capabilities (e.g. the
`Page` class), and utilities for users of afore-mentioned wrappers (e.g.
`iter_til_end` function.)
"""

class _deps:
    import collections.abc
    import dataclasses
    import typing

    from infoblox_netmri.easy import NetMRIEasy


_TPageItemContainer = _deps.typing.TypeVar("_TPageItemContainer",
                                           bound=_deps.collections.abc.Iterator)


@_deps.dataclasses.dataclass(frozen=True)
class Page(_deps.typing.Generic[_TPageItemContainer]):
    
    total: int
    """
    Number of items available on the server.
    """
    

    start: int
    """
    Index of the first item in this page.
    """
    

    limit: int
    """
    Maximum number of items in a page (as specified in the query.)
    """
    
    
    current: int
    """
    Actual number of items in this page.
    """
    
    
    items: _TPageItemContainer
    """
    Items in this page.
    """


_TPageItem = _deps.typing.TypeVar("_TPageItem")


def page_from_response(response: dict[str, _deps.typing.Any],
                       items_key: str,
                       model: type[_TPageItem]) -> Page[_deps.collections.abc.Iterator[_TPageItem]]:
    """
    Create a `Page` object from a NetMRI API response.

    :param response: raw response from the NetMRI API.
    :param items_key: key in the response associated with the items of the page.
        This is usually the technical name of the API controller.
    :param model: type of the items in the page.
    """
    
    return Page(
        total=response["total"],
        start=response["start"],
        limit=response["limit"],
        current=response["current"],
        # Map the response to instances of Model, excluding attributes not
        # defined as annotations on the Model. This excludes the attribute
        # "_class".
        items=(model(**{k:v for k,v in g.items() if k in _deps.typing.get_type_hints(model)}) for g in response[items_key])
    )


def iter_til_end(query_function: _deps.collections.abc.Callable[..., Page[_deps.collections.abc.Iterator[_TPageItem]]],
                 netmri: _deps.NetMRIEasy,
                 model: type[_TPageItem],
                 **kwargs: _deps.typing.Any) -> _deps.collections.abc.Iterator[_TPageItem]:
    """
    Call the specified Python querying function with the specified arguments,
    yields the items in the result page, and repeat the process for the next
    page until all items are yielded.

    Essentially, this allows the caller to efficiently and conveniently iterate
    **all** the items of a particular type without dealing with paging.

    The `start` keyword argument may be used to specify the index of the first
    item to include. It is internally incremented at every request.

    The `netmri`, `model` and other keyword arguments are passed to the
    `query_function` without change.

    ## Example
    
    ```
    from dataclasses import dataclass

    from infoblox_netmri.easy import NetMRIEasy
    import infoblox_netmri2.settings_cred_cli_grids as cli_creds
    import infoblox_netmri2.paging

    @dataclass
    class MyModel:
        Username: str
    
    with NetMRIEasy(...) as easy:
        all_creds = infoblox_netmri2.paging.iter_til_end(
            cli_creds.index,
            MyModel,
            sort=("Priority",)
        )
        print("These are all the user names in the CLI grid:")
        for c in all_creds:
            print(c.Username)
    ```
    """
    
    def query() -> Page[_deps.collections.abc.Iterator[_TPageItem]]:
        return  query_function(netmri, model, **kwargs)
    
    # Do initial query.
    page = query()
    while True:
        # Yield items from previous query.
        for i in page.items:
            yield i
        # Check if there are more items available.
        next_start = page.start + page.current
        if next_start == page.total:
            break
        # Do next query.
        assert next_start < page.total
        kwargs["start"] = next_start
        page = query()