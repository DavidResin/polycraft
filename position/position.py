import sys

z = -135.5
x = -79.5
fac = 1

longitude = 3470
latitude = 2562.5

m = 1
h = 0

if len(sys.argv) < 3:
	sys.exit(0)

if sys.argv[1] == "x":
	v = -x
	pos = longitude
	fac = -1
elif sys.argv[1] == "z":
	v = z
	pos = latitude
	m = 1.029661
	h = 4.741
else:
	sys.exit(0)

arg = float(sys.argv[2])

res = m * (v + 1.34903905766 * (pos - arg)) + h



print(sys.argv[1], "=", "%.02f" % (fac * res))