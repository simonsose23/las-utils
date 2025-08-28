import laspy
import numpy as np
import matplotlib.pyplot as plt

def get_hist(filename):
    with laspy.open(filename) as fh:
        las = fh.read()

        pointrecord = las.points

        matid = pointrecord['MaterialID']

        num_mats = np.unique(matid)

        num_points = len(matid)

        hist, bin = np.histogram(matid, bins=num_mats)

        return hist / num_points




hists = []

for i in range(0, 47):
    hist = get_hist(f'/mnt/SUPERCOOL/pointclouds/pwest/pc-{i}.las')
    plt.plot(hist)

    hists.append(hist)


plt.show()