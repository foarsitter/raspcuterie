import os
import pathlib

base_path = pathlib.Path(__file__).parent.parent

FAKE_VALUES = bool(os.getenv("FAKE_VALUES", False))
