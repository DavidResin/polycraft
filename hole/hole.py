import numpy as np
import pickle as pkl
import os, sys

if len(sys.argv) < 5:
	sys.exit(0)

x0, z0, x1, z1 = tuple(map(int, sys.argv[1:]))

if x0 > x1:
	x0, x1 = x1, x0

if z0 > z1:
	z0, z1 = z1, z0

with open("hMapMc.pkl", "rb") as f:
	arr = pkl.load(f)

template = "/usr/bin/screen -p 0 -S mc-server -X eval 'stuff \"'\"'\"fill {0} {1} {2} {0} {1} {2} diamond_block keep\"'\"'\"\\015'; "
prefix = "ssh mc-server@owo.miomjon.ch \""
cmd = prefix

xMin, xMax, zMin, zMax = -1527, 1938, -1243, 1082

limit = 1000
counter = limit

for x in range(x0, x1 + 1):
	for z in range(z0, z1 + 1):
		y = arr[z - zMin, x - xMin]
		cmd += template.format(x, y, z)
		counter -= 1

		if counter == 0:
			os.system(cmd[:-2] + "\"")
			cmd = prefix
			counter = limit

if cmd != prefix:
	os.system(cmd[:-2] + "\"")