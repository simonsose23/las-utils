import argparse
import os
import laspy
import numpy as np
import matplotlib.pyplot as plt

font = {'size'   : 16}

plt.rc('font', **font)

MAT_LIST = [
    "Fence",
    "Ground",
    "Building",
    "Streetlight",
    "Trafficlight",
    "Car",
    "Tree"
]

def draw_confmat(filename, orig_scalar, pred_scalar, fig, ax, title, colorbar=False):
    DATA = np.empty(shape=(len(MAT_LIST)))

    with laspy.open(filename) as fh:
        las = fh.read()

        pr = las.points

        for i, _ in enumerate(MAT_LIST):
            mat_pr = pr[pr[orig_scalar] == i]
            hist, _ = np.histogram(mat_pr[pred_scalar], bins=[x-0.5 for x in range(0, 8, 1)], density=True)
            #print(hist)
            DATA = np.vstack([DATA, hist])

    DATA = np.delete(DATA, 0, axis=0)

    img = ax.imshow(DATA)

    ax.set_xticks(np.arange(7))
    ax.set_xticklabels(MAT_LIST, rotation=45, ha='right')
    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(MAT_LIST)
    ax.set_title(title, fontsize=16)

    if colorbar:
        fig.colorbar(img)

if __name__ == '__main__':
    argpaser = argparse.ArgumentParser(description='Plots point cloud class distribtion of all point cloud collections contained in the given folder')
    argpaser.add_argument('folder')
    argpaser.add_argument('orig_scalar')
    argpaser.add_argument('predicted_scalar')
    args = argpaser.parse_args()

    filenames = [os.path.join(root, name)
             for root, dirs, files in os.walk(args.folder)
             for name in files
             if name.endswith(".laz")]

    filenames = sorted(filenames)

    fig, ax = plt.subplots(figsize=(20, 5), nrows=1, ncols=4)

    titles = ['Real-world only', 'Hybrid', 'Adatrainset-rmse', 'Adatrainset-rand']

    for fname, a, t in zip(filenames, ax.flat, titles):
        draw_confmat(fname, args.orig_scalar, args.predicted_scalar, fig, a, t)
        print(fname)

    plt.tight_layout()
    plt.savefig('plot.pdf', format='pdf')