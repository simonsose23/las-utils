import os
import hydra
from omegaconf import DictConfig, OmegaConf
import argparse
import laspy
import numpy as np
from progressbar import progressbar

SUPPORTED_TYPES = ('.las', '.laz')

def merge_scalar(filepath, target_file_path, merge_scalar, values_to_merge, onto_scalar, write_offset, *, onto_values):
    with laspy.open(filepath) as fh:
        las = fh.read()
        pr = las.points

        # create mask of all points that are labeled with a value to merge
        points_to_write = np.isin(pr[merge_scalar], values_to_merge)


        if onto_values:
            # create mask of all points that we may write to (onto_values)
            masked_points = np.isin(pr[onto_scalar], onto_values)

            # create final mask
            mask = np.logical_and(points_to_write, masked_points)
        else:
            mask = points_to_write

        # offset all merge_scalar values by maximum onto_scalar value + 1 to not write into onto_scalar range
        pr[merge_scalar] += write_offset

        pr[onto_scalar][mask] = pr[merge_scalar][mask]

        las.write(target_file_path)


@hydra.main(version_base=None, config_path='configs/merger')
def main(cfg: DictConfig) -> None:
    pc_paths = []
    
    for path, _, files in os.walk(cfg['pc_folder']):
        for fname in files:
            if fname.endswith(SUPPORTED_TYPES):
                full_name = os.path.join(path, fname)
                pc_paths.append(full_name)

    for pc_path in progressbar(pc_paths):
        basepath, filetype = pc_path.split('.')

        merge_scalar(pc_path, f'{basepath}-merged.{filetype}', cfg['from_scalar'], cfg['merge_values'], cfg['onto_scalar'], int(cfg['write_offset']), onto_values=cfg['onto_values'])

if __name__ == '__main__':
    main()