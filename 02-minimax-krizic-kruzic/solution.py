# Kôd za lab. zadatak: Križić-kružić (Tic-Tac-Toe) s Minimax algoritmom

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# -----------------
# 1. FUNKCIJE ZA PLOČU
# -----------------

def create_board():
    """Vraća praznu 3x3 ploču."""
    return [' '] * 9


def print_board(board):
    """Ispisuje ploču u formatu 3x3."""
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")


def get_possible_moves(board):
    """Vraća listu indeksa slobodnih polja."""
    return [i for i, spot in enumerate(board) if spot == ' ']


def is_terminal_state(board):
    """Provjerava je li igra gotova (pobjednik ili neriješeno)."""
    return check_winner(board) is not None or not get_possible_moves(board)


def check_winner(board):
    """
    Provjerava pobjednika. Vraća 'X', 'O', ili None.
    Ako je neriješeno (iako nema pobjednika), vraća None.
    """
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Redovi
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Stupci
        (0, 4, 8), (2, 4, 6)  # Dijagonale
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != ' ':
            return board[combo[0]]  # Vraća 'X' ili 'O'

    return None


# -----------------
# 2. MINIMAX ALGORITAM
# -----------------

def utility(board):
    """Isplatna funkcija (utility) za Minimax."""
    winner = check_winner(board)
    if winner == 'O':
        return 1  # Računalo (MAX) pobjeđuje
    elif winner == 'X':
        return -1  # Čovjek (MIN) pobjeđuje
    else:
        return 0  # Neriješeno


def minimax(board, is_max_turn):
    """
    Glavna Minimax funkcija. Rekurzivno prolazi stablo igre.
    Vraća (vrijednost, potez). Potez je relevantan samo u korijenu.
    """
    # Baza rekurzije: Ako je završno stanje, vrati utility vrijednost
    if is_terminal_state(board):
        return utility(board), None

    if is_max_turn:
        # MAX (Računalo): Maksimizira
        best_value = -float('inf')
        best_move = None

        # Iterira kroz sve moguće poteze
        for move in get_possible_moves(board):
            # Simuliraj potez
            board[move] = 'O'
            # Rekurzivni poziv: sljedeci je MIN igrac
            value, _ = minimax(board, False)
            # Poništi simulirani potez (vraćanje stanja)
            board[move] = ' '

            # Ažuriraj najbolju vrijednost
            if value > best_value:
                best_value = value
                best_move = move

        return best_value, best_move
    else:
        # MIN (Čovjek): Minimizira
        best_value = float('inf')
        best_move = None  # Potez nije potreban, ali se vraća radi simetrije

        for move in get_possible_moves(board):
            # Simuliraj potez
            board[move] = 'X'
            # Rekurzivni poziv: sljedeci je MAX igrac
            value, _ = minimax(board, True)
            # Poništi simulirani potez
            board[move] = ' '

            # Ažuriraj najbolju vrijednost
            if value < best_value:
                best_value = value
                best_move = move

        return best_value, best_move


# -----------------
# 3. GLAVNA LOGIKA IGRE
# -----------------

def play_game():
    """Glavna funkcija za vođenje igre."""
    board = create_board()
    current_player = 'X'  # Čovjek (MIN) uvijek počinje

    print("Započela je igra Križić-kružić!")
    print("Vi ste 'X', Računalo je 'O'.")

    # Pomoćna tablica za indekse
    print("Pozicije na ploči (indeksi 0-8):")
    print(f"\n 0 | 1 | 2 ")
    print("---|---|---")
    print(f" 3 | 4 | 5 ")
    print("---|---|---")
    print(f" 6 | 7 | 8 \n")

    print_board(board)

    while not is_terminal_state(board):
        if current_player == 'X':
            # Potez Čovjeka (MIN)
            try:
                move = int(input(f"Vi ste na potezu ({current_player}). Unesite poziciju (0-8): "))
                if move not in range(9) or board[move] != ' ':
                    print("Neispravan potez. Pokušajte ponovno.")
                    continue
                board[move] = 'X'
                current_player = 'O'
            except ValueError:
                print("Neispravan unos. Unesite broj od 0 do 8.")
                continue
        else:
            # Potez Računala (MAX)
            print("Računalo razmišlja...")
            # Pozivanje Minimaxa za određivanje najboljeg poteza
            _, best_move = minimax(board, True)

            # Izvršavanje najboljeg poteza
            if best_move is not None:
                board[best_move] = 'O'
                print(f"Računalo igra na poziciji: {best_move}")
                current_player = 'X'

        print_board(board)

    # Ispis rezultata
    final_winner = check_winner(board)
    if final_winner == 'X':
        print("Kraj igre! Vi ste pobijedili!")
    elif final_winner == 'O':
        print("Kraj igre! Računalo (Minimax) je pobijedilo!")
    else:
        print("Kraj igre! Neriješeno je!")

# Pokretanje igre (za testiranje rješenja)
play_game()
