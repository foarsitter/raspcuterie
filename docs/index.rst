.. raspcuterie documentation master file, created by
   sphinx-quickstart on Sat Oct 31 19:54:09 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to raspcuterie's documentation!
=======================================

You need a:

- raspberry pi zero with header
- am2302
- relay board
- fan
- jumper cables
- power adapter


  Download en installeer "raspberry pi os". Hoe je dat doe staat veelvuldig op internet uitgegelegd, bijvoorbeeld hier: https://raspberrytips.nl/raspberry-pi-installeren/

  Sluit vervolgens de AM2302 & relay board aan.

  https://raspberrytips.nl/dht22-temperatuursensor-raspberry-pi/
  https://www.youtube.com/watch?v=OQyntQLazMU

  Installeerd raspcuterie: `pip install raspcuterie[pi]`

  test of de installatie is gelukt:

  raspcuterie-cli version

  sudo raspcuterie-cli install


  ga naar het ip van je raspberry pi met daarachter poort 5000: localhost:5000



.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


sudo apt  --assume-yes update
sudo apt  --assume-yes install python3-pip

sudo pip3 install --upgrade pip setuptools wheel

sudo pip3 install raspcuterie[rpi]

raspcuterie config
raspcuterie log-values
raspcuterie install cron
raspcuterie install systemd