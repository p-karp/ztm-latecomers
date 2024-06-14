import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import csv

with open('test_13_06_2024.csv', 'r') as file:
    csv_reader = csv.reader(file)
    
    for row in csv_reader:
        print(row)