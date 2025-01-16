# Autor: Łukasz Reinke s15037@pjwstk.edu.pl
# Projekt: Wykrywanie twarzy z rysowaniem celownika na zielonych twarzach
#
# Opis problemu:
# Celem projektu jest stworzenie aplikacji, która wykrywa twarze w obrazie wideo przechwytywanym z kamery,
# sprawdza, czy centrum twarzy jest koloru zielonego, i w przypadku pozytywnego wyniku rysuje celownik
# na twarzy. Aplikacja korzysta z biblioteki OpenCV do przetwarzania obrazu i wykrywania twarzy.
#
# Instrukcja użycia:
# 1. Zainstaluj bibliotekę OpenCV: `pip install opencv-python-headless`
# 2. Uruchom skrypt: `python baba_jaga_patrzy.pl`
# 3. Aby zakończyć program, naciśnij klawisz "q".
#
# Wymagania:
# - Kamera internetowa podłączona do urządzenia.
# - Zainstalowane biblioteki: numpy, opencv-python-headless.

import cv2
import numpy as np

# Funkcja do wykrywania twarzy i rysowania celownika
def detect_and_target_face(image):
    """
    Wykrywa twarze w obrazie i rysuje celownik na twarzach, których centrum jest koloru zielonego.

    Parametry:
        image (numpy.ndarray): Obraz w postaci macierzy BGR.
    """
    # Konwersja obrazu na skalę szarości
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Ładowanie klasyfikatora Haar do wykrywania twarzy
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Wykrywanie twarzy w obrazie
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Iteracja po wykrytych twarzach
    for (x, y, w, h) in faces:
        # Pobranie koloru w centrum twarzy
        face_center_color = image[y + h // 2, x + w // 2]

        # Sprawdzenie, czy kolor jest zielony
        if is_color_green(face_center_color):
            # Rysowanie celownika
            cv2.circle(image, (x + w // 2, y + h // 2), min(w, h) // 2, (0, 255, 0), 2)

# Funkcja do sprawdzania, czy kolor jest zielony
def is_color_green(bgr_color):
    """
    Sprawdza, czy podany kolor w przestrzeni BGR mieści się w zakresie zielonego w przestrzeni HSV.

    Parametry:
        bgr_color (numpy.ndarray): Kolor w przestrzeni BGR.

    Zwraca:
        bool: True, jeśli kolor jest zielony, w przeciwnym wypadku False.
    """
    # Przekształcanie koloru na obraz 1x1x3
    bgr_color = np.uint8([[bgr_color]])

    # Konwersja koloru z BGR na HSV
    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)

    # Zakres koloru zielonego w przestrzeni HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Sprawdzenie, czy kolor mieści się w zakresie zielonego
    mask = cv2.inRange(hsv_color, lower_green, upper_green)
    return np.any(mask)

# Inicjalizacja kamery
cap = cv2.VideoCapture(0)

# Pętla do przechwytywania obrazu z kamery
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Przetworzenie obrazu
    detect_and_target_face(frame)

    # Wyświetlenie obrazu
    cv2.imshow('Camera Feed - Targeted Faces', frame)

    # Warunek na zamknięcie okna
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnienie kamery i zamknięcie wszystkich okien
cap.release()
cv2.destroyAllWindows()

# Dane do uczenia algorytmu:
# 1. Zbierz zdjęcia twarzy w różnych warunkach oświetleniowych.
# 2. Zadbaj o balans kolorów i różnorodność kolorów wokół twarzy.
# 3. Utwórz odpowiedni zestaw danych testowych i treningowych do analizy HSV.
