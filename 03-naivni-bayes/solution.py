# Naivni Bayes klasifikator - Odbojka na pijesku (da / ne)
# Ovaj program implementira jednostavan Naivni Bayesov klasifikator
# koji predvida hoce li se igrati odbojka na pijesku (da/ne)
# na temelju vremenskih uvjeta: vrijeme, temperatura, vlaga, vjetar.
# Naivni Bayes koristi Bayesov teorem uz pretpostavku nezavisnosti
# atributa ("naivna" pretpostavka)

from collections import defaultdict  # Omogucuje rjecnik s default vrijednostima

# 1) Ulazni podaci - skup za treniranje
# Svaki redak sadrzi: (vrijeme, temperatura, vlaga, vjetar, odluka)
podatci = [
    ("suncano",  "visoka",  "visoka",   "slab", "ne"),
    ("suncano",  "visoka",  "visoka",   "jak",  "ne"),
    ("oblacno",  "visoka",  "visoka",   "slab", "da"),
    ("kisno",    "srednja", "visoka",   "slab", "da"),
    ("kisno",    "niska",   "normalna", "slab", "da"),
    ("kisno",    "niska",   "normalna", "jak",  "ne"),
    ("oblacno",  "niska",   "normalna", "jak",  "da"),
    ("suncano",  "srednja", "visoka",   "slab", "ne"),
    ("suncano",  "niska",   "normalna", "slab", "da"),
    ("kisno",    "srednja", "normalna", "slab", "da"),
    ("suncano",  "srednja", "normalna", "jak",  "da"),
    ("oblacno",  "srednja", "visoka",   "jak",  "da"),
    ("oblacno",  "visoka",  "normalna", "slab", "da"),
    ("kisno",    "srednja", "visoka",   "jak",  "ne"),
]

# 2) Izracun svih potrebnih vjerojatnosti

# Prior vjerojatnosti P(da) i P(ne) - koliko cesto se igra/ne igra
# defaultdict(int) stvara rjecnik gdje nepostojeci kljucevi vracaju 0
prior = defaultdict(int)

# Uvjetne (kondicionalne) vjerojatnosti P(atribut | klasa)
# Za svaku klasu ("da"/"ne") brojimo pojavljivanja svake vrijednosti atributa
cond = {
    "da": defaultdict(int),  # Brojac za klasu "da"
    "ne": defaultdict(int)   # Brojac za klasu "ne"
}

# Prolazimo kroz sve podatke i brojimo pojavljivanja
for (vrijeme, temp, vlaga, vjetar, y) in podatci:
    prior[y] += 1  # Povecaj brojac za klasu y (da ili ne)
    # Brojimo koliko puta se svaka vrijednost atributa pojavljuje uz klasu y
    cond[y][("vrijeme", vrijeme)] += 1
    cond[y][("temp", temp)] += 1
    cond[y][("vlaga", vlaga)] += 1
    cond[y][("vjetar", vjetar)] += 1

N = len(podatci)  # Ukupan broj primjera u skupu za treniranje

# Funkcija za izracun vjerodostojnosti (likelihood)
# Racuna: P(vrijeme|y) * P(temp|y) * P(vlaga|y) * P(vjetar|y)
def likelihood(vrijeme, temp, vlaga, vjetar, y):
    """
    Izracunava umnozak uvjetnih vjerojatnosti svih atributa za danu klasu.
    
    Parametri:
        vrijeme, temp, vlaga, vjetar - vrijednosti atributa novog primjera
        y - klasa ("da" ili "ne")
    
    Vraca:
        float - umnozak P(atribut_i | klasa) za sve atribute
    """
    ukupno_y = prior[y]  # Koliko primjera ima klasu y

    p = 1.0  # Pocetna vrijednost umnoska

    # Mnozimo uvjetne vjerojatnosti za svaki atribut
    p *= cond[y][("vrijeme", vrijeme)] / ukupno_y  # P(vrijeme | y)
    p *= cond[y][("temp", temp)]       / ukupno_y  # P(temperatura | y)
    p *= cond[y][("vlaga", vlaga)]     / ukupno_y  # P(vlaga | y)
    p *= cond[y][("vjetar", vjetar)]   / ukupno_y  # P(vjetar | y)

    return p

# 3) Glavna funkcija - predikcija nove instance
def predict(novi_podatak):
    """
    Racuna P(da) * P(atributi|da) i P(ne) * P(atributi|ne),
    te vraca klasu s vecom vrijednoscu.
    
    Parametri:
        novi_podatak - tuple (vrijeme, temp, vlaga, vjetar)
    
    Vraca:
        str - "da" ako se predvida igra, inace "ne"
    """
    vrijeme, temp, vlaga, vjetar = novi_podatak  # Raspakiraj atribute

    # Bayesova formula:
    # P(klasa | atributi) proporcionalno P(klasa) * P(atributi | klasa)
    p_da = (prior["da"] / N) * likelihood(vrijeme, temp, vlaga, vjetar, "da")
    p_ne = (prior["ne"] / N) * likelihood(vrijeme, temp, vlaga, vjetar, "ne")

    # Vracamo klasu s vecom vjerojatnoscu
    return "da" if p_da > p_ne else "ne"

# 4) Primjer izvodenja - testiranje klasifikatora
if __name__ == "__main__":
    print("NAIVNI BAYES - Odbojka (da/ne)")

    # Novi primjer za klasifikaciju
    unos = ("suncano", "visoka", "normalna", "jak")
    print("Novi podatak:", unos)

    # Pozivamo predikciju i ispisujemo rezultat
    rezultat = predict(unos)
    print("Predikcija:", rezultat)
