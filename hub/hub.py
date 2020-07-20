import pyperclip

t = 5

prefix = "summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:[ \
{id:armor_stand,Health:0,Passengers:[ \
{id:falling_block,Time:1,BlockState:{Name:activator_rail},Passengers:[ \
{id:command_block_minecart,Command:'gamerule commandBlockOutput false'}, \
{id:command_block_minecart,Command:'data merge block ~ ~-2 ~ {auto:0}'},"

template = 'id:command_block_minecart,Command:"/setblock ~ ~{0} ~ minecraft:chain_command_block[facing=up]{{Command:\'{1}\',TrackOutput:0,auto:1}} replace"'

suffix = "{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:\"fill ~ ~ ~ ~ ~-2 ~ air\"}'}, \
{id:command_block_minecart,Command:'kill @e[type=command_block_minecart,distance=..1]'}]}]}]}"

commands = ""

for px, x, dx in [("-94995", "-94995", "0"), ("~-1", "-94993.5", "25"), ("-94969", "-94967", "0")]:
	for pz, z, dz in [("-40", "-40", "0"), ("~-1", "-38.5", "4"), ("-35", "-34", "4")]:
		for py, y, dy, st in [("~-1", "68.7", "16", "0"), ("~-1.6", "69.5", "15.3", "1..")]:
			commands += "{" + template.format(t, f"execute as @a[scores={{sneak_time={st}}},x={x},dx={dx},y={y},dy={dy},z={z},dz={dz}] at @s run clone -94953 76 8 -94951 76 10 {px} {py} {pz} masked normal") + "},"
			t += 1
full = prefix + commands + suffix
print(full)
print()
print(len(full))

pyperclip.copy(full)

