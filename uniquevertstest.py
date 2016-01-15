#!/usr/local/bin/env python3

from random import randint

class vertex:
    __slots__ = ("x", "y", "z")

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "X:{0} Y:{1} Z:{2}".format(self.x, self.y, self.z)

    def __eq__(self, other):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.z != other.z:
            return False
        return True

    def __hash__(self):
        return hash((self.x, self.y, self.z))

a = []
for i in range(0,10000):
    a.append(vertex(randint(0,10),randint(0,10),randint(0,100)))

print(len(a))
for b in a:
    print(b)

print("set")
c = list(set(a))
print(len(c))
for b in c:
    print(b)
print("debug")

keys={s:i for i,s in enumerate(c)}
d=[keys[s] for s in a]
print("done making indices")
for i,b in enumerate(d):
    print("oldindex %s new index %s %s"%(i,b,c[b]))

print("input:%i"%(len(a)))
print("output:%i"%(len(c)))
