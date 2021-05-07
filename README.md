# Analiza nogometnih tekem 2019/2020

Analiziral bom vse nogometne tekme v 3 najmočnejših ligah: Premier league, LaLiga, Serie A. Podatke za vse tekme bom dobil na portalu [Transfermarkt](https://www.transfermarkt.com/).

## Podatki
Za vsako odigrano tekmo bom zajel:
* domačo in gostujočo ekipo
* končni rezultat tekme
* položaj domače in gostujoče ekipe na lestvici pred odigrano tekmo
* čas tekme

Obdelani podatki so v mapi `obdelani-podatki` na repozitoriju. V mapi so tri csv datoteke (za vsako ligo svoja). Vsaka tekma, odigrana v teh ligah, ima svojo vrstico. Razlaga imen stolpcev:
* `kolo`: Krog lige, v katerem je bila tekma odigrana
* `dan`: Dan v tednu, na kateri je bila odigrana
* `datum`: Datum tekme
* `ura`: Ura tekme
* `id_domaci`: Poseben transfermarkt id (uporaba bo samo za lažje citiranje ekipe)
* `lestvica_domaci`: Mesto domače ekipe na lestvici lige, po odigrani tekmi
* `domaca_ekipa`: Ime domače ekipe
* `id_gostje`: Poseben transfermarkt id (uporaba bo samo za lažje citiranje ekipe)
* `lestvica_gostje`: Mesto gostujoče ekipe na lestvici lige, po odigrani tekmi
* `gostujoca_ekipa`: Ime gostujoče ekipe
* `zadetki_domaci`: Število zadetkov za domačo ekipo
* `zadetki_gostje`: Število zadetkov za goste

## Hipoteze
Ogledal si bom naslednje **hipoteze**:
* domača ekipa zmaga v več primerih kakor gostujoča
* odstotek zmag domače ekipe je nižji po korona-premoru (prazne tribune)
* forma ekipe vpliva na končni rezultat (večkrat zmaga ekipa, ki je v dobri formi kakor tista, ki je v slabi)
* najpogostejši rezultat na derbijih (vodilne ekipe) je remi
* boljše ekipe igrajo ob bolj poznih urah 
* celotno število golov je najnižje v italjanski ligi (obrambni nogomet) in najvišje v španski ligi (precej napadalen nogomet)