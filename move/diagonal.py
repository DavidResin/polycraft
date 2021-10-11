sliceHeight = 144
x0, y0, z0 = 1179, 43, -680
x1, y1, z1 = 1376, 73, -401
zMin, zMax = -625, -428
dx, dz = -3, -3


prefix = "summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:[ \
{id:armor_stand,Health:0,Passengers:[ \
{id:falling_block,Time:1,BlockState:{Name:activator_rail},Passengers:[ \
{id:command_block_minecart,Command:'gamerule commandBlockOutput false'}, \
{id:command_block_minecart,Command:'data merge block ~ ~-2 ~ {auto:0}'},"

template = "id:command_block_minecart,Command:'{0}'"

suffix = "{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:\"fill ~ ~ ~ ~ ~-2 ~ air\"}'}, \
{id:command_block_minecart,Command:'kill @e[type=command_block_minecart,distance=..1]'}]}]}]}"

cloner = "clone {0} {1} {2} {3} {4} {5} {6} {7} {8} replace {9}"
wiper = "fill {0} {1} {2} {3} {4} {5} air"

commands = ""

n = x1 - x0 + 1

for i in range(n):
	temp = cloner.format(x0 + i, y0, max(zMin, z0 + i), x0 + i, y1, min(zMax, z0 + sliceHeight + i), x0 + i + dx, y1 + 27, dz + max(zMin, z0 + i), "normal")
	#temp = wiper.format(x0 + i + dx, y1 + 27, dz + max(zMin, z0 + i), x0 + i + dx, 2 * y1 - y0 + 30, dz + min(zMax, z0 + sliceHeight + i))
	commands += "{" + template.format(temp) + "},"
	#commands += 

full = prefix + commands + suffix

print(full)