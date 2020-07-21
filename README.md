# Welcome to Polycraft Tools

To gain access to the server, please head over to [our Discord](https://discord.gg/zYtZuue).

This repository is a collection of all the tools that were coded to help build the EPFL and Unil campus recreation in Minecraft. Those tools are listed and described here. Please note that most of the code is not commented, but the descriptions provided here should give enough of a clue as to how they work.

## Chunks
As hundreds of players go all over the place and generate useless chunks that take up growing space with daily backups, this script was made to limit the growth of the map files by visualizing what chunk file was necessary or not.

## Hub
As the map was growing in size, we needed a way for non-OP players to consult the huge map on the hub wall without the ability to fly. This uses a system that constantly places a platform under the feet of the player, with the ability to raise or lower it by jumping or crouching respectively. A lot of edge cases need to be accounted for when the player goes to the edge of the room and this script allowed us to quickly tweak the system without writing tons of commands by hand.

## Layout
While working on the layout of the Unil campus, it quickly became clear that tracing out all those paths by hand was a needlessly long undertaking. This system, by far the most complex made for this project, allows us to place blocks on the map simply by clicking their corresponding location on the [Unil plan website](www.planete.unil.ch/plan). It comprises multiple components :
* The Javascript component, which is an extension of the position script, sends the coordinates to a local Python server for each click.
* The Python component, which receives the coordinates, encapsulates them in a command which is sent to the server via SSH.  

The server then processes the SSH message and writes the command in the Minecraft server's CLI which spawns a block in the world.

## Pixel Art
The fill up functionality of our pixel art system requires multiple commands to clone a single block to a 128x128 area. This script creates an encapsulated command that does all the job, to be executed in-game on a command block.

## Position
To speed up the process of finding the position of real-world objects in the Minecraft world, this converter was created. The Python script does a simple conversion, while the JavaScript code files can be pasted in the console on the official map websites of [EPFL](www.map.epfl.ch) and [Unil](www.planete.unil.ch/plan) respectively and will print out Minecraft coordinates everytime the user clicks the map.  
  
Credit goes to Soraefir for the JavaScript work.

## Shift
Early on in the project, it was acknowledged that more precision in the building layouts was needed. It was therefore decided that we would need to shift most built chunks around relative to each other to make everything match proportions. The script creates a long command that moves plenty of chunks around, to be executed in-game on a command block.

## Terraform
The campuses cover multiple square kilometers of land, which would be a dreadful task to shape by hand. Through legal means, we got our hands on official altimetric records of the region (not provided here for obvious reasons) and made a script that would convert those to usable block heights through linear interpolation and place blocks in the world. This allowed us to completely terraform the map (nearly 8 million blocks in surface) in a matter of hours. This must be run on a local server that is launched by Python as there are too many commands to execute for it to be done efficiently through command blocks.

© 2020 David Resin  
This project is freely available under a GNU GPLv3 license.
