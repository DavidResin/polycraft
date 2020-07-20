import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import os

data = np.random.rand(10, 10) * 20

reg = [tuple(map(int,fn.split(".")[1:3])) for fn in os.listdir("hm_test/region")]
arrs = list(zip(*reg))

x0, x1 = min(arrs[0]), max(arrs[0])
z0, z1 = min(arrs[1]), max(arrs[1])

x = np.zeros((x1 - x0 + 1, z1 - z0 + 1))

for r, s in reg:
	x[r - x0, s - z0] = 15

# create discrete colormap
cmap = colors.ListedColormap(['red', 'blue'])
bounds = [0,10,20]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
ax.imshow(x, cmap=cmap, norm=norm)

# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(x0, x1, 200));
ax.set_yticks(np.arange(z0, z1, 200));

plt.show()