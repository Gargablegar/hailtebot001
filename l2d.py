# l2d.py
import numpy as np

a = np.matrix('1 2; 3 4')
print a[1,1]
print a
w = 10
h = 10
blockTypeMatrix = np.ones((w,h))

print blockTypeMatrix

np.savetxt('DERP.txt',  np.rint(blockTypeMatrix), delimiter=',')