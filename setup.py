from setuptools import setup, find_packages

setup(
    name="raspcuterie",
    version="0.1.0",
    py_modules=["raspcuterie"],
    packages=find_packages(),
    install_requires=["Click"],
    entry_points={
        "console_scripts": ["raspcuterie-cli=raspcuterie.cli:cli"],
        "raspcuterie.devices.input": [
            "am2302=raspcuterie.devices.input.am2302:AM2302",
            "sinus=raspcuterie.devices.input.sinus:SinusInput",
        ],
        "raspcuterie.devices.output": [
            "relay=raspcuterie.devices.output.relay:RelaySwitch",
            "dbrelay=raspcuterie.devices.output.relay:DBRelay",
        ],
    },
)
