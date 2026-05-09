# Rješenje zadatka: Implementacija ID3 algoritma za izgradnju stabla odlučivanja
# Cilj: koristiti informational gain (IG) za izbor značajke pri razdvajanju

import math
import sys
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 1. KORAK: Definiranje skupa podataka
# Podaci su lista rječnika, svaki rječnik predstavlja jedan primjer (instance)
# Svaki primjer ima 4 značajke: 'Vrijeme', 'Temp', 'Vlažnost', 'Vjetar' i ciljnu klasu 'Odbojka'
dataset = [
    {'Vrijeme': 'sunčano', 'Temp': 'visoka', 'Vlažnost': 'visoka', 'Vjetar': 'slab', 'Odbojka': 'ne'},
    {'Vrijeme': 'sunčano', 'Temp': 'visoka', 'Vlažnost': 'visoka', 'Vjetar': 'jak',  'Odbojka': 'ne'},
    {'Vrijeme': 'oblačno', 'Temp': 'visoka', 'Vlažnost': 'visoka', 'Vjetar': 'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kišno',   'Temp': 'srednja','Vlažnost': 'visoka', 'Vjetar': 'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kišno',   'Temp': 'niska',  'Vlažnost': 'normalna','Vjetar':'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kišno',   'Temp': 'niska',  'Vlažnost': 'normalna','Vjetar':'jak',  'Odbojka': 'ne'},
    {'Vrijeme': 'oblačno', 'Temp': 'niska',  'Vlažnost': 'normalna','Vjetar':'jak',  'Odbojka': 'da'},
    {'Vrijeme': 'sunčano', 'Temp': 'srednja','Vlažnost': 'visoka', 'Vjetar': 'slab', 'Odbojka': 'ne'},
    {'Vrijeme': 'sunčano', 'Temp': 'niska',  'Vlažnost': 'normalna','Vjetar':'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kišno',   'Temp': 'srednja','Vlažnost': 'normalna','Vjetar':'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'sunčano', 'Temp': 'srednja','Vlažnost': 'normalna','Vjetar':'jak',  'Odbojka': 'da'},
    {'Vrijeme': 'oblačno', 'Temp': 'srednja','Vlažnost': 'visoka', 'Vjetar': 'jak',  'Odbojka': 'da'},
    {'Vrijeme': 'oblačno', 'Temp': 'visoka', 'Vlažnost': 'normalna','Vjetar':'slab', 'Odbojka': 'da'},
    {'Vrijeme': 'kišno',   'Temp': 'srednja','Vlažnost': 'visoka', 'Vjetar': 'jak',  'Odbojka': 'ne'}
]

# 2. KORAK: Pomoćne funkcije za Entropiju i Informacijsku dobit

def calculate_entropy(data, target_attr):
    """Računa entropiju skupa podataka za ciljnu značajku target_attr.

    Entropija mjeri nesigurnost/nesortiranost ciljne varijable u skupu.
    Formula: - sum(p_i * log2(p_i)) gdje su p_i relativne frekvencije klasa.

    Ulaz:
        data: lista rječnika (primjer)
        target_attr: ime ciljne značajke (string)
    Povratna vrijednost:
        entropija (float)
    """
    n = len(data)
    if n == 0:
        # Ako nema primjera, entropija je 0 (nema nesigurnosti jer nema podataka)
        return 0

    # Prebroj pojavljivanja svake vrijednosti ciljne značajke
    counts = Counter([row[target_attr] for row in data])
    entropy = 0

    # Sumarno računamo -p * log2(p) po svakoj klasi
    for count in counts.values():
        p = count / n
        entropy -= p * math.log2(p)
    return entropy


def calculate_information_gain(data, feature, target_attr):
    """Računa informacijsku dobit IG(data, feature).

    IG = Entropija(D) - sum_v (|D_v|/|D| * Entropija(D_v))
    gdje je D_v podskup primjera koji imaju vrijednost feature = v.

    Ulaz:
        data: lista primjera
        feature: ime značajke za koju računamo IG
        target_attr: ime ciljne značajke
    Povratna vrijednost:
        informational gain (float)
    """
    total_entropy = calculate_entropy(data, target_attr)
    n = len(data)

    # Dobavimo sve jedinstvene vrijednosti značajke u trenutnom skupu
    feature_values = set([row[feature] for row in data])
    weighted_entropy = 0

    # Za svaku vrijednost značajke izračunamo entropiju podskupa i težimo ju s relativnom veličinom podskupa
    for val in feature_values:
        subset = [row for row in data if row[feature] == val]
        p = len(subset) / n
        weighted_entropy += p * calculate_entropy(subset, target_attr)

    # IG je smanjenje entropije
    return total_entropy - weighted_entropy

# 3. KORAK: Glavni ID3 Algoritam

def id3(data, features, target_attr, parent_class=None):
    """Rekurzivna funkcija koja gradi stablo odlučivanja vraćanjem ugniježđene strukture rječnika.

    Struktura stabla (primjer):
        {'Vrijeme': {'sunčano': {'Vlažnost': {'visoka': 'ne', 'normalna': 'da'}},
                     'kišno': 'da',
                     ...}}

    Ulaz:
        data: trenutni skup podataka (lista rječnika)
        features: lista preostalih značajki koje se mogu koristiti za dijeljenje
        target_attr: ime ciljne značajke
        parent_class: najčešća klasa roditeljskog čvora (koristi se kad je podskup prazan)
    Povratna vrijednost:
        ili string (klasa) za listove, ili rječnik koji predstavlja čvor
    """
    # Izdvoji sve ciljne oznake u trenutnom čvoru
    targets = [row[target_attr] for row in data]

    # Baza rekurzije 1: Ako je skup prazan, vraćamo najčešću klasu roditelja (fallback)
    if not data:
        return parent_class

    # Baza rekurzije 2: Ako svi primjeri imaju istu klasu, vraća se ta klasa (list)
    if len(set(targets)) == 1:
        return targets[0]

    # Baza rekurzije 3: Ako nema više značajki za razdvajanje, vrati najčešću klasu u ovom čvoru
    if not features:
        return Counter(targets).most_common(1)[0][0]

    # Spremimo najčešću klasu u trenutnom čvoru za slučaj da neki podskup bude prazan
    parent_class = Counter(targets).most_common(1)[0][0]

    # Odaberemo značajku s najvećom informacijskom dobiti
    item_gains = {feat: calculate_information_gain(data, feat, target_attr) for feat in features}
    # best_feature = ključ s maksimalnom vrijednošću IG
    best_feature = max(item_gains, key=item_gains.get)

    # Kreiramo čvor stabla; ključ je ime značajke, vrijednost je rječnik grana
    tree = {best_feature: {}}

    # Uklonimo odabranu značajku iz liste za daljnju rekurziju
    remaining_features = [f for f in features if f != best_feature]

    # Dohvatimo sve vrijednosti odabrane značajke u trenutnom podskupu
    feature_values = set([row[best_feature] for row in data])

    # Za svaku vrijednost značajke izgradimo podstablo rekurzivno
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
    """Ispis stabla u čitljivom (tekstualnom) obliku.

    Ako je node list (nije rječnik), ispisujemo klasu. Inače rekurzivno ispisujemo značajke i grane.
    """
    # Ako smo došli do lista (klase), ispišemo rezultat
    if not isinstance(tree, dict):
        print(indent + "=> KLASA: " + str(tree))
        return

    # Inače, za svaki čvor ispišemo naziv značajke i zatim grane
    for feature, branches in tree.items():
        print(indent + "[" + feature + "]")
        for value, subtree in branches.items():
            # Ispis grane (vrijednost značajke) na istoj liniji
            print(indent + "  " + str(value) + ": ", end="")
            if not isinstance(subtree, dict):
                # List/klasa - ispišemo odmah
                print("=> " + str(subtree))
            else:
                # Ako je podstablo, prelazimo u novi red i povećavamo uvlaku
                print()
                print_tree(subtree, indent + "    ")


def predict(tree, instance):
    """Klasifikacija novog primjera koristeći izgrađeno stablo.

    Algoritam: od korijena silazimo prema grani koja odgovara vrijednosti značajke u instance.
    Ako naiđemo na vrijednost koja nije u stablu vraćamo poruku da je nepoznata.
    """
    # Ako je tree list (string), vraćamo ga kao predikciju
    if not isinstance(tree, dict):
        return tree

    # Inače, uzmemo naziv značajke u korijenu
    root_feature = list(tree.keys())[0]
    # Vrijednost koju instanca ima za tu značajku
    input_val = instance.get(root_feature)

    # Pokušamo pronaći odgovarajuću granu prema vrijednosti
    subtree = tree[root_feature].get(input_val)

    # Ako vrijednost nije u stablo (nije viđena u treningu), vraćamo fallback string
    if subtree is None:
        return "Nepoznato (vrijednost nije u trening skupu)"

    # Inače, nastavljamo rekurzivno
    return predict(subtree, instance)

# --- IZVRŠAVANJE (glavni dio koji pokreće učenje i demonstraciju) ---

attributes = ['Vrijeme', 'Temp', 'Vlažnost', 'Vjetar']
target = 'Odbojka'

# Izgradnja stabla pozivom ID3 funkcije
decision_tree = id3(dataset, attributes, target)
# Ispišemo dobiveno stablo
print_tree(decision_tree)

# Primjer za testiranje predikcije
new_sample = {'Vrijeme': 'kišno', 'Temp': 'niska', 'Vlažnost': 'normalna', 'Vjetar': 'jak'}
prediction = predict(decision_tree, new_sample)

print(f"Ulaz: {new_sample}")
print(f"Predikcija: {prediction}")
