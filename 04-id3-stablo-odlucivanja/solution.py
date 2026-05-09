# Rjesenje zadatka: Implementacija ID3 algoritma za izgradnju stabla odlucivanja
# Cilj: koristiti informational gain (IG) za izbor znacajke pri razdvajanju

import math
from collections import Counter

# 1. KORAK: Definiranje skupa podataka
# Podaci su lista rjecnika, svaki rjecnik predstavlja jedan primjer (instance)
# Svaki primjer ima 4 znacajke: 'Vrijeme', 'Temp', 'Vlaznost', 'Vjetar' i ciljnu klasu 'Odbojka'
dataset = [
    {'Vrijeme': 'suncano', 'Temp': 'visoka', 'Vlaznost': 'visoka', 'Vjetar': 'slab', 'Odbojka': 'ne'},
    {'Vrijeme': 'suncano', 'Temp': 'visoka', 'Vlaznost': 'visoka', 'Vjetar': 'jak',  'Odbojka': 'ne'},
    {'Vrijeme': 'oblacno', 'Temp': 'visoka', 'Vlaznost': 'visoka', 'Vjetar': 'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kisno',   'Temp': 'srednja','Vlaznost': 'visoka', 'Vjetar': 'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kisno',   'Temp': 'niska',  'Vlaznost': 'normalna','Vjetar':'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kisno',   'Temp': 'niska',  'Vlaznost': 'normalna','Vjetar':'jak',  'Odbojka': 'ne'},
    {'Vrijeme': 'oblacno', 'Temp': 'niska',  'Vlaznost': 'normalna','Vjetar':'jak',  'Odbojka': 'da'},
    {'Vrijeme': 'suncano', 'Temp': 'srednja','Vlaznost': 'visoka', 'Vjetar': 'slab', 'Odbojka': 'ne'},
    {'Vrijeme': 'suncano', 'Temp': 'niska',  'Vlaznost': 'normalna','Vjetar':'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kisno',   'Temp': 'srednja','Vlaznost': 'normalna','Vjetar':'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'suncano', 'Temp': 'srednja','Vlaznost': 'normalna','Vjetar':'jak',  'Odbojka': 'da'},
    {'Vrijeme': 'oblacno', 'Temp': 'srednja','Vlaznost': 'visoka', 'Vjetar': 'jak',  'Odbojka': 'da'},
    {'Vrijeme': 'oblacno', 'Temp': 'visoka', 'Vlaznost': 'normalna','Vjetar':'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kisno',   'Temp': 'srednja','Vlaznost': 'visoka', 'Vjetar': 'jak',  'Odbojka': 'ne'}
]

# 2. KORAK: Pomocne funkcije za Entropiju i Informacijsku dobit

def calculate_entropy(data, target_attr):
    """Racuna entropiju skupa podataka za ciljnu znacajku target_attr.

    Entropija mjeri nesigurnost/nesortiranost ciljne varijable u skupu.
    Formula: - sum(p_i * log2(p_i)) gdje su p_i relativne frekvencije klasa.

    Ulaz:
        data: lista rjecnika (primjer)
        target_attr: ime ciljne znacajke (string)
    Povratna vrijednost:
        entropija (float)
    """
    n = len(data)
    if n == 0:
        # Ako nema primjera, entropija je 0 (nema nesigurnosti jer nema podataka)
        return 0

    # Prebroj pojavljivanja svake vrijednosti ciljne znacajke
    counts = Counter([row[target_attr] for row in data])
    entropy = 0

    # Sumarno racunamo -p * log2(p) po svakoj klasi
    for count in counts.values():
        p = count / n
        entropy -= p * math.log2(p)
    return entropy


def calculate_information_gain(data, feature, target_attr):
    """Racuna informacijsku dobit IG(data, feature).

    IG = Entropija(D) - sum_v (|D_v|/|D| * Entropija(D_v))
    gdje je D_v podskup primjera koji imaju vrijednost feature = v.

    Ulaz:
        data: lista primjera
        feature: ime znacajke za koju racunamo IG
        target_attr: ime ciljne znacajke
    Povratna vrijednost:
        informational gain (float)
    """
    total_entropy = calculate_entropy(data, target_attr)
    n = len(data)

    # Dobavimo sve jedinstvene vrijednosti znacajke u trenutnom skupu
    feature_values = set([row[feature] for row in data])
    weighted_entropy = 0

    # Za svaku vrijednost znacajke izracunamo entropiju podskupa i tezimo ju s relativnom velicinom podskupa
    for val in feature_values:
        subset = [row for row in data if row[feature] == val]
        p = len(subset) / n
        weighted_entropy += p * calculate_entropy(subset, target_attr)

    # IG je smanjenje entropije
    return total_entropy - weighted_entropy

# 3. KORAK: Glavni ID3 Algoritam

def id3(data, features, target_attr, parent_class=None):
    """Rekurzivna funkcija koja gradi stablo odlucivanja vracanjem ugnijezdene strukture rjecnika.

    Struktura stabla (primjer):
        {'Vrijeme': {'suncano': {'Vlaznost': {'visoka': 'ne', 'normalna': 'da'}},
                     'kisno': 'da',
                     ...}}

    Ulaz:
        data: trenutni skup podataka (lista rjecnika)
        features: lista preostalih znacajki koje se mogu koristiti za dijeljenje
        target_attr: ime ciljne znacajke
        parent_class: najcesca klasa roditeljskog cvora (koristi se kad je podskup prazan)
    Povratna vrijednost:
        ili string (klasa) za listove, ili rjecnik koji predstavlja cvor
    """
    # Izdvoji sve ciljne oznake u trenutnom cvoru
    targets = [row[target_attr] for row in data]

    # Baza rekurzije 1: Ako je skup prazan, vracamo najcescu klasu roditelja (fallback)
    if not data:
        return parent_class

    # Baza rekurzije 2: Ako svi primjeri imaju istu klasu, vraca se ta klasa (list)
    if len(set(targets)) == 1:
        return targets[0]

    # Baza rekurzije 3: Ako nema vise znacajki za razdvajanje, vrati najcescu klasu u ovom cvoru
    if not features:
        return Counter(targets).most_common(1)[0][0]

    # Spremimo najcescu klasu u trenutnom cvoru za slucaj da neki podskup bude prazan
    parent_class = Counter(targets).most_common(1)[0][0]

    # Odaberemo znacajku s najvecom informacijskom dobiti
    item_gains = {feat: calculate_information_gain(data, feat, target_attr) for feat in features}
    # best_feature = kljuc s maksimalnom vrijednoscu IG
    best_feature = max(item_gains, key=item_gains.get)

    # Kreiramo cvor stabla; kljuc je ime znacajke, vrijednost je rjecnik grana
    tree = {best_feature: {}}

    # Uklonimo odabranu znacajku iz liste za daljnju rekurziju
    remaining_features = [f for f in features if f != best_feature]

    # Dohvatimo sve vrijednosti odabrane znacajke u trenutnom podskupu
    feature_values = set([row[best_feature] for row in data])

    # Za svaku vrijednost znacajke izgradimo podstablo rekurzivno
    for val in feature_values:
        # Podskup primjera koji imaju vrijednost best_feature == val
        subset = [row for row in data if row[best_feature] == val]
        # Rekurzivni poziv - roditeljska klasa se predaje za fallback
        subtree = id3(subset, remaining_features, target_attr, parent_class)
        # Dodamo granu u stablo
        tree[best_feature][val] = subtree

    return tree

# 4. KORAK: Funkcija za ispis stabla i predikciju

def print_tree(tree, indent=""):
    """Ispis stabla u citljivom (tekstualnom) obliku.

    Ako je node list (nije rjecnik), ispisujemo klasu. Inace rekurzivno ispisujemo znacajke i grane.
    """
    # Ako smo dosli do lista (klase), ispisemo rezultat
    if not isinstance(tree, dict):
        print(indent + "=> KLASA: " + str(tree))
        return

    # Inace, za svaki cvor ispisemo naziv znacajke i zatim grane
    for feature, branches in tree.items():
        print(indent + "[" + feature + "]")
        for value, subtree in branches.items():
            # Ispis grane (vrijednost znacajke) na istoj liniji
            print(indent + "  " + str(value) + ": ", end="")
            if not isinstance(subtree, dict):
                # List/klasa - ispisemo odmah
                print("=> " + str(subtree))
            else:
                # Ako je podstablo, prelazimo u novi red i povecavamo uvlaku
                print()
                print_tree(subtree, indent + "    ")


def predict(tree, instance):
    """Klasifikacija novog primjera koristeci izgradeno stablo.

    Algoritam: od korijena silazimo prema grani koja odgovara vrijednosti znacajke u instance.
    Ako naidemo na vrijednost koja nije u stablu vracamo poruku da je nepoznata.
    """
    # Ako je tree list (string), vracamo ga kao predikciju
    if not isinstance(tree, dict):
        return tree

    # Inace, uzmemo naziv znacajke u korijenu
    root_feature = list(tree.keys())[0]
    # Vrijednost koju instanca ima za tu znacajku
    input_val = instance.get(root_feature)

    # Pokusamo pronaci odgovarajucu granu prema vrijednosti
    subtree = tree[root_feature].get(input_val)

    # Ako vrijednost nije u stablo (nije videna u treningu), vracamo fallback string
    if subtree is None:
        return "Nepoznato (vrijednost nije u trening skupu)"

    # Inace, nastavljamo rekurzivno
    return predict(subtree, instance)

# --- IZVRSAVANJE (glavni dio koji pokrece ucenje i demonstraciju) ---

attributes = ['Vrijeme', 'Temp', 'Vlaznost', 'Vjetar']
target = 'Odbojka'

# Izgradnja stabla pozivom ID3 funkcije
decision_tree = id3(dataset, attributes, target)
# Ispisemo dobiveno stablo
print_tree(decision_tree)

# Primjer za testiranje predikcije
new_sample = {'Vrijeme': 'kisno', 'Temp': 'niska', 'Vlaznost': 'normalna', 'Vjetar': 'jak'}
prediction = predict(decision_tree, new_sample)

print(f"Ulaz: {new_sample}")
print(f"Predikcija: {prediction}")
