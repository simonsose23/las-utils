import argparse
import os
import laspy
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import colormaps
from matplotlib.ticker import MaxNLocator
from progressbar import progressbar

font = {'size'   : 16}

plt.rc('font', **font)

PERFORMANCE = [.1, .2, .3, .4, .5, .6, .7]

MAT_LIST = [
    "Fence",
    "Ground",
    "Building",
    "Streetlight",
    "Trafficlight",
    "Car",
    "Tree"
]

def get_hist(filename):
    with laspy.open(filename) as fh:
        las = fh.read()

        pointrecord = las.points

        matid = pointrecord['classification']

        #matid = np.append(matid, range(0, len(MAT_LIST)))

        unique_mats = np.unique(matid)

        num_points = len(matid)

        hist, bin = np.histogram(matid, bins=[x-.5 for x in range(0, len(MAT_LIST) + 1)])

        return hist, num_points

if __name__ == '__main__':
    argpaser = argparse.ArgumentParser(description='Plots point cloud class distribtion of all point cloud collections contained in the given folder')
    argpaser.add_argument('parent_folder')
    args = argpaser.parse_args()

    pc_folders = [os.path.join(args.parent_folder, f) for f in os.listdir(args.parent_folder) if os.path.isdir(os.path.join(args.parent_folder, f))]

    avg_hists = []

    for folder in pc_folders:
        print(f'Processing {folder}...')
        lasfiles = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and os.path.splitext(f)[1] == '.las']

        overall_hist = np.zeros(shape=(len(MAT_LIST)))
        total_num_points = 0

        for f in progressbar(lasfiles):
            hist, num_points = get_hist(f)

            overall_hist = np.add(overall_hist, hist)
            total_num_points += num_points

        overall_hist = overall_hist / total_num_points

        avg_hists.append(overall_hist)

    num_plots = len(pc_folders)
    num_cols = 5
    colors = [ colormaps['Set2'](float(i)) for i in np.linspace(0, 1, num=len(MAT_LIST)) ]

    fig, axes = plt.subplots(math.ceil(num_plots/num_cols), num_cols, figsize=(5 * num_cols, 5 * math.ceil(num_plots/num_cols)), sharey=True)

    for i, _zip in enumerate(zip(axes.flat, pc_folders)):
        ax, folder = _zip

        if i % num_cols == 0:
            ax.set_ylabel("Class distribution")

        ax.bar(MAT_LIST, avg_hists[i], color=colors, edgecolor='black')
        ax.bar(MAT_LIST, PERFORMANCE, color='none', edgecolor='red')
        ax.set_title(os.path.split(folder)[1])
        ax.set_xticklabels(MAT_LIST, rotation=45, ha='right')
        ax.grid(axis='y')
        ax.set_yscale('log')
        ax.yaxis.set_tick_params(labelleft=True)
        ax.set_yticks([.001, .01, .1, .25, .5])
        ax.set_yticklabels([r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$2.5 \cdot 10^{-1}$',  r'$5 \cdot 10^{-1}$'])


    # remove unused axes
    for ax in axes.flat[num_plots:]:
        ax.remove()

    plt.tight_layout()
    plt.savefig('plot.pdf', format='pdf')
