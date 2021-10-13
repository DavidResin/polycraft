x0, y0, z0 = 94734, 99, -180
x, y, z = 94656, 83, -320
function = "clone {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}"
commands = ""

prefix = "summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:[ \
	{id:armor_stand,Health:0,Passengers:[ \
	{id:falling_block,Time:1,BlockState:{Name:activator_rail},Passengers:[ \
	{id:command_block_minecart,Command:'gamerule commandBlockOutput false'}, \
	{id:command_block_minecart,Command:'data merge block ~ ~-2 ~ {auto:0}'},"

template = "id:command_block_minecart,Command:'{0}'"
dummy = "{" + template.format("") + "},"

suffix = "{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:\"fill ~ ~ ~ ~ ~-2 ~ air\"}'}, \
	{id:command_block_minecart,Command:'kill @e[type=command_block_minecart,distance=..1]'}]}]}]}"

# clone up + shift
# shift
# clone down + shift

m = 64

for i in range(2 * m):
	commands += "{" + template.format(function.format(x+i, y, z, x+i, y, z+2*m-1, x+i, 1, z+i, "", "").strip()) + "},"	

#for i in range(2 * m):
#	commands += "{" + template.format(function.format(x, y, z+i, x+2*m-1, y, z+i, x+i, y+1, z+i, "replace", "normal")) + "},"	

#for i in range(2 * m - 1):
#	xs = x+4*m-2-i
#	zs = z+2*m-1
#	commands += "{" + template.format(function.format(x+i, y+1, z, x+i, y+1, z+i, x+i, y+1, zs-i, "replace", "move")) + "},"
#	commands += "{" + template.format(function.format(xs, y+1, zs, xs, y+1, zs-i, xs, y+1, z, "replace", "move")) + "},"

for i in range(2 * m - 1):
	zs = z+4*m-2-i
	xs = x+2*m-1
	commands += "{" + template.format(function.format(x, 1, z+i, x+i, 1, z+i, xs-i, 1, z+i, "replace", "move")) + "},"
	commands += "{" + template.format(function.format(xs, 1, zs, xs-i, 1, zs, x, 1, zs, "replace", "move")) + "},"

#for i in range(2 * m):
#	commands += "{" + template.format(function.format(x+2*m-1-i, y+1, z+i, x+4*m-2-i, y+1, z+i, x, y+2, z+i, "replace", "normal")) + "},"	

for i in range(2 * m):
	commands += "{" + template.format(function.format(x+i, 1, z+2*m-1-i, x+i, 1, z+4*m-2-i, x+i, y, z, "", "").strip()) + "},"	

commands += "{" + template.format("fill {0} 2 {2} {3} 2 {5} stone".format(x, y+1, z, x + 2*m-1, y+1, z + 2*m-1)) + "},"	

final = prefix + commands + suffix
final.replace("  ", "")
print(final)

print(len(prefix + commands + suffix))

print(template.format(function.format(x, 1, z+i, x+i, 1, z+i, xs-i, 1, z+i, "replace", "move")) + "},")