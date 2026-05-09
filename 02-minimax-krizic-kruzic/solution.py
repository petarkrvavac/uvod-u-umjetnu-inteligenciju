# Kod za lab. zadatak: Krizic-kruzic (Tic-Tac-Toe) s Minimax algoritmom

# -----------------
# 1. FUNKCIJE ZA PLOCU
# -----------------

def create_board():
    """Vraca praznu 3x3 plocu."""
    return [' '] * 9


def print_board(board):
    """Ispisuje plocu u formatu 3x3."""
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")


def get_possible_moves(board):
    """Vraca listu indeksa slobodnih polja."""
    return [i for i, spot in enumerate(board) if spot == ' ']


def is_terminal_state(board):
    """Provjerava je li igra gotova (pobjednik ili nerijeseno)."""
    return check_winner(board) is not None or not get_possible_moves(board)


def check_winner(board):
    """
    Provjerava pobjednika. Vraca 'X', 'O', ili None.
    Ako je nerijeseno (iako nema pobjednika), vraca None.
    """
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Redovi
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Stupci
        (0, 4, 8), (2, 4, 6)  # Dijagonale
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != ' ':
            return board[combo[0]]  # Vraca 'X' ili 'O'

    return None


# -----------------
# 2. MINIMAX ALGORITAM
# -----------------

def utility(board):
    """Isplatna funkcija (utility) za Minimax."""
    winner = check_winner(board)
    if winner == 'O':
        return 1  # Racunalo (MAX) pobjeduje
    elif winner == 'X':
        return -1  # Covjek (MIN) pobjeduje
    else:
        return 0  # Nerijeseno


def minimax(board, is_max_turn):
    """
    Glavna Minimax funkcija. Rekurzivno prolazi stablo igre.
    Vraca (vrijednost, potez). Potez je relevantan samo u korijenu.
    """
    # Baza rekurzije: Ako je zavrsno stanje, vrati utility vrijednost
    if is_terminal_state(board):
        return utility(board), None

    if is_max_turn:
        # MAX (Racunalo): Maksimizira
        best_value = -float('inf')
        best_move = None

        # Iterira kroz sve moguce poteze
        for move in get_possible_moves(board):
            # Simuliraj potez
            board[move] = 'O'
            # Rekurzivni poziv: sljedeci je MIN igrac
            value, _ = minimax(board, False)
            # Ponisti simulirani potez (vracanje stanja)
            board[move] = ' '

            # Azuriraj najbolju vrijednost
            if value > best_value:
                best_value = value
                best_move = move

        return best_value, best_move
    else:
        # MIN (Covjek): Minimizira
        best_value = float('inf')
        best_move = None  # Potez nije potreban, ali se vraca radi simetrije

        for move in get_possible_moves(board):
            # Simuliraj potez
            board[move] = 'X'
            # Rekurzivni poziv: sljedeci je MAX igrac
            value, _ = minimax(board, True)
            # Ponisti simulirani potez
            board[move] = ' '

            # Azuriraj najbolju vrijednost
            if value < best_value:
                best_value = value
                best_move = move

        return best_value, best_move


# -----------------
# 3. GLAVNA LOGIKA IGRE
# -----------------

def play_game():
    """Glavna funkcija za vodenje igre."""
    board = create_board()
    current_player = 'X'  # Covjek (MIN) uvijek pocinje

    print("Zapocela je igra Krizic-kruzic!")
    print("Vi ste 'X', Racunalo je 'O'.")

    # Pomocna tablica za indekse
    print("Pozicije na ploci (indeksi 0-8):")
    print(f"\n 0 | 1 | 2 ")
    print("---|---|---")
    print(f" 3 | 4 | 5 ")
    print("---|---|---")
    print(f" 6 | 7 | 8 \n")

    print_board(board)

    while not is_terminal_state(board):
        if current_player == 'X':
            # Potez Covjeka (MIN)
            try:
                move = int(input(f"Vi ste na potezu ({current_player}). Unesite poziciju (0-8): "))
                if move not in range(9) or board[move] != ' ':
                    print("Neispravan potez. Pokusajte ponovno.")
                    continue
                board[move] = 'X'
                current_player = 'O'
            except ValueError:
                print("Neispravan unos. Unesite broj od 0 do 8.")
                continue
        else:
            # Potez Racunala (MAX)
            print("Racunalo razmislja...")
            # Pozivanje Minimaxa za odredivanje najboljeg poteza
            _, best_move = minimax(board, True)

            # Izvrsavanje najboljeg poteza
            if best_move is not None:
                board[best_move] = 'O'
                print(f"Racunalo igra na poziciji: {best_move}")
                current_player = 'X'

        print_board(board)

    # Ispis rezultata
    final_winner = check_winner(board)
    if final_winner == 'X':
        print("Kraj igre! Vi ste pobijedili!")
    elif final_winner == 'O':
        print("Kraj igre! Racunalo (Minimax) je pobijedilo!")
    else:
        print("Kraj igre! Nerijeseno je!")

# Pokretanje igre (za testiranje rjesenja)
play_game()
