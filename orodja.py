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

vzorec_zadnji_datum = (
    r'<td class="hide-for-small">'
    r'(?s)(\s*?)'
    r'(?P<dan>\w{3})'
    r'(?s)(\s*?)'
    r'\w*?<a href="https://www.transfermarkt.com/aktuell/waspassiertheute/aktuell/new/datum/\d{4}-\d{2}-\d{2}">'
    r'(?P<datum>.*?)</a>'
    r'(?s)(.*?)'
    r'<div class="table-footer">'
)

vzorec_ura = (
    r'<td class="show-for-small" colspan="7">'
	r'(?s)(\s*?)'
    r'(?P<ura>\d{1,2}:\d\d (AM|PM))?'
    r'(?s)(\s*?)'
    r'</td>'
    r'(?s)(.*?)'
    r'<tr class="bg_blau_20">?'
)

# Vzorec za tekmo znotraj datuma in časa
vzorec_tekma = (
    r''
)

laliga = uvozi_datoteko('.\html\laliga.html')

i = 0
#for zadetek in re.finditer(vzorec_datum, laliga):
#    print(zadetek['datum'])
for zadetek in re.finditer(vzorec_ura,laliga):
    print(zadetek['ura'])
#    print(zadetek['matchday']) 