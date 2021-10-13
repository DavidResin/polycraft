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

for i in range(128):
	commands += "{" + template.format(function.format(x+i, y, z, x+i, y, z+127, x+127-i, y+1, z, "replace", "normal")) + "},"

commands += "{" + template.format(function.format(x, y+1, z, x+127, y+1, z+127, x, y, z, "replace", "move")) + "},"

print(prefix + commands + suffix)