import argparse
import os
import laspy
import numpy as np
from progressbar import progressbar

np.set_printoptions(suppress=True)

MAT_LIST = [
    "Fence",
    "Ground",
    "Building",
    "Streetlight",
    "Trafficlight",
    "Car",
    "Tree"
]

def get_class_counts(folder):
    class_counts = np.zeros(shape=(len(MAT_LIST)+1))
    
    for file in progressbar(os.listdir(folder)):
        with laspy.open(os.path.join(folder, file)) as fh:
            las = fh.read()

            pointrecord = las.points

            classid = pointrecord['classification']

            hist, _ = np.histogram(classid, bins=len(MAT_LIST))

            hist = np.append(hist, len(classid))

            class_counts = class_counts + hist

    return class_counts

if __name__ == '__main__':
    argpaser = argparse.ArgumentParser(description='Plots point cloud class distribtion of all point cloud collections contained in the given folder')
    argpaser.add_argument('parent_folder')
    args = argpaser.parse_args()

    cc_dict = {}

    pc_folders = [os.path.join(args.parent_folder, f) for f in os.listdir(args.parent_folder) if os.path.isdir(os.path.join(args.parent_folder, f))]

    for folder in pc_folders:
        print(f'evalute folder {folder}')
        cc_dict[folder] = get_class_counts(folder)

    cumul_cc = np.zeros(shape=len(MAT_LIST)+1)

    for cc in cc_dict.values():
        cumul_cc = cumul_cc + cc

    cc_dict['total'] = cumul_cc

    print(cc_dict)