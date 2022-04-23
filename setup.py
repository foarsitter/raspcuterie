from setuptools import find_packages, setup

minimal_requirements = [
    "Flask[async]==2.0.2",
    "Click==8.0.3",
    "pyyaml==5.4.1",
    "adafruit-circuitpython-dht==3.7.0",
    "rpi.gpio==0.7.0",
    "pydantic==1.9.0",
    "timeout-decorator==0.5.0",
    "pygments",
    "rpi.bme280",
    "smbus2",
]


def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()


setup(
    description="Charcuterie dashboard and controller for the Raspberry PI",
    license="MIT",
    name="raspcuterie",
    version="1.0.0",
    py_modules=["raspcuterie"],
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/foarsitter/raspcuterie",
    include_package_data=True,
    entry_points={
        "console_scripts": ["raspcuterie=raspcuterie.cli:cli"],
    },
    install_requires=minimal_requirements,
)
