import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import csv

with open('test_13_06_2024.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    
    for row in csv_reader:
        print(row)

#milion przystanków c załej warszawy guzik da
#trzeba manualnie sprawdzać, czy przystanek 02
#jest w stronę centrum, czy nie, bo inaczej jest wielki burdel
#trzeba sprawdzić które przystanki są w którą stronę
#może dwa pliki dla każdej linii
#nie wiem jak inaczej...