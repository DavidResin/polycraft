prefix = "summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:[ \
{id:armor_stand,Health:0,Passengers:[ \
{id:falling_block,Time:1,BlockState:{Name:activator_rail},Passengers:[ \
{id:command_block_minecart,Command:'gamerule commandBlockOutput false'}, \
{id:command_block_minecart,Command:'data merge block ~ ~-2 ~ {auto:0}'},"

template = "id:command_block_minecart,Command:'{0}'"

suffix = "{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:\"fill ~ ~ ~ ~ ~-2 ~ air\"}'}, \
{id:command_block_minecart,Command:'kill @e[type=command_block_minecart,distance=..1]'}]}]}]}"

cloner = "clone {0} 62 {1} {2} 112 {3} {4} 132 {5} replace"
cloner2 = "clone {0} 132 {1} {2} 182 {3} {4} 62 {5} replace"
eraser = "fill {0} 132 {1} {2} 172 {3} minecraft:air"

function = eraser

commands = ""

xG, zG = -24, 0

x0, z0 = -208, -288
x1, z1 = 31, 32

yHigh, yLow = 62, 80
y0, y1 = 62, 102

xChunks = [0, 21]
xShifts = [-1, 0]
xDict = dict(zip(xChunks, xShifts))
xS = 0

zChunks = [0, 2, 3, 5, 6]
zShifts = [0, 2, 2, 4, 5]

zDict = dict(zip(zChunks, zShifts))
zS = 0

doXShifts, doZShifts = False, False

if x0 > x1:
	temp = x0
	x0 = x1
	x1 = temp

if z0 > z1:
	temp = z0
	z0 = z1
	z1 = temp

x, z = x0, z0
xC, zC = 0, 0

while x < x1:
	if doXShifts:
		xS = xDict.get(xC, xS)

	while z < z1:
		if doZShifts:
			zS = zDict.get(zC, zS)

		commands += "{" + template.format(function.format(x, z, x + 15, z + 15, x - xS + xG, z - zS + zG)) + "},"
		z += 16
		zC += 1

	z = z0
	zC = 0
	x += 16
	xC += 1

full = prefix + commands + suffix
print(full)
print()
print(len(full))