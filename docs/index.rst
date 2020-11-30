Welkom bij de documentatie van raspcuterie!
===============================================

Raspcuterie is een samenstelling van het woord raspberry-pi en charcuterie.
Met dit project proberen we om een zo simpel mogelijke interface te bieden voor de charcuterie & worst liefhebber.

Momenteel bestaat het project uit een dashboard waaraan een relais, luchtvochtigheid en temperatuur sensor is gekoppeld.
Op basis van een simpele configuratie kun je apparaten schakelen via het relais als er aan bepaalde condities worden voldaan.

Als je nog nooit gewerkt hebt met elektronica en geen enkele ervaring hebt met programmeren zal er in het begin veel op je af komen.
Echter is doorzettingsvermogen het enige wat je nodig hebt om het te leren!

Hardware vereisten
------------------------------------------
Raspcuterie is met onderstaande hardware ontwikkeld:

- Raspberry Pi zero with header [`Okaphone <https://www.okaphone.com/artikel.asp?id=487575>`__]
- Micro-SDHC geheugenkaart [`Okaphone <https://www.okaphone.com/artikel.asp?id=487575>`__]
- AM2302 Temperatuur en luchtvochtigheid sensor [`Okaphone <https://www.okaphone.com/artikel.asp?id=480699>`__]
- Relais module [`Okaphone <https://www.okaphone.com/artikel.asp?id=484452>`__]
- Ventilator [`Okaphone <https://www.okaphone.com/artikel.asp?id=490326>`__]
- Jumper cables male-male [`Okaphone <https://www.okaphone.com/artikel.asp?id=471086>`__]
- Power adapter [`Okaphone <https://www.okaphone.com/artikel.asp?id=483040>`__]

Als je zelf een goed idee hebt van waar je mee bezig bent kun je gekozen onderdelen natuurlijk ook uitwisselen voor anderen.
Zo is de aangeschafte voeding wellicht een beetje overkill en kun je ook gerust een oude smartphone voeding gebruiken.
Dit geldt eveneens voor de gebruikte geheugenkaart.
We hebben echt geen 16gb nodig, eerder 2gb, maar een 8gb kaart is slechts 3 euro goedkoper.

Het goedkoopste is natuurlijk om al de onderdelen online in het buitenland te bestellen. Echter heb je dan wel te maken met een lange levertijd. Als je snel aan de slag wilt kun je het beste bestellen bij een Nederlandse partij zoals het groningse Okaphone.

Software
------------------------------------------

Raspberry Pi os
```````````````````````````````
De eerste stap is om de geheugenkaart voor te bereiden op het draaien van het "raspberry pi os".
Hoe je dat doe staat veelvuldig op internet uitgelegd, bijvoorbeeld hier: `<https://raspberrytips.nl/raspberry-pi-installeren/>`__

Om de kosten te drukken ben ik voor een headless setup gegaan (zonder toetsenbord, muis en monitor).
De uitleg om direct SSH aan te zetten en met WIFI te verbinden is hier te lezen `<https://raspberrytips.nl/wifi-instellingen-raspbian-image/>`__.

Als je je door bovenstaande stappen hebt weten te worstelen heb je nu een werkend Raspberry Pi.

Vergeet niet om direct bij de eerste keer inloggen je wachtwoord aan te passen.

AM2302
````````````
In de onderstaande link staat uitgelegd hoe je de sensor koppeld met je RPi.
Kinderspel zeg je over 3 maanden. Voor nu zijn die nummertjes van die pinnetjes lastig te onderscheiden.
Het wil helpen om een overzicht te printen en naast je bordje te leggen. Dan heb je een goed overzicht.

Het software gedeelte kun je overslaan.

In de standaard configuratie gaan we er vanuit dat je `gpio 5` gebruikt als data pin.
Maar dit kun je makkelijk wijzigen in de configuratie.

https://raspberrytips.nl/dht22-temperatuursensor-raspberry-pi/

Relais module
```````````````````````````````
De relais module is ook geen rocket science.
Kies 4 gpio pinnen, 1 voor de stroom (5v) en 1 voor de aarde.

https://www.youtube.com/watch?v=OQyntQLazMU

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



Ga naar het ip van je raspberry pi met daarachter poort 5000: localhost:5000. Het ip-adres van je raspberry pi kun je vinden in je router.



