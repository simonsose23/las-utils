import argparse
import os
import laspy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from progressbar import progressbar

def get_hist(filename):
    with laspy.open(filename) as fh:
        las = fh.read()

        pointrecord = las.points

        matid = pointrecord['MaterialID']

        matid = np.append(matid, [0, 1, 2, 3, 4, 5, 6, 7, 8])

        unique_mats = np.unique(matid)

        num_points = len(matid)

        hist, bin = np.histogram(matid, bins=len(unique_mats))

        hist_norm = hist / num_points

        return hist_norm

if __name__ == '__main__':
    argpaser = argparse.ArgumentParser(description='Plots point cloud class distribtion')
    argpaser.add_argument('folder')
    args = argpaser.parse_args()

    lasfiles = [os.path.join(args.folder, f) for f in os.listdir(args.folder) if os.path.isfile(os.path.join(args.folder, f)) and os.path.splitext(f)[1] == '.las']

    hists = []

    for f in progressbar(lasfiles):
        hist = get_hist(f)

        hists.append(hist)

    img = plt.imshow(hists)
    plt.colorbar()

    plt.show()