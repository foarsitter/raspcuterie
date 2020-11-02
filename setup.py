from setuptools import setup, find_packages

minimal_requirements = [
    "Flask==1.1.2",
    "Click==7.1.2",
    "pyyaml==5.3.1",
    "flask-babel==2.0.0",
]

rpi_requirements = ["rpi.gpio==0.7.0", "Adafruit_DHT==1.4.0"]

setup(
    name="raspcuterie",
    version="0.1.1",
    py_modules=["raspcuterie"],
    packages=find_packages(),
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
    install_requires=minimal_requirements,
    extras_require={"rpi": rpi_requirements},
)
