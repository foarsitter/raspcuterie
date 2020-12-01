Software
------------------------------------------

Raspberry Pi os
```````````````````````````````
De eerste stap is om de geheugenkaart voor te bereiden op het draaien van het "raspberry pi os".
Hoe je dat doe staat veelvuldig op internet uitgelegd, bijvoorbeeld hier: `<https://raspberrytips.nl/raspberry-pi-installeren/>`__

Headless setup
................................
Om de kosten te drukken kun je voor een headless setup gaan.
Dit betekend dat je geen toetsenbord, muis en monitor koppeld aan je Raspberry Pi.
Je logt dan via SSH in op de Raspberry Pi.
De uitleg om direct SSH aan te zetten en met WIFI te verbinden is hier te lezen `<https://raspberrytips.nl/wifi-instellingen-raspbian-image/>`__.

Belangrijk
.................
Vergeet niet om direct bij de eerste keer inloggen je wachtwoord aan te passen.


Raspcuterie
````````````````````````````````````

.. code-block:: shell

   sudo apt  --assume-yes update
   sudo apt  --assume-yes install python3-pip

   pip3 install raspcuterie

   raspcuterie config
   raspcuterie install cron
   raspcuterie install systemd

test of de installatie is gelukt:

.. code-block:: shell

    raspcuterie --help
    sudo systemctl status raspcuterie

Open je browser en ga naar `<http://localhost:5000>`_

Heb je een headless setup? Ga dan in de browser naar het ipadres van je Raspberry Pi met daarachter :5000.

Ga naar het ip van je raspberry pi met daarachter poort 5000: localhost:5000. Het ip-adres van je raspberry pi kun je vinden in je router.
