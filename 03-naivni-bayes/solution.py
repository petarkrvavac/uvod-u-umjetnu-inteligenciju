# Naivni Bayes klasifikator - Odbojka na pijesku (da / ne)
# Ovaj program implementira jednostavan Naivni Bayesov klasifikator
# koji predviđa hoće li se igrati odbojka na pijesku (da/ne)
# na temelju vremenskih uvjeta: vrijeme, temperatura, vlaga, vjetar.
# Naivni Bayes koristi Bayesov teorem uz pretpostavku nezavisnosti
# atributa ("naivna" pretpostavka)

import sys
from collections import defaultdict  # Omogućuje rječnik s default vrijednostima

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 1) Ulazni podaci - skup za treniranje
# Svaki redak sadrži: (vrijeme, temperatura, vlaga, vjetar, odluka)
podatci = [
    ("sunčano",  "visoka",  "visoka",   "slab", "ne"),
    ("sunčano",  "visoka",  "visoka",   "jak",  "ne"),
    ("oblačno",  "visoka",  "visoka",   "slab", "da"),
    ("kišno",    "srednja", "visoka",   "slab", "da"),
    ("kišno",    "niska",   "normalna", "slab", "da"),
    ("kišno",    "niska",   "normalna", "jak",  "ne"),
    ("oblačno",  "niska",   "normalna", "jak",  "da"),
    ("sunčano",  "srednja", "visoka",   "slab", "ne"),
    ("sunčano",  "niska",   "normalna", "slab", "da"),
    ("kišno",    "srednja", "normalna", "slab", "da"),
    ("sunčano",  "srednja", "normalna", "jak",  "da"),
    ("oblačno",  "srednja", "visoka",   "jak",  "da"),
    ("oblačno",  "visoka",  "normalna", "slab", "da"),
    ("kišno",    "srednja", "visoka",   "jak",  "ne"),
]

# 2) Izračun svih potrebnih vjerojatnosti

# Prior vjerojatnosti P(da) i P(ne) - koliko često se igra/ne igra
# defaultdict(int) stvara rječnik gdje nepostojeći ključevi vraćaju 0
prior = defaultdict(int)

# Uvjetne (kondicionalne) vjerojatnosti P(atribut | klasa)
# Za svaku klasu ("da"/"ne") brojimo pojavljivanja svake vrijednosti atributa
cond = {
    "da": defaultdict(int),  # Brojač za klasu "da"
    "ne": defaultdict(int)   # Brojač za klasu "ne"
}

# Prolazimo kroz sve podatke i brojimo pojavljivanja
for (vrijeme, temp, vlaga, vjetar, y) in podatci:
    prior[y] += 1  # Povećaj brojač za klasu y (da ili ne)
    # Brojimo koliko puta se svaka vrijednost atributa pojavljuje uz klasu y
    cond[y][("vrijeme", vrijeme)] += 1
    cond[y][("temp", temp)] += 1
    cond[y][("vlaga", vlaga)] += 1
    cond[y][("vjetar", vjetar)] += 1

N = len(podatci)  # Ukupan broj primjera u skupu za treniranje

# Funkcija za izračun vjerodostojnosti (likelihood)
# Računa: P(vrijeme|y) * P(temp|y) * P(vlaga|y) * P(vjetar|y)
def likelihood(vrijeme, temp, vlaga, vjetar, y):
    """
    Izračunava umnožak uvjetnih vjerojatnosti svih atributa za danu klasu.
    
    Parametri:
        vrijeme, temp, vlaga, vjetar - vrijednosti atributa novog primjera
        y - klasa ("da" ili "ne")
    
    Vraća:
        float - umnožak P(atribut_i | klasa) za sve atribute
    """
    ukupno_y = prior[y]  # Koliko primjera ima klasu y

    p = 1.0  # Početna vrijednost umnoška

    # Množimo uvjetne vjerojatnosti za svaki atribut
    p *= cond[y][("vrijeme", vrijeme)] / ukupno_y  # P(vrijeme | y)
    p *= cond[y][("temp", temp)]       / ukupno_y  # P(temperatura | y)
    p *= cond[y][("vlaga", vlaga)]     / ukupno_y  # P(vlaga | y)
    p *= cond[y][("vjetar", vjetar)]   / ukupno_y  # P(vjetar | y)

    return p

# 3) Glavna funkcija – predikcija nove instance
def predict(novi_podatak):
    """
    Računa P(da) * P(atributi|da) i P(ne) * P(atributi|ne),
    te vraća klasu s većom vrijednošću.
    
    Parametri:
        novi_podatak - tuple (vrijeme, temp, vlaga, vjetar)
    
    Vraća:
        str - "da" ako se predviđa igra, inače "ne"
    """
    vrijeme, temp, vlaga, vjetar = novi_podatak  # Raspakiraj atribute

    # Bayesova formula:
    # P(klasa | atributi) ∝ P(klasa) * P(atributi | klasa)
    p_da = (prior["da"] / N) * likelihood(vrijeme, temp, vlaga, vjetar, "da")
    p_ne = (prior["ne"] / N) * likelihood(vrijeme, temp, vlaga, vjetar, "ne")

    # Vraćamo klasu s većom vjerojatnošću
    return "da" if p_da > p_ne else "ne"

# 4) Primjer izvođenja - testiranje klasifikatora
if __name__ == "__main__":
    print("NAIVNI BAYES - Odbojka (da/ne)")

    # Novi primjer za klasifikaciju
    unos = ("sunčano", "visoka", "normalna", "jak")
    print("Novi podatak:", unos)

    # Pozivamo predikciju i ispisujemo rezultat
    rezultat = predict(unos)
    print("Predikcija:", rezultat)
