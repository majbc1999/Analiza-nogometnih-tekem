import re

def relacija_datumov(dat, dat2): #Vrne True če je dat2 nujno po dat sicer False
    if int(dat[0]) < int(dat2[0]):
        return True
    elif int(dat[0]) == int(dat2[0]):
        if int(dat[1]) < int(dat2[1]):
            return True
        elif int(dat[1]) == int(dat2[1]):
            if int(dat[2]) < int(dat2[2]):
                return True
            else: return False
        else: return False
    else: return False


# Funkcija, ki iz stringa datuma naredi seznam intov

vzorec_datuma = (
    r'(?P<mesec>\d{1,2})'
    r'/'
    r'(?P<dan>\d{1,2})'
    r'/'
    r'(?P<leto>\d{1,2})'
)

def izlusci_datum(dat):
    for datum in re.finditer(vzorec_datuma, dat):
        leto = datum['leto']
        mesec = datum['mesec']
        dan = datum['dan']
        return float(leto) + 1 / 12 * (float(mesec) - 1) + 1 / 12 * 1 / 31 * (float(dan) - 1)

#print(izlusci_datum("12/31/20"))