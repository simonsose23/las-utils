import laspy
import numpy as np


for i in range(0, 47):
    filename = f'/mnt/SUPERCOOL/pointclouds/pwest/pc-{i}.las'
    with laspy.open(filename) as fh:
        las = fh.read()

        pointrecord = las.points

        matid = pointrecord['MaterialID']

        hist, bin_edge = np.histogram(matid, bins=16)

        mask = hist == 0

        empty_classes = np.where(mask)[0]

        print(f'empty classes in {filename}: \t {empty_classes.tolist()}')