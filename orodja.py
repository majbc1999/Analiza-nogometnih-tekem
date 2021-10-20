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

# vzorecpy = <div class="table-header">(.*?)</div>(?s)(.*?)<div class="table-footer">

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
    r'" href="https://www.transfermarkt.com/.*?/spielplan/verein/\d{1,5}/saison_id/\d{4}">'
    r'(?P<domaca_ekipa>.*?)'
    r'</a></td>\n(.*?)\n(.*?)class="ergebnis-link" id="\d{7}" href="(.*?)">'
    r'(?P<zadetki_domaci>\d{1,2})'
    r':'
    r'(?P<zadetki_gostje>\d{1,2})'
    r'</a>&nbsp;</td>\n.*?\n.*?<td class="no-border-links hauptlink"><a class="vereinprofil_tooltip tooltipstered" id="'
    r'(?P<id_gostje>\d{1,5})'
    r'" href="https://www.transfermarkt.com/.*?/spielplan/verein/\d{1,5}/saison_id/\d{4}">'
    r'(?P<gostujoca_ekipa>.*?)'
    r'</a>&nbsp;&nbsp;<span class="tabellenplatz">\('
    r'(?P<lestvica_gostje>\d{1,2})'
    r'\.\)</span></td>'
)

#vzorec = <td class="text-right no-border-rechts hauptlink"><span class="tabellenplatz">\(\d{1,2}.\)</span>&nbsp;&nbsp;<a class="vereinprofil_tooltip tooltipstered" id="\d{1,5}" href="https://www.transfermarkt.com/.*?/spielplan/verein/\d{1,5}/saison_id/\d{4}">.*?</a></td>\n(.*?)\n(.*?)class="ergebnis-link" id="\d{7}" href="(.*?)">\d{1,2}:\d{1,2}</a>&nbsp;</td>\n.*?\n.*?<td class="no-border-links hauptlink"><a class="vereinprofil_tooltip tooltipstered" id="\d{1,5}" href="https://www.transfermarkt.com/.*?/spielplan/verein/\d{1,5}/saison_id/\d{4}">(.*?)</a>&nbsp;&nbsp;<span class="tabellenplatz">\(\d{1,2}\.\)</span></td>

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
seznam_den2019 = []


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

# Pomožna funkcija, ki pove ali je rezulat remi ali ne
def remi(n): 
    if n == 1.5: return 0
    else: return 1

# Tukaj je funkcija za izluščitev v slovarje, ki se shranijo v sezname
def izlusci_podatke_v_slovar(podatki, datoteka, drzava, sezona):
    seznam = []
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
                    slovar_tekme = {"kolo": stevilka_matchdaya(matchday), 
                                    "dan": datum_prevedi(dan), 
                                    "datum": datum,
                                    "ura": ura, 
                                    "lestvica_domaci": lestvica_domaci, 
                                    "domaca_ekipa": domaca_ekipa,
                                    "lestvica_gostje": lestvica_gostje,
                                    "gostujoca_ekipa": gostujoca_ekipa,
                                    "zadetki_domaci": zadetki_domaci,
                                    "zadetki_gostje": zadetki_gostje,
                                    "drzava": drzava,
                                    "sezona": sezona
                                    }
                    seznam.append(slovar_tekme)       

    zapisi_csv(seznam, 
        ['kolo', 'dan', 'datum', 'ura', 'lestvica_domaci', 'domaca_ekipa', 'lestvica_gostje', 'gostujoca_ekipa', 'zadetki_domaci', 'zadetki_gostje', 'drzava', 'sezona'],
        'obdelani-podatki-magisterij/' + datoteka + '.csv')


############### TESTIRANJE ###################

# Uvozimo vse lige

izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\bundes2018.html'), 'bundes19', 'Germany', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\bundes2018.html'), 'bundes18', 'Germany', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\bundes2020.html'), 'bundes20', 'Germany', 20)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\den2019.html'), 'den19', 'Denmark', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\den2018.html'), 'den18', 'Denmark', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\den2020.html'), 'den20', 'Denmark', 20)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\ere2019.html'), 'ere19', 'Netherlands', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\ere2018.html'), 'ere18', 'Netherlands', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\ere2020.html'), 'ere20', 'Netherlands', 20)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\fra2019.html'), 'fra19', 'France', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\fra2018.html'), 'fra18', 'France', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\fra2020.html'), 'fra20', 'France', 20)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\laliga2019.html'), 'laliga19', 'Spain', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\laliga2018.html'), 'laliga18', 'Spain', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\laliga2020.html'), 'laliga20', 'Spain', 20)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\por2019.html'), 'por19', 'Portugal', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\por2018.html'), 'por18', 'Portugal', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\por2020.html'), 'por20', 'Portugal', 20)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\prem2019.html'), 'prem19', 'United Kingdom', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\prem2018.html'), 'prem18', 'United Kingdom', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\prem2020.html'), 'prem20', 'United Kingdom', 20)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\serie2019.html'), 'serie19', 'Italy', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\serie2018.html'), 'serie18', 'Italy', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\serie2020.html'), 'serie20', 'Italy', 20)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\srb2019.html'), 'srb19', 'Serbia', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\srb2018.html'), 'srb18', 'Serbia', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\srb2020.html'), 'srb20', 'Serbia', 20)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\tur2019.html'), 'tur19', 'Turkey', 19)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\tur2018.html'), 'tur18', 'Turkey', 18)
izlusci_podatke_v_slovar(uvozi_datoteko(r'.\html_magisterij\tur2020.html'), 'tur20', 'Turkey', 20)

                
