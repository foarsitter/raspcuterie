
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


Andere hardware
........................

Als je zelf een goed idee hebt van waar je mee bezig bent kun je gekozen onderdelen natuurlijk ook uitwisselen voor anderen.
Zo is de aangeschafte voeding wellicht een beetje overkill en kun je ook gerust een oude smartphone voeding gebruiken.
Dit geldt eveneens voor de gebruikte geheugenkaart.
We hebben echt geen 16gb nodig, eerder 2gb, maar een 8gb kaart is slechts 3 euro goedkoper.

Goedkoopste
........................

Het goedkoopste is natuurlijk om al de onderdelen online in het buitenland te bestellen. Echter heb je dan wel te maken met een lange levertijd. Als je snel aan de slag wilt kun je het beste bestellen bij een Nederlandse partij zoals het groningse Okaphone.


Devices
........


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