import argparse
import os
import laspy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from progressbar import progressbar

# MAT_LIST = [
#     "Building/Foundation",
#     "Building/Roof",
#     "Building/Walls",
#     "Lot/Lot Surface",
#     "Street/Road Marking",
#     "Street/Road Surface",
#     "Street/Sidewalk",
#     "Street/Streetlight",
#     "Street/Traffic Light",
#     "Street/Vehicle",
#     "Vegetation/Tree-Branches",
#     "Vegetation/Tree-Leaves",
#     "Vegetation/Tree-Stem"
# ]

MAT_LIST = [
    "Building",
    "Soil",
    "Street/Streetlight",
    "Street/Traffic Light",
    "Street/Vehicle",
    "Vegetation/Tree-Branches",
    "Vegetation/Tree-Leaves",
    "Vegetation/Tree-Stem"
]

def get_hist(filename):
    with laspy.open(filename) as fh:
        las = fh.read()

        pointrecord = las.points

        matid = pointrecord['MaterialID']

        #matid = np.append(matid, range(0, len(MAT_LIST)))

        unique_mats = np.unique(matid)

        num_points = len(matid)

        hist, bin = np.histogram(matid, bins=[x-.5 for x in range(0, len(MAT_LIST) + 1)])

        return hist, num_points

if __name__ == '__main__':
    argpaser = argparse.ArgumentParser(description='Plots point cloud class distribtion of all point cloud collections contained in the given folder')
    argpaser.add_argument('parent_folder')
    args = argpaser.parse_args()

    pc_folders = [os.path.join(args.parent_folder, f) for f in os.listdir(args.parent_folder) if os.path.join(args.parent_folder, f)]

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

    fig, axes = plt.subplots(1, len(pc_folders), figsize=(len(pc_folders) * 5, 5), sharey=True)
    print(avg_hists)

    for i, folder in enumerate(pc_folders):
        axes[i].bar(MAT_LIST, avg_hists[i], color='blue')
        axes[i].set_title(os.path.split(folder)[1])
        axes[i].set_ylabel("Frequency")
        axes[i].set_xticklabels(MAT_LIST, rotation=45, ha='right')

    plt.tight_layout()
    plt.show()