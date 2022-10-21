from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import lfilter
import pandas as pd

Z = []
true = []
selisihVal = []
errorrateVal = []
dataMerge = []

with open('dataLinearTrue.txt', 'r') as datafile:
    plotting = csv.reader(datafile, delimiter=',')
    for ROWS in plotting:
        selisih = float(ROWS[1]) - float(ROWS[0])
        errorRate = ((float(ROWS[0]) - float(ROWS[1]))/float(ROWS[1]))*100
        print("Jarak Sebenarnya: {},  Jarak Terukur: {},  Selisih Jarak: {},  Error Rate: {}".format(ROWS[1], ROWS[0], selisih, errorRate))
        Z.append(float(ROWS[0]))
        true.append(float(ROWS[1]))
        selisihVal.append(selisih)
        errorrateVal.append(errorRate)
        dataMerge.append([float(ROWS[1]), float(ROWS[0]), selisih, errorRate])

print(dataMerge)
df = pd.DataFrame(dataMerge, columns=['Jarak Sebenarnya', 'Jarak Terukur', 'Selisih', 'Error'])
print(df)