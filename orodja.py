# Uvoz potrebnih knjižnic
import re

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
    r'<td class="hide-for-small">'
    r'(?s)(\s*?)'
    r'(?P<dan>\w{3})'
    r'(?s)(\s*?)'
    r'\w*?<a href="https://www.transfermarkt.com/aktuell/waspassiertheute/aktuell/new/datum/\d{4}-\d{2}-\d{2}">'
    r'(?P<datum>.*?)</a>'
    r'(?s)(\s*?)'
    r'</td>'
    r'(?s)(.*?)'
    r'<tr class="bg_blau_20">'
    r'(?s)(\s*?)'
    r'<td class="show-for-small" colspan="7">'
    r'(?s)(\s*?)'
    r'\w{3}'
)

# Poseben vzorec za zadnji datum zadnjega matchdaya (pozor, en datum v celem matchdayu tudi poveže na to)
vzorec_zadnji_datum38 = (
    r'<td class="hide-for-small">'
    r'(?s)(\s*?)'
    r'(?P<dan>\w{3})'
    r'(?s)(\s*?)'
    r'\w*?<a href="https://www.transfermarkt.com/aktuell/waspassiertheute/aktuell/new/datum/\d{4}-\d{2}-\d{2}">'
    r'(?P<datum>.*?)</a>'
    r'(?s)(.*?)'
    r'<div class="table-footer">'
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

laliga = uvozi_datoteko(r'.\html\laliga.html')
seriea = uvozi_datoteko(r'.\html\seriea.html')
premierleague = uvozi_datoteko(r'.\html\premierleague.html')


i = 0

for zadetek in re.finditer(vzorec_tekma,laliga):
    i += 1
    print(i)
    print(zadetek['domaca_ekipa'] + '   '+ zadetek['zadetki_domaci']+ ':' + zadetek['zadetki_gostje'] + '   ' + zadetek['gostujoca_ekipa'])

for zadetek in re.finditer(vzorec_tekma,seriea):
    i += 1
    print(i)
    print(zadetek['domaca_ekipa'] + '   '+ zadetek['zadetki_domaci']+ ':' + zadetek['zadetki_gostje'] + '   ' + zadetek['gostujoca_ekipa'])

for zadetek in re.finditer(vzorec_tekma,premierleague):
    i += 1
    print(i)
    print(zadetek['domaca_ekipa'] + '   '+ zadetek['zadetki_domaci']+ ':' + zadetek['zadetki_gostje'] + '   ' + zadetek['gostujoca_ekipa'])