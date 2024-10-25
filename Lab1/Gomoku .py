# Łukasz Reinke s15037 NAI Lab1

# Gra Gomoku (Pięć w rzędzie) w Pythonie
# Instrukcja uruchomienia:
# 1. Zainstaluj easyAI: wpisz w terminalu: pip install easyAI
# 2. Uruchom grę w terminalu za pomocą: python gomoku.py
# 3. Graj jako Gracz 1 (symbol "O"), podając współrzędne ruchu w formacie (x, y).
#    Gracz 2 to AI, które wybiera losowy ruch.
# Celem gry jest ułożenie pięciu symboli w rzędzie (pionowo, poziomo lub ukośnie).

import random
from easyAI import TwoPlayerGame, Human_Player, AI_Player


class Gomoku(TwoPlayerGame):
    def __init__(self, players, size=15):
        # Inicjalizacja gry: ustawienie graczy, rozmiaru planszy i bieżącego gracza
        self.players = players  # Lista graczy (człowiek lub AI)
        self.size = size  # Ustalony rozmiar planszy, domyślnie 15x15
        self.board = [[0 for _ in range(size)] for _ in range(size)]  # Tworzenie pustej planszy jako tablicy 2D
        self.current_player = 1  # Ustawienie Gracza 1 jako zaczynającego grę

    def possible_moves(self):
        # Zwraca listę wszystkich dostępnych ruchów (wszystkie puste pola na planszy)
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]

    def make_move(self, move):
        # Wykonuje ruch na planszy, ustawiając bieżącego gracza na wybranym polu
        x, y = move
        self.board[x][y] = self.current_player

    def unmake_move(self, move):
        # Cofa ruch, ustawiając wybrane pole na 0 (przydatne w algorytmach AI)
        x, y = move
        self.board[x][y] = 0

    def lose(self):
        # Sprawdza, czy bieżący gracz ustawił linię 5, co w tym przypadku oznacza jego wygraną
        for x in range(self.size):
            for y in range(self.size):
                if self.check_line(x, y):  # Wywołuje sprawdzanie w różnych kierunkach
                    return True
        return False

    def check_line(self, x, y):
        # Sprawdza, czy na planszy jest linia 5 pionków bieżącego gracza w jednym kierunku
        for direction in [(1, 0), (0, 1), (1, 1), (1, -1)]:  # Kierunki: pionowo, poziomo, ukośnie
            dx, dy = direction
            if all(0 <= x + i * dx < self.size and 0 <= y + i * dy < self.size and
                   self.board[x + i * dx][y + i * dy] == self.current_player for i in range(5)):
                return True  # Znaleziono linię 5 w jednym kierunku
        return False

    def is_over(self):
        # Gra kończy się, jeśli ktoś wygra lub jeśli nie ma możliwych ruchów
        return self.possible_moves() == [] or self.lose()

    def show(self):
        # Wyświetla aktualny stan planszy, używając symboli dla graczy: '.' dla pustego pola, 'O' dla Gracza 1, 'X' dla Gracza 2
        symbols = ['.', 'O', 'X']
        for row in self.board:
            print(" ".join([symbols[cell] for cell in row]))  # Tworzy wizualną reprezentację planszy

    def scoring(self):
        # Zwraca wynik dla AI - -100 punktów dla przegranej, 0 dla pozostałych stanów
        return -100 if self.lose() else 0

    def play(self):
        # Główna pętla rozgrywki - kontynuuje grę do momentu zakończenia
        while not self.is_over():
            self.show()  # Wyświetla planszę przed wykonaniem ruchu
            move = self.player.ask_move(self)  # Pobiera ruch od gracza (człowieka lub AI)
            self.make_move(move)  # Wykonuje ruch na planszy
            print(f"Gracz {self.current_player} wykonał ruch na pozycję {move}")  # Wyświetla komunikat o ruchu
            if self.lose():  # Sprawdza, czy bieżący gracz ustawił linię pięciu, co oznacza jego wygraną
                print(f"Gracz {self.current_player} wygrał!")  # Wyświetla komunikat o wygranej
                break  # Kończy pętlę, jeśli gra została wygrana
            # Przełącza bieżącego gracza na przeciwnika
            self.current_player = 2 if self.current_player == 1 else 1  # Przełączanie current_player

        self.show()  # Wyświetla końcowy stan planszy po zakończeniu gry


# Konfiguracja gry - Human_Player przeciwko AI_Player, który wybiera losowy ruch
game = Gomoku([Human_Player(), AI_Player(lambda game: random.choice(game.possible_moves()))])

# Rozpoczęcie gry
game.play()
