## DisCsengő

Ez egy egyszerű discord bot pythonban, amit az iskolám discord szerveréhez írtam, hogy jelezze amikor elkezdődik/vége van egy órának.

### Használat

* hozz létre egy discord botot és add hozzá a szerveredhez
* írd be a bot token-jét a `TOKEN` változóhoz
* változtasd meg a `timetable` változót, hogy hogy az osztályok órarendjét tartalmazza
* a `lesson_start`-hoz (órák eleje) és a `lesson_end`-hez (órák vége) pedig a csengetési rendet írd
* indítsd el a programot `python discsengo.py` (ennek örökké futnia kell, hogy a bot működjön)
* abban a chat szobában, ahol szeretnéd az órák kiírását látni, írd be a `!start_csengo 12.A` parancsot (érdemes minden osztálynak külön csengő szobát létrehozni)
* az osztály neve ne tartalmazzon szóközt
* ha nem akarod beírni az órarendet osztályonként, a `!start_csengo -` parancs csak az órák számát írja ki
* ha ki akarod kapcsolni a csengőt egy szobában: `!stop_csengo`

