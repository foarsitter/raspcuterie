from setuptools import setup, find_packages

minimal_requirements = [
    "Flask==1.1.2",
    "Click==7.1.2",
    "pyyaml==5.3.1",
    "flask-babel==2.0.0",
]


def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()


rpi_requirements = ["rpi.gpio==0.7.0", "Adafruit_DHT==1.4.0"]

setup(
    description="Charcuterie dashboard and controller for the Raspberry PI",
    license="MIT",
    name="raspcuterie",
    version="0.1.2",
    py_modules=["raspcuterie"],
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/foarsitter/raspcuterie",
    entry_points={
        "console_scripts": ["raspcuterie-cli=raspcuterie.cli:cli"],
        # "raspcuterie.devices.input": [
        #     "am2302=raspcuterie.devices.input.am2302:AM2302",
        #     "sinus=raspcuterie.devices.input.sinus:SinusInput",
        # ],
        # "raspcuterie.devices.output": [
        #     "relay=raspcuterie.devices.output.relay:RelaySwitch",
        #     "dbrelay=raspcuterie.devices.output.relay:DBRelay",
        # ],
    },
    install_requires=minimal_requirements,
    extras_require={"rpi": rpi_requirements},
)