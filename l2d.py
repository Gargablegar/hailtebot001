# l2d.py
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

# a = np.matrix('1 2; 3 4')
# print a[1,1]
# print a
# w = 10
# h = 10
# blockTypeMatrix = np.zeros((w,h))

# print blockTypeMatrix

# Read in saved Numpy data from game
ff = open('TEMPNP')
array = np.loadtxt(ff,delimiter=',')
ff.close()

print array.max()
plt.imshow(array, cmap='hot', interpolation='nearest')
plt.show()