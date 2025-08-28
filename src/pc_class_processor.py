import os
import hydra
from omegaconf import DictConfig, OmegaConf
import laspy
import numpy as np
from progressbar import progressbar

SUPPORTED_TYPES = ('.las', '.laz')

'''
Cluster classes of given point cloud according to given cluster scheme.

For every key x, there is an array Y. For every element y captured by the clusters array Y, all the classes y in Y will be
renamed to x.

if rename is set, the scalar_field is renamed to rename.
'''
def cluster_classes(las, cluster_dict, scalar_field, *, rename, default_class):
    # TODO: Adapt readme
    pr = las.points

    # create overall_mask to track points that have not been touched in the end
    overall_mask = np.full(len(pr), np.bool(False))

    for key, cluster_expr in cluster_dict.items():
        # expand cluster expressions to literal cluster
        lit_cluster = []

        for ce in cluster_expr:
            if 'x' in str(ce):
                lit_cluster += [np.int32(x) for x in range(int(ce.replace('x', '0')), int(ce.replace('x', '9')) + 1)]
            else:
                lit_cluster.append(np.int32(ce))

        # create mask marking all the entries captured by the cluster
        mask = np.isin(pr[scalar_field], np.array(lit_cluster))

        # refine mask to avoid cascading
        mask = np.logical_and(mask, np.logical_not(overall_mask))

        overall_mask = np.logical_or(overall_mask, mask)

        pr[scalar_field][mask] = np.int8(key)

    if default_class:
        pr[scalar_field][np.logical_not(overall_mask)] = np.int8(default_class)

    if rename:
        pr[rename] = pr[scalar_field]
        las.remove_extra_dim(scalar_field)
            
    if np.bool(False) in overall_mask and not default_class:
        print("Warning: Some values have not been remapped")

@hydra.main(version_base=None, config_path='configs/processor')
def main(cfg: DictConfig) -> None:
    # 0. Collect all las files to process
    src_las_files = []
    tgt_las_files = []

    # get all las files
    for path, subdirs, files in os.walk(cfg['input_dir']):
        for fname in files:
            if fname.endswith(SUPPORTED_TYPES):
                full_name = os.path.join(path, fname)
                tgt_dir = path.replace(cfg['input_dir'], cfg['output_dir'], 1)

                if not os.path.exists(tgt_dir):
                    os.makedirs(tgt_dir, exist_ok=True)

                basepath, filetype = full_name.split('.')

                src_las_files.append(full_name)
                tgt_las_files.append(f'{basepath}-processed.{filetype}'.replace(cfg['input_dir'], cfg['output_dir'], 1))

    print("Clustering...")
    
    # 1. Cluster
    for tgt, src in progressbar(zip(tgt_las_files, src_las_files)):
        with laspy.open(src) as fh:
            las = fh.read()
            
            if 'cluster' in cfg:
                cluster_classes(las, cfg['cluster'], cfg['scalar_field'], rename=cfg['rename'], default_class=cfg['default_class'])

            las.write(tgt)

if __name__ == '__main__':
    main()