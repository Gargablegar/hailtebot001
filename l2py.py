from hlt import *
from networking import *
from random import randint


print ('A' if random.random() > 0.5 else 'S')
print ('A' if random.random() > 0.5 else 'S')
print ('A' if random.random() > 0.5 else 'S')
print ('A' if random.random() > 0.5 else 'S')

print ('STILL' if random.random() > 0.25 else randint(1,4))
print ('STILL' if random.random() > 0.25 else randint(1,4))
print ('STILL' if random.random() > 0.25 else randint(1,4))
print ('STILL' if random.random() > 0.25 else randint(1,4))


print '===================='
print CARDINALS[1]
print random.random()
x = 1
y = 2
location = Location(x, y)

print location.x
location.x = location.x + 5
print location.x

for a in range(1, 5):
	print a
W = 10
H = 10
productionField = [[0 for x in range(W)] for y in range(H)]

print productionField

