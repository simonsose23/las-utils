import os
import hydra
from omegaconf import DictConfig, OmegaConf
import argparse
import laspy
import numpy as np
from progressbar import progressbar

SUPPORTED_TYPES = ('.las', '.laz')

def merge_scalar(filepath, target_file_path, merge_scalar, values, onto_scalar):
    with laspy.open(filepath) as fh:
        las = fh.read()
        pr = las.points

        onto_scalar_max = np.max(pr[onto_scalar])

        points_to_write = np.isin(pr[merge_scalar], values)

        pr[merge_scalar] += onto_scalar_max + 1

        pr[onto_scalar][points_to_write] = pr[merge_scalar][points_to_write]

        las.write(target_file_path)


@hydra.main(version_base=None, config_path='.', config_name='pc_scalar_merger_conf')
def main(cfg: DictConfig) -> None:
    pc_paths = []

    for path, _, files in os.walk(cfg['pc_folder']):
        for fname in files:
            if fname.endswith(SUPPORTED_TYPES):
                full_name = os.path.join(path, fname)
                pc_paths.append(full_name)

    for pc_path in progressbar(pc_paths):
        basepath, filetype = pc_path.split('.')

        merge_scalar(pc_path, f'{basepath}-merged.{filetype}', cfg['from_scalar'], cfg['merge_values'], cfg['onto_scalar'])

if __name__ == '__main__':
    main()