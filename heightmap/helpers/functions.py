import json
import numpy as np
import pyperclip as pc

from itertools import product
from scipy.ndimage.measurements import label

# Computes the affine coefficients of two 2D points
def getMH(x0_old, x0_new, x1_old, x1_new):
    m = (x0_new - x1_new) / (x0_old - x1_old)
    h = (x1_new * x0_old - x0_new * x1_old) / (x0_old - x1_old)
    
    return m, h

# Makes an affine matrix from a list of Ms and a list of Hs
def make_affine_matrix(ms, hs):
    if len(ms) != len(hs):
        raise ValueError("Ms and Hs must have the same length!")

    M = np.diag(ms)
    M = np.vstack([M, np.zeros(len(ms))])
    H = np.hstack([hs, 1])
    H = H.reshape((H.shape[0], 1))

    return np.hstack([M, H])

# Transforms a whole set of points with a given matrix
def convert_points(points, mat):
    points = np.c_[ points, points.shape[0]]
    return np.matmul(mat, points)

# Returns the altitude of a point defined by its latitude and longitude
def getV(rasters, lon, lat):
    r = find_raster(rasters, lon, lat)
    
    if r is None:
        return None
    
    return r.value_at_coords(lon, lat)

# Returns in-game X and Z coordinates of the top-left-most point of a map given by its XZ map indices
def mapTopLeft(mapX, mapZ):
    return mapX * 128 - 64, mapZ * 128 - 64

# Tells whether a longitude and a latitude fit within a given raster
def fits_bb(raster, lon, lat):
    bb = raster.bounds
    lonFit = bb.left <= lon <= bb.right
    latFit = bb.bottom <= lat <= bb.top
    return lonFit, latFit

# Finds a raster that matches a longitude and a latitude
def find_raster(rasters, lon, lat):
    for r in rasters:
        if sum(fits_bb(r, lon, lat)) == 2:
            return r
        
    return None

# Transforms a single point with a given matrix
def xzTrans(m2c, x, z):
    trans = np.matmul(m2c, [x, z, 1])
    return tuple(trans[:2])
    
# Takes two XZ points and returns the list of sub-areas with their corresponding raster
def raster_ranges(rasters, m2c, c2m, xS, zS, xE, zE):
    points = [(xS, zS)]
    ranges = []
    lonEnd, latEnd = xzTrans(m2c, xE, zE)
    
    while points:
        x0, z0 = points.pop()
        lon0, lat0 = xzTrans(m2c, x0, z0)
        
        raster = find_raster(rasters, lon0, lat0)
        
        if raster is None:
            raise ValueError("A raster is missing for longitude", lon, "and latitude", lat)
            
        lonFit, latFit = fits_bb(raster, lonEnd, latEnd)
        xB, zB = xzTrans(c2m, raster.bounds.right, raster.bounds.bottom)
        xB, zB = int(xB // 1), int(zB // 1)
        x1 = xE if lonFit else xB
        z1 = zE if latFit else zB
        
        ranges.append((raster, x0, z0, x1, z1))
        
        if not lonFit:
            points.append((xB + 1, z0))
            
        if not latFit and x0 == xS:
            points.append((x0, zB + 1))
            
    return ranges
            
# Generates a 128x128 Minecraft heightmap from a given top-left-most XZ point
def gen_heightmap(rasters, m2c, c2m, v2y, xS, zS):
    xE, zE = xS + 127, zS + 127
    ranges = raster_ranges(rasters, m2c, c2m, xS, zS, xE, zE)
    ret = np.zeros((128, 128))
    
    xFixes, zFixes = [], []
    
    for raster, x0, z0, x1, z1 in ranges:
        w = x1 - x0 + 1
        h = z1 - z0 + 1
        coords = np.array(list(product(range(w), range(h)))).T
        ones = np.ones((1, coords.shape[1]))
        matrix = np.r_[coords, ones]
        matrix[0] = matrix[0] + x0
        matrix[1] = matrix[1] + z0
        real_coords = np.matmul(m2c, matrix)[:2].T
        heights = raster.interp_points(pts=real_coords)
        
        sub_ret = np.zeros((w, h))
        sub_ret[tuple(coords)] = heights
        xShift, zShift = x0 - xS, z0 - zS
        ret[xShift:xShift + w, zShift:zShift + h] = sub_ret
        
        if x0 != xS:
            xFixes.append(x0)
            
        if z0 != zS:
            zFixes.append(z0)
            
    for fix in xFixes:
        x = fix - xS - 1
        ret[x, :] = (ret[x + 1, :] + ret[x - 1, :]) / 2
        
    for fix in zFixes:
        z = fix - zS - 1
        ret[:, z] = (ret[:, z + 1] + ret[:, z - 1]) / 2
        
    coords = np.array(list(product(range(128), range(128)))).T
    retF = np.array(ret.flatten())
    matrix = np.c_[retF.T, np.ones((retF.shape[0]))].T
    matrix = np.matmul(v2y, matrix)
    ret[tuple(coords)] = matrix[0]
    
    return np.around(ret).T.astype(int)

# Generates a fill command string
def gen_fill(strings, edges, Y, block0, mode=None, block1=None):
    h, w, X0, Z0 = edges
    X1 = X0 + h
    Z1 = Z0 + w
    
    if mode == "keep":
        pass
    elif mode == "replace":
        if block1 is None:
            raise ValueError
    elif mode is None:    
        mode = ""
    else:
        raise ValueError
        
    if block1 is None:
        block1 = ""
    else:
        if mode != "replace":
            raise ValueError
        
    cmd = strings["fill_command"].format(X0, Y, Z0, X1, Y, Z1, block0, mode, block1).strip()
    return strings["template"].format(cmd)
            
# Generates a clone command string
def gen_clone(strings, edges, Y0, yShift, mode, block=None):
    h, w, X0, Z0 = edges
    X1 = X0 + h
    Z1 = Z0 + w
    Y1 = Y0 + yShift
    
    if mode == "replace" or mode == "masked":
        pass
    elif mode == "filtered":
        if block is None:
            raise ValueError
    else:
        raise ValueError
        
    if block is None:
        block = ""
    else:
        if mode != "filtered":
            raise ValueError
        
    cmd = strings["clone_command"].format(X0, Y0, Z0, X1, Y0, Z1, X0, Y1, Z0, mode, block).strip()
    return strings["template"].format(cmd)

# Packages command for entry into a command block, yields several sets if too long
def package_commands(cmds, strings):
    max_chars = 32500
    prefix = strings["prefix"]
    suffix = strings["suffix"]
    
    def_len = len(prefix) + len(suffix)
    avail_space = max_chars - def_len
    lens = [len(cmd) + 1 for cmd in cmds]
    
    idx = 0
    batches = []
    
    while lens:
        idx = (np.cumsum(lens) <= avail_space).argmin(0)
        
        if idx == 0:
            idx = len(cmds)
            
        string = prefix + ",".join(cmds[:idx]) + suffix
        batches.append(string)
        lens = lens[idx:]
        cmds = cmds[idx:]
        
    for i, b in enumerate(batches):
        input("Press Enter to store the next command in your clipboard...")
        pc.copy(b)
        print(f"Batch {i + 1} of {len(batches)}")

# Turns a height array into a series of binary arrays for each layer
def thicken(arr):
    bottom = np.min(arr)
    top = np.max(arr)
    depth = top - bottom + 1
    ret = np.zeros(arr.shape + (depth,), dtype=bool)

    for d in range(depth):
        ret[..., d] = (arr == bottom + d)

    return ret, bottom, depth

# Splits a single layer into multiple sublayers of individual connected components
def split_layer(layer):
    structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    labeled, N = label(layer, structure)
    background_label = None if N == 1 else labeled[tuple(np.column_stack(np.where(layer == 0))[0])]
    ret = []
    
    for idx in range(1, N + 1):
        if background_label is None:
            idx = layer[0, 0]
        elif background_label == idx:
            continue
            
        component = (labeled == idx)
        j0, j1 = tuple(np.argwhere(np.any(component, axis=0))[[0, -1]].flatten().tolist())
        i0, i1 = tuple(np.argwhere(np.any(component, axis=1))[[0, -1]].flatten().tolist())
        
        ret.append((component[i0:i1 + 1, j0:j1 + 1], i0, j0))
        
    return ret

# Finds a near-optimal rectangular tiling of a layer
def tesselate_layer(sub_layer, i0, j0, xShift, zShift):
    # Trivial case
    if len(np.unique(sub_layer)) == 1:
        h0, w0 = sub_layer.shape
        return [(h0 - 1, w0 - 1, i0, j0)]
    
    # Initialize working arrays
    possible =   gen_tesseract(sub_layer)
    selected =   np.zeros(possible.shape)
    mask =       gen_mask(possible)
    coords_gen = gen_coords_generator(possible)

    # Iteratively select the best fills
    while select_next_fill(selected, possible, coords_gen, mask, sub_layer):
        pass

    # Generate scores
    scores = gen_scores_post(selected)

    # Remove redundant fills
    sanitize(selected, scores)

    # Shrink fills to their minimum useful size
    shrink(selected, scores)
    
    return [(h, w, i + i0 + xShift, j + j0 + zShift) for h, w, i, j in np.column_stack(selected.nonzero()).tolist()]

old = """        
# Splits a single layer into multiple sublayers of individual components
def split_layer_old(layer):
    structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    labeled, N = label(layer, structure)
    background_label = None if N == 1 else labeled[tuple(np.column_stack(np.where(layer == 0))[0])]
    ret = []
    
    for idx in range(1, N + 1):
        if background_label is None:
            idx = layer[0, 0]
        elif background_label == idx:
            continue
            
        component = (labeled == idx)
        j0, j1 = tuple(np.argwhere(np.any(component, axis=0))[[0, -1]].flatten().tolist())
        i0, i1 = tuple(np.argwhere(np.any(component, axis=1))[[0, -1]].flatten().tolist())
        
        ret.append((i1 - i0, j1 - j0, i0, j0))
        
    return ret
    
def tesselate_layer_old(layer, h0, w0, i0, j0, xShift, zShift):
    # Trivial case
    if len(np.unique(layer)) == 1:
        return [(h0, w0, i0, j0)]
    
    # Slice out the wanted part
    sub_layer = layer[i0:i0 + h0 + 1, j0:j0 + w0 + 1]
    
    # Initialize working arrays
    possible =   gen_tesseract(sub_layer)
    selected =   np.zeros(possible.shape)
    mask =       gen_mask(possible)
    coords_gen = gen_coords_generator(possible)

    # Iteratively select the best fills
    while select_next_fill(selected, possible, coords_gen, mask, sub_layer):
        pass

    # Generate scores
    scores = gen_scores_post(selected)

    # Remove redundant fills
    sanitize(selected, scores)

    # Shrink fills to their minimum useful size
    shrink(selected, scores)
    
    return [(h, w, i + i0 + xShift, j + j0 + zShift) for h, w, i, j in np.column_stack(selected.nonzero()).tolist()]
    
def cubify_old(arr, strings, shift=(0, 0)):
    multilayer, Y0, depth = thicken(arr.T)
    xShift, zShift = shift
    cmds = []
    
    for y in range(depth):
        layer = multilayer[..., y]
        sublayers = split_layer_old(layer)
        edges = []
        
        for (h, w, i, j) in sublayers:
            edges += tesselate_layer_old(layer, h, w, i, j, xShift, zShift)
            
        cmds += [gen_fill(strings, elem, Y0 + y, "diamond_block", mode="keep") for elem in edges]
    
    package_commands(cmds, strings)

# Turns a Minecraft heightmap into a set of individual commands yielded as batches
def cubify(arr, strings, shift=(0, 0)):
    multilayer, Y0, depth = thicken(arr.T)
    xShift, zShift = shift
    cmds = []
    
    for y in range(depth):
        layer = multilayer[..., y]
        sublayers = split_layer(layer)
        edges = []
        
        for (sub_layer, i, j) in sublayers:
            edges += tesselate_layer(sub_layer, i, j, xShift, zShift)
            
        cmds += [gen_fill(strings, elem, Y0 + y, "diamond_block", mode="keep") for elem in edges]
    
    package_commands(cmds, strings)
"""
    
# Turns a Minecraft heightmap into a set of individual commands yielded as batches
def cubify(arr, strings, shift=(0, 0)):
    multilayer, Y0, depth = thicken(arr.T)
    xShift, zShift = shift
    cmds = []
    
    for y in range(depth):
        layer = multilayer[..., y]
        sublayers = split_layer(layer)
        edges = []
        
        for (sub_layer, i, j) in sublayers:
            edges += tesselate_layer(sub_layer, i, j, xShift, zShift)
            
        cmds += [gen_fill(strings, elem, Y0 + y, "diamond_block", mode="keep") for elem in edges]
    
    package_commands(cmds, strings)
    
    return cmds, (Y0, Y0 + depth)
    
# Extracts the border of a binary component, array edges included
def gen_border(arr):
    h, w = arr.shape
    edge = np.ones((h, w), dtype=bool)
    edge[1:h-1,1:w-1] = 0
    
    dirs = [round(np.sin(i * np.pi / 2)) for i in range(4)]
    empties = arr == 0
    mem = empties.copy()
    
    for roll in zip(dirs, np.roll(dirs, -1)):
        mem += np.roll(empties, roll, axis=(0, 1))
        
    return (mem + edge) * (arr > 0)

# Generate mask of possible tesseract values
# More performant than gen_tesseract(np.ones(tsrct.shape[:2]))
def gen_mask(tsrct):
    h, w = tsrct.shape[:2]
    mask = np.ones(tsrct.shape, dtype=bool)

    for i in range(h):
        mask[i, :, h - i:h, :] = 0

    for j in range(w):
        mask[:, j, :, w - j:w] = 0

    return mask

# Subroutine for gen_tesseract
def gen_tesseract_sub(arr, true_if_and):
    h, w = arr.shape
    ret = np.zeros((h, w, h, w), dtype=bool)
    ret[0, 0] = arr > 0

    for i in range(1, h):
        curr = ret[i - 1, 0]
        roll = np.roll(curr, -1, axis=0)
        roll[-1] = False
        ret[i, 0] = curr & roll if true_if_and else curr | roll

    for j in range(1, w):
        curr = ret[:, j - 1]
        roll = np.roll(curr, -1, axis=2)
        roll[:, :, -1] = False
        ret[:, j] = curr & roll if true_if_and else curr | roll
        
    return ret

# Generates a tesseract for a given array, and ignores values that do not touch an edge if carve is set to True
def gen_tesseract(arr, carve=True):
    ret = gen_tesseract_sub(arr, True)
    
    if carve:
        border = gen_border(arr)
        no_fillers = gen_tesseract_sub(border, False)
        ret = ret & no_fillers
        
    return ret

# Alters a tesseract at a given coordinate and updates the score array
def modify_fill_at(tsrct, scores, h, w, i, j, true_if_add):
    tsrct[h, w, i, j] = true_if_add
    scores[i:i + h + 1, j:j + w + 1] -= -1 if true_if_add else 1

# Removes a fill
def remove_fill_at(tsrct, scores, h, w, i, j):
    modify_fill_at(tsrct, scores, h, w, i, j, False)
    
# Adds a fill
def add_fill_at(tsrct, scores, h, w, i, j):
    modify_fill_at(tsrct, scores, h, w, i, j, True)
    
# Iterates the given generator until a value is given that is still valid
def yield_coords(possible, gen):
    try:
        while True:
            h, w, i, j = next(gen)
            
            if possible[h, w, i, j]:
                return h, w, i, j
    except StopIteration:
        return None

# Makes a generator of valid values out of a tesseract
def gen_coords_generator(possible):
    h, w = possible.shape[:2]
    order = sorted(np.column_stack(possible.nonzero()), key=lambda elem: (-max(elem[:2]), -elem[0], -elem[1]))
    
    for h0, w0, i0, j0 in order:
        yield h0, w0, i0, j0
    
# Selects the next valid fill
def select_next_fill(selected, possible, gen, mask, arr):
    H, W = arr.shape
    coords = yield_coords(possible, gen)
    
    if coords is None:
        return False
    
    h, w, i, j = coords
    selected[h, w, i, j] = True
    
    slc = np.index_exp[:h + 1, :w + 1, i:i + h + 1, j:j + w + 1:]
    sub_possible = possible[slc]
    sub_mask = mask[H - h - 1:, W - w - 1:, :h + 1, :w + 1]
    possible[slc] = sub_possible & (1 - (sub_mask & sub_possible))
    
    return True
    
# Creates a score array
def gen_scores_post(selected):
    ret = np.zeros(selected.shape[:2], dtype=np.int16)
    
    for h, w, i, j in np.column_stack(selected.nonzero()).tolist():
        slc = np.index_exp[i:i + h + 1, j:j + w + 1]
        ret[slc] = ret[slc] + 1
        
    return ret

# Removes strictly redundant fills
def sanitize(selected, scores):
    for h, w, i, j in sorted(np.column_stack(selected.nonzero()), key=lambda t: (-np.prod(t[:2]), -t[0])):
        if np.all(scores[i:i + h + 1, j:j + w + 1] > 1):
            remove_fill_at(selected, scores, h, w, i, j)
        
# Shrinks all fills to their absolute minimal size
def shrink(selected, scores):
    for h, w, i, j in sorted(np.column_stack(selected.nonzero()), key=lambda t: (-np.prod(t[:2]), -t[0])):
        vals = scores[i:i + h + 1, j:j + w + 1] == 1
        aggrI = np.where(np.any(vals, axis=1))[0]
        aggrJ = np.where(np.any(vals, axis=0))[0]

        if len(aggrI) + len(aggrJ) > 0:
            iMin, iMax = aggrI[0], aggrI[-1]
            jMin, jMax = aggrJ[0], aggrJ[-1]
            newH = iMax - iMin
            newW = jMax - jMin

            if newH < h or newW < w:
                remove_fill_at(selected, scores, h, w, i, j)
                add_fill_at(selected, scores, newH, newW, i + iMin, j + jMin)

old = """
# Yields commands for a given map coordinate
def yield_map(rasters, strings, m2c, c2m, v2y, xMap, zMap):
    xS, zS = mapTopLeft(xMap, zMap)
    arr = gen_heightmap(rasters, m2c, c2m, v2y, xS, zS)
    cubify(arr, strings, shift=(xS, zS))
"""
    
# Yields commands for a given map coordinate
def yield_map(rasters, strings, m2c, c2m, v2y, xMap, zMap):
    xS, zS = mapTopLeft(xMap, zMap)
    arr = gen_heightmap(rasters, m2c, c2m, v2y, xS, zS)
<<<<<<< HEAD
    cmds, Y = cubify(arr, strings, shift=(xS, zS))
    save_range((xMap, zMap), cmds, Y)
=======
    cubify(arr, strings, shift=(xS, zS))
>>>>>>> 9c21258383524f52cdab824da287edc843ad4146
