import pathlib

import pkg_resources

base_path = pathlib.Path(__file__).parent.parent

version = pkg_resources.require("raspcuterie")[0].version
