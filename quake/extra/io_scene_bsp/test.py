import api
import quake

b = api.Bsp.open(r'C:\Users\Joshua\Games\QUAKE\Id1\maps\test.bsp')
#b = quake.bsp.Bsp.open(r'C:\Users\Joshua\Games\QUAKE\Id1\maps\test.bsp')
v = b.ffaces[0].vertexes
print(b)
