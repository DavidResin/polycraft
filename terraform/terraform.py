import numpy as np
import pickle as pkl
from subprocess import Popen, PIPE, STDOUT
import time

with open("hMapMc.pkl", "rb") as f:
	arr = pkl.load(f)

cmd = Popen('start.bat', stdin=PIPE)

template = "fill {0} {1} {2} {0} {1} {2} gold_block\n"
template2 = "fill {0} {1} {2} {0} {1} {2} gold_block replace {3}\n"

xMin, xMax, zMin, zMax = -1527, 1938, -1243, 1082
width = xMax - xMin
height = zMax - zMin

size = 256
xLim = width // size
zLim = height // size

print("X: ", [xMin + (i + .5) * size for i in range(xLim)])
print("Z: ", [zMin + (i + .5) * size for i in range(zLim)])

print(xLim, zLim)

def fill(x, z):
	for i in range(size):
		for j in range(size):
			tempX = min(xMax - xMin, i + x * size)
			tempZ = min(zMax - zMin, j + z * size)
			#cmd.stdin.write(("fill " + str(tempX + xMin) + " " + str(min(0, arr[tempZ, tempX])) + " " + str(tempZ + zMin) + str(tempX + xMin) + " " + str(min(0, arr[tempZ, tempX])) + " " + str(tempZ + zMin) + " diamond_block\n").encode())
			cmd.stdin.write((template.format(str(tempX + xMin), str(max(0, arr[tempZ, tempX])),str(tempZ + zMin))).encode())
	print(x * size, z * size)

def fill_safe(x, z):
	for i in range(size):
		for j in range(size):
			tempX = min(xMax - xMin, i + x * size)
			tempZ = min(zMax - zMin, j + z * size)
			y = arr[tempZ, tempX]
			#cmd.stdin.write(("fill " + str(tempX + xMin) + " " + str(min(0, arr[tempZ, tempX])) + " " + str(tempZ + zMin) + str(tempX + xMin) + " " + str(min(0, arr[tempZ, tempX])) + " " + str(tempZ + zMin) + " diamond_block\n").encode())
			if y > 61:
				cmd.stdin.write((template2.format(str(tempX + xMin), str(max(0, y)),str(tempZ + zMin), "air")).encode())
			else:
				cmd.stdin.write((template.format(str(tempX + xMin), str(max(0, y)),str(tempZ + zMin))).encode())

	print(x * size, z * size)

def test():
	for i in range(64):
		for j in range(64):
			cmd.stdin.write(("execute at MCRaisin run fill ~" + str(-32 + i) + " " + str(arr[j, i]) + " ~" + str(-32 + j) + " ~" + str(-32 + i) + " " + str(arr[j, i]) + " ~" + str(-32 + j) + " gold_block\n").encode())
