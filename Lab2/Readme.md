authors: Łukasz Reinke
emails: s15037@pjwstk.edu.pl
task: Car Wash

Zadaniem tego programu jest wyliczenie ceny za myjnię samochodową.
Mamy 3 wejścia
    Wielkość samochodu (car_size) : od 0 - 100, gdzie 100 Van a 0 Hatchback. 
    Ilość odwiedzeń w miesiącu (visit_count) : od 0 - 10, gdzie 10 to jest 10 odwiedzeń
    Wielkość zabrudzenia (dirt_level) : od 0 - 10, gdzie 0 to lekko brudny

I 1 wyjście
    Cena za usługe (price) : od 0 do 100, gdzie 100 to 50 zł

Przypadek testowy to duży samochód, klient z dużą ilością odwiedzeń i mała wielkość zabrudzenia
    car_size = 90
    visit_count = 10
    dirt_level = 1

Żeby uruchomić program trzeba zainstalować
pip install scikit-fuzzy
pip install matplotlib
pip install numpy