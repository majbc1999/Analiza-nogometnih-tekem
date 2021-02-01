# Uvoz potrebnih knjižnic
import re
import csv
import json
import os
import requests
import sys

# Uvoz html-jev
def uvozi_datoteko(datoteka):
    with open(datoteka, encoding='utf-8') as d:
        return d.read()

# Vzorec za matchday
vzorec_matchday = (
    r'<div class="table-header">'
    r'(?P<matchday>.*?)'
    r'</div>'
    r'(?s)(.*?)'
    r'<div class="table-footer">'
)

# Vzorec za zajem datuma in časa znotraj matchdaya
vzorec_datum = (
    r'<td class="hide-for-small">\n'
    r'(?s)(\s*?)'
    r'(?P<dan>\w{3})'
    r'(?s)(\s*?)'
    r'\w*?<a href="https://www.transfermarkt.com/aktuell/waspassiertheute/aktuell/new/datum/\d{4}-\d{2}-\d{2}">'
    r'(?P<datum>.*?)</a>'
    r'(?s)(\s*?)</td>\n(?s)(.*?)((<tr class="bg_blau_20">(?s)(\s*?)<td class="show-for-small" colspan="7">(?s)(\s*?)\w{3})|(<div class="table-footer">))'
)

# Vzorec za uro
vzorec_ura = (
    r'<td class="zentriert hide-for-small">\n\s.*?'
    r'(?P<ura>(\d{1,2}:\d\d (AM|PM)))'
    r'.*?((</td>([\s\S]*?)<tr class="bg_blau_20">)|(</td>([\s\S]*?)<div class="table-footer">))'
)

# Vzorec za tekmo znotraj datuma in časa
vzorec_tekma = (
    r'<td class="text-right no-border-rechts hauptlink"><span class="tabellenplatz">\('
    r'(?P<lestvica_domaci>\d{1,2})'
    r'.\)</span>&nbsp;&nbsp;<a class="vereinprofil_tooltip tooltipstered" id="'
    r'(?P<id_domaci>\d{1,5})'
    r'" href="https://www.transfermarkt.com/.*?/spielplan/verein/\d{1,5}/saison_id/2019">'
    r'(?P<domaca_ekipa>.*?)'
    r'</a></td>\n(.*?)\n(.*?)class="ergebnis-link" id="\d{7}" href="https://www.transfermarkt.com/spielbericht/index/spielbericht/\d{7}">'
    r'(?P<zadetki_domaci>\d{1,2})'
    r':'
    r'(?P<zadetki_gostje>\d{1,2})'
    r'</a>&nbsp;</td>\n.*?\n.*?<td class="no-border-links hauptlink"><a class="vereinprofil_tooltip tooltipstered" id="'
    r'(?P<id_gostje>\d{1,5})'
    r'" href="https://www.transfermarkt.com/.*?/spielplan/verein/\d{1,5}/saison_id/2019">'
    r'(?P<gostujoca_ekipa>.*?)'
    r'</a>&nbsp;&nbsp;<span class="tabellenplatz">\('
    r'(?P<lestvica_gostje>\d{1,2})'
    r'\.\)</span></td>'
)

# Uvozimo vse lige
laliga = uvozi_datoteko(r'.\html\laliga.html')
premierleague = uvozi_datoteko(r'.\html\premierleague.html')
seriea = uvozi_datoteko(r'.\html\seriea.html')


# Orodje za zapis csv datoteke (iz predavanj - najdene v profesorjevem repozitoriju)
def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj, lineterminator='\n')
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

# Prazni začetni seznami za slovarje
seznam_laliga = []
seznam_premier_league = []
seznam_seriea = []

# Pomožne funkcije za obdelavo podatkov:
def stevilka_matchdaya(niz):
    stevila = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    nov_niz = ""
    for crka in niz:
        if crka in stevila:
            nov_niz += crka
    return int(nov_niz)

slovarprevoda = {"Mon": "ponedeljek", "Tue": "torek", "Wed" : "sreda", "Thu": "četrtek", "Fri": "petek", "Sat": "sobota", "Sun": "nedelja"}
def datum_prevedi(niz):
    return slovarprevoda[niz]

# Tukaj je funkcija za izluščitev v slovarje, ki se shranijo v sezname
def izlusci_podatke_v_slovar(seznam, podatki):
    for z1 in re.finditer(vzorec_matchday, podatki):
        matchday = z1['matchday']
        x1 = z1.group()
        for z2 in re.finditer(vzorec_datum, x1):
            dan = z2['dan']
            datum = z2['datum']
            x2 = z2.group()
            for z3 in re.finditer(vzorec_ura, x2):
                ura = z3['ura'] 
                x3 = z3.group()
                for z4 in re.finditer(vzorec_tekma, x3):
                    id_domaci = int(z4['id_domaci'])
                    lestvica_domaci = int(z4['lestvica_domaci'])
                    domaca_ekipa = z4['domaca_ekipa']
                    id_gostje = int(z4['id_gostje'])
                    lestvica_gostje = int(z4['lestvica_gostje'])
                    gostujoca_ekipa = z4['gostujoca_ekipa']
                    zadetki_domaci = int(z4['zadetki_domaci'])
                    zadetki_gostje = int(z4['zadetki_gostje'])
                    if zadetki_domaci > zadetki_gostje:
                        tocke_domaci = 3
                        tocke_gostje = 0
                    if zadetki_domaci < zadetki_gostje:
                        tocke_domaci = 0
                        tocke_gostje = 3
                    if zadetki_domaci == zadetki_gostje:
                        tocke_domaci = 1
                        tocke_gostje = 1
                    slovar_tekme = {"kolo": stevilka_matchdaya(matchday), 
                                    "dan": datum_prevedi(dan), 
                                    "datum": datum, 
                                    "ura": ura, 
                                    "id_domaci": id_domaci, 
                                    "lestvica_domaci": lestvica_domaci, 
                                    "domaca_ekipa": domaca_ekipa,
                                    "id_gostje": id_gostje,
                                    "lestvica_gostje": lestvica_gostje,
                                    "gostujoca_ekipa": gostujoca_ekipa,
                                    "zadetki_domaci": zadetki_domaci,
                                    "tocke_domaci": tocke_domaci,
                                    "zadetki_gostje": zadetki_gostje,
                                    "tocke_gostje": tocke_gostje,
                                    }
                    seznam.append(slovar_tekme)                                          

# Izluščimo dejanske podatke, ki so sedaj shranjeni v sezname
izlusci_podatke_v_slovar(seznam_laliga, laliga)
izlusci_podatke_v_slovar(seznam_premier_league, premierleague)
izlusci_podatke_v_slovar(seznam_seriea, seriea)

# Jih še izvozimo v csv obliko
zapisi_csv(seznam_laliga, 
    ['kolo', 'dan', 'datum', 'ura', 'id_domaci', 'lestvica_domaci', 'domaca_ekipa', 'id_gostje', 'lestvica_gostje', 'gostujoca_ekipa', 'zadetki_domaci', 'tocke_domaci', 'zadetki_gostje', 'tocke_gostje'],
    'obdelani-podatki/laliga.csv')
zapisi_csv(seznam_premier_league, 
    ['kolo', 'dan', 'datum', 'ura', 'id_domaci', 'lestvica_domaci', 'domaca_ekipa', 'id_gostje', 'lestvica_gostje', 'gostujoca_ekipa', 'zadetki_domaci', 'tocke_domaci', 'zadetki_gostje', 'tocke_gostje'],
    'obdelani-podatki/premier_league.csv')
zapisi_csv(seznam_seriea, 
    ['kolo', 'dan', 'datum', 'ura', 'id_domaci', 'lestvica_domaci', 'domaca_ekipa', 'id_gostje', 'lestvica_gostje', 'gostujoca_ekipa', 'zadetki_domaci', 'tocke_domaci', 'zadetki_gostje', 'tocke_gostje'],
    'obdelani-podatki/seriea.csv')


