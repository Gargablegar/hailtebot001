from hlt import *
from networking import *
from random import randint

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

for y in range(s):