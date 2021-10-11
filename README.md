# Welcome to PolyCraft Tools

To gain access to the server, please head over to [our Discord](https://discord.gg/zYtZuue).

This repository is a collection of all the tools that were coded to help build PolyCraft, the EPFL and Unil campus recreation in Minecraft. Those tools are listed and described here. Please note that most of the code is not commented, but the descriptions provided here should give enough of a clue as to how they work.

## Chunks
As hundreds of players go all over the place and generate useless chunks that take up growing space with daily backups, this script was made to limit the growth of the map files by visualizing what chunk file was necessary or not.

## Heightmap
The terraform script was quickly coded and was complex to run. This is a work-in-progress bringing massive optimizations to the heightmap generation pipeline.

## Hole
A modification of the terraform script used to patch small holes in the landscape. Less efficient as it runs client-side, but good enough for average-sized surfaces.

## Hub
As the map was growing in size, we needed a way for non-OP players to consult the huge map on the hub wall without the ability to fly. This uses a system that constantly places a platform under the feet of the player, with the ability to raise or lower it by jumping or crouching respectively. A lot of edge cases need to be accounted for when the player goes to the edge of the room and this script allowed us to quickly tweak the system without writing tons of commands by hand.

## Layout
While working on the layout of the Unil campus, it quickly became clear that tracing out all those paths by hand was a needlessly long undertaking. This system, by far the most complex made for this project, allows us to place blocks on the map by simply clicking their corresponding location on the [Unil plan website](www.planete.unil.ch/plan). It comprises multiple components :
* The Javascript component, which is an extension of the position script, sends the coordinates to a local Python server for each click.
* The Python component, which receives the coordinates, buffers them and encapsulates them in a command which is sent to the hosting server via SSH every five seconds (sending one SSH message per command would make the spawning of the blocks very long, whereas this solution means the results are nearly instantaneous).  

The hosting server then processes the SSH message and writes the contained commands in the Minecraft server's CLI which spawns the blocks in the world.

## Pixel Art
The fill up functionality of our pixel art system requires multiple commands to clone a single block to a 128x128 area. This script creates an encapsulated command that does all the job, to be executed in-game on a command block.

## Position
To speed up the process of finding the position of real-world objects in the Minecraft world, this converter was created. The Python script does a simple conversion, while the JavaScript code files accomplish the same action but can be pasted in the console on the official map websites of [EPFL](www.map.epfl.ch) and [Unil](www.planete.unil.ch/plan) respectively and will print out Minecraft coordinates everytime the user clicks the map.

## Shift
Early on in the project, it was acknowledged that more precision in the building layouts was needed. It was therefore decided that we would need to shift most built chunks around relative to each other to make everything match proportions. The script creates a long command that moves plenty of chunks around based on a set of distances, to be executed in-game on a command block.

## Terraform
The campuses cover multiple square kilometers of land, which would be a dreadful task to carve by hand. Through legal means, we got our hands on official altimetric records of the region (not provided here for obvious reasons) and made a script that would convert those to usable block heights through linear interpolation and place blocks in the world. This allowed us to completely terraform the map (nearly 8 million blocks in surface) in a matter of hours. This must be run on a local server that is launched by Python as there are too many commands to execute for it to be done efficiently through command blocks.

## Toolbook
To facilitate the use of the different tools we coded for builders (preset teleporters, togglable player effects, ...), we wrote an in-game toolbook where players can trigger various actions by clicking text. The book is generated through a complex `give` command triggered in a command block.

## Translation
We want all info on the server to be available in French, English and German. We store all text here to simplify this task.

# Credits
Python and MC commands : myself  
JavaScript : Soraefir and myself  
Bash : Miomjon  
Prototyping : Fehross and myself
Translations : MeepMeep and myself

© 2020-2021 David Resin  
This project is freely available under a GNU GPLv3 license.
