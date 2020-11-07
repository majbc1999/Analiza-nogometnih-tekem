def stevilka_matchdaya(niz):
    stevila = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    nov_niz = ""
    for crka in niz:
        if crka in stevila:
            nov_niz += crka
    return nov_niz

print(stevilka_matchdaya("25. Matchday"))