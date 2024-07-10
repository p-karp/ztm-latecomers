# ztm-latecomers
## Authors: Patryk Karp, Mateusz Roman, Hanna Moczek, Karolina Winczewska

An application that collects data from "warsaw-data-api 0.5.3" and analyzes delays of Warsaw Buses. 

## Data Collection Instructions

To begin collecting data, follow these steps:
1. Open your terminal.

2. Type the following command, replacing python3 with the appropriate Python interpreter installed on your workstation:
> python3 run.py

3. Press Enter to execute the command. (Make sure you have the necessary Python environment set up and that the run.py file exists in the specified location.)

4. Data downloading will start at 2:55 by downloading the timetables of the selected stops, this data will be saved in a file with the path "./zebranieDane/originalne" with the file prefix "rj_" and the download start date. At 3:00 the actual part of collecting live data will begin, which will be placed in a directory with the same path, but this time with the file prefix "data_" and the download start date. It will end at 1 a.m. the next day. While collecting data, you will be able to see various control information on the terminal, so you can constantly monitor the correctness of the data collection process.