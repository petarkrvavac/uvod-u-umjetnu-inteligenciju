# Uvod u umjetnu inteligenciju

Laboratorijski zadaci iz kolegija Uvod u umjetnu inteligenciju na FSRE-u.
Zadaci pokrivaju osnovne algoritme pretraživanja, odlučivanja i klasifikacije implementirane u Pythonu bez vanjskih biblioteka.

## Što projekt pokazuje

- rad s prostorom stanja, heuristikama i prioritetnim redovima
- rekurzivno odlučivanje pomoću Minimax i ID3 algoritama
- osnovnu probabilističku klasifikaciju pomoću Naivnog Bayesa
- pisanje jednostavnih terminalskih programa i obradu ulaznih datoteka

## Pregled zadataka

| Zadatak | Tema | Što implementira |
| --- | --- | --- |
| `01-pretrazivanje-prostora-stanja` | Pretraživanje prostora stanja | BFS, UCS, A* te provjera optimističnosti i konzistentnosti heuristika |
| `02-minimax-krizic-kruzic` | Minimax algoritam | Interaktivna igra križić-kružić protiv računala |
| `03-naivni-bayes` | Naivni Bayes | Klasifikacija odluke o igranju odbojke na temelju vremenskih uvjeta |
| `04-id3-stablo-odlucivanja` | ID3 algoritam | Izgradnja stabla odlučivanja pomoću entropije i informacijske dobiti |

## Preduvjeti

Potreban je Python 3.6 ili noviji. Projekt koristi samo Python standardnu biblioteku, pa nisu potrebni dodatni paketi.

## Pokretanje

Primjeri koriste naredbu `python`. Ako na Windowsu nije dostupna, koristite `py` umjesto `python`.

### 1. Pretraživanje prostora stanja

```bash
cd 01-pretrazivanje-prostora-stanja
python solution.py --alg bfs --ss istra.txt
python solution.py --alg ucs --ss istra.txt
python solution.py --alg astar --ss istra.txt --h istra_heuristic.txt
```

Provjera heuristika:

```bash
python solution.py --ss istra.txt --h istra_heuristic.txt --check-optimistic
python solution.py --ss istra.txt --h istra_heuristic.txt --check-consistent
python solution.py --ss istra.txt --h istra_pessimistic_heuristic.txt --check-optimistic
```

Format datoteke prostora stanja (`istra.txt`):

- prvi redak sadrži početno stanje
- drugi redak sadrži ciljna stanja odvojena razmakom
- ostali redci sadrže prijelaze u obliku `stanje: susjed,cijena susjed,cijena`
- prazni redci i redci koji počinju znakom `#` se ignoriraju

Format datoteka heuristike (`istra_heuristic.txt` i `istra_pessimistic_heuristic.txt`):

- svaki redak sadrži heurističku vrijednost u obliku `stanje: vrijednost`
- prazni redci i redci koji počinju znakom `#` se ignoriraju

Primjer izlaza za BFS:

```text
# BFS
[FOUND_SOLUTION]: yes
[STATES_VISITED]: 15
[PATH_LENGTH]: 5
[TOTAL_COST]: 100.0
[PATH]: Pula => Barban => Labin => Lupoglav => Buzet
```

### 2. Minimax križić-kružić

```bash
cd 02-minimax-krizic-kruzic
python solution.py
```

Program pokreće interaktivnu igru u terminalu. Igrač koristi oznaku `X`, a računalo oznaku `O`. Potezi se unose kao brojevi od `0` do `8`, gdje svaki broj predstavlja jedno polje na ploči.

### 3. Naivni Bayes

```bash
cd 03-naivni-bayes
python solution.py
```

Program trenira jednostavni Naivni Bayes klasifikator na ugrađenom skupu podataka i ispisuje predikciju za novi primjer.

### 4. ID3 stablo odlučivanja

```bash
cd 04-id3-stablo-odlucivanja
python solution.py
```

Program izračunava entropiju i informacijsku dobit, gradi stablo odlučivanja te prikazuje primjer klasifikacije.
