infoblox-netmri2
================

This Python libraries provides bindings to Infoblox NetMRI API methods not yet
implemented in [`infoblox-netmri`](https://pypi.org/project/infoblox-netmri/).
It leverages recent Python 3 features (e.g. type annotations) to offer a better
development experience than the first-party library.

Usage
-----

This library includes one module per supported NetMRI API controller. Each
module contains functions corresponding to NetMRI API methods. The parameter of
the functions aligns, with the following exceptions, with those of the NetMRI
API methods.

* The first parameter is mandatory and of type
  `infoblox_netmri.easy.NetMRIEasy`.
* When present, the `select` parameter of a NetMRI API method is replaced with a
  positional argument taking a class.

Due to the dependency on a `NetMRIEasy` object, this library can only be used
within a NetMRI Job. This should change in a future version.

Example:

```py
from infoblox_netmri.easy import NetMRIEasy
import infoblox_netmri2.settings_cred_cli_grids

easy_args = { ... }

with NetMRIEasy(**easy_args) as easy:
    # Get five CLI credential entries from the NetMRI credential manager.
    cli_creds = infoblox_netmri2.settings_cred_cli_grids.index(
      easy,
      sort=("Username",),
      limit=5
    )

    # Print all the usernames.
    for c in cli_creds.items:
        print(c.Username)
```