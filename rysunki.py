import matplotlib.pyplot as plt

dictionary = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    
# Przygotowanie danych do wykresu
keys = list(dictionary.keys())
values = list(dictionary.values())
    
    # Tworzenie wykresu
plt.figure(figsize=(8, 5))
plt.bar(keys, values, color='skyblue')
plt.xlabel('Klucze')
plt.ylabel('Wartości')
plt.title('Wykres wartości w słowniku')
plt.grid(True)
plt.show()
