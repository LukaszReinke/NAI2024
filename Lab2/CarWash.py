"""
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


"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Define input variables with their universes of discourse
car_size = ctrl.Antecedent(np.arange(0, 101, 10), 'car_size')
visit_count = ctrl.Antecedent(np.arange(0, 11, 1), 'visit_count')
dirt_level = ctrl.Antecedent(np.arange(0, 11, 1), 'dirt_level')

# Define output variable
price = ctrl.Consequent(np.arange(0, 101, 1), 'price')

# Auto-generate membership functions for inputs (poor, average, good)
car_size.automf(3)
visit_count.automf(3)
dirt_level.automf(3)

# Define custom triangular membership functions for the output
price['low'] = fuzz.trimf(price.universe, [0, 0, 40])
price['medium'] = fuzz.trimf(price.universe, [0, 30, 60])
price['high'] = fuzz.trimf(price.universe, [50, 100, 100])

# Visualize membership functions
def plot_membership_functions():
    car_size['good'].view()
    visit_count['good'].view()
    dirt_level['poor'].view()
    price.view()

plot_membership_functions()

# Define fuzzy rules
rule1 = ctrl.Rule(
    (car_size['good'] & visit_count['average']) |
    (dirt_level['good'] & car_size['average']),
    price['high']
)

rule2 = ctrl.Rule(
    (car_size['good'] & visit_count['good'] & dirt_level['poor']) |
    (car_size['average'] & dirt_level['average']),
    price['medium']
)

rule3 = ctrl.Rule(
    (car_size['poor'] & visit_count['good']) |
    (car_size['average'] & dirt_level['poor'] & visit_count['average']),
    price['low']
)

# Create and simulate the control system
price_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
price_sim = ctrl.ControlSystemSimulation(price_ctrl)

# Input values
price_sim.input['car_size'] = 90
price_sim.input['visit_count'] = 10
price_sim.input['dirt_level'] = 1

# Perform computation
price_sim.compute()

# Print and visualize results
print(f"Calculated Price: {price_sim.output['price']:.2f}")
price.view(sim=price_sim)
plt.show()
