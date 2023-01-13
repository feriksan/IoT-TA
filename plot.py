from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import lfilter


# fig = plt.figure()
# ax = plt.axes(projection='3d')

X = []
Y = []
Z = []
true = []
avr = []
avrDiameter = []
avrValue = 0
diameterValue = 0
val = 10

with open('dataWithDiameter.txt', 'r') as datafile:
    plotting = csv.reader(datafile, delimiter=',')
    for ROWS in plotting:
        # if(float(ROWS[4]) == val):
        #     avr.append(float(ROWS[0]))
        #     avrDiameter.append(float(ROWS[1]))
        X.append(float(ROWS[0]))
        Y.append(float(ROWS[4]))
        print(float(ROWS[0]))
        true.append(float(ROWS[4]))
        Z.append(float(ROWS[0]))

# Data for a three-dimensional line
avrValue = np.average(avr)
diameterValue = np.average(avrDiameter)
# print(round(D, 5))
# print(round(avrValue, 5))
# print(round(diameterValue, 2))
# print("{},{}".format(avrValue, val))
zline = Z
plt.figure(figsize=(10,10))
plt.scatter(true, zline, c='crimson')
plt.yscale('log')
plt.xscale('log')

p1 = max(max(zline), max(true))
p2 = min(min(zline), min(true))
plt.plot([p1, p2], [p1, p2], 'b-')
plt.xlabel('True Values', fontsize=15)
plt.ylabel('Predictions', fontsize=15)
plt.axis('equal')
plt.show()

xline = X
yline = Y
fig, ax = plt.subplots()

ax.plot(zline, true, linewidth=2.0)

plt.plot(zline)
plt.xlabel('Jarak Sebenarnya')
plt.ylabel('Jarak Terdeteksi')
ax.set_xlim3d(-1, 1)
ax.set_ylim3d(-1, 1)
ax.set_zlim3d(-1, 1)
ax.plot3D(zline, zline, zline, 'gray')

# Data for three-dimensional scattered points
zdata = 15 * np.random.random(100)
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
plt.show()