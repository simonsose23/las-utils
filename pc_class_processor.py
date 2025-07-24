import os
import hydra
from omegaconf import DictConfig, OmegaConf
import laspy
import numpy as np
from progressbar import progressbar

'''
Cluster classes of given point cloud according to given cluster scheme.

For every element x in the clusters array, all the classes y in x will be
renamed to x.
'''
def cluster_classes(pr, clusters):
    for cluster in clusters:
        new_id = np.min(cluster)

        mask = np.isin(pr['MaterialID'], cluster)

        pr['MaterialID'][mask] = [new_id]


'''
We determine all classes that are contained in the point clouds in the named folder.
'''
def get_existing_classes(pr) -> set:
    return set([ int(x) for x in np.unique(pr['MaterialID']) ])
    

'''
Compress classes of given point cloud in LAS format.

We rearrange the class ids so that there are no gaps in the numbering.
'''
def rearrange_classes(pr, classes_to_keep):
    classes_to_keep.sort()

    # create class mapping 
    class_mapping = dict()

    for i, key in enumerate(classes_to_keep):
        class_mapping[key] = i

    print(class_mapping)

    # apply class mapping to point record
    pr['MaterialID'] = [ class_mapping[int(old_class)] for old_class in pr['MaterialID'] ]
    #pr['MaterialID'] = np.vectorize(class_mapping.get)(pr['MaterialID'])


@hydra.main(version_base=None, config_path='.', config_name='pc_class_config')
def main(cfg: DictConfig) -> None:
    # 0. Collect all las files to process
    src_las_files = []
    wrk_las_files = []
    tgt_las_files = []

    # get all las files
    for path, subdirs, files in os.walk(cfg['input_dir']):
        for fname in files:
            if fname.endswith('.las'):
                full_name = os.path.join(path, fname)
                tgt_dir = path.replace(cfg['input_dir'], cfg['output_dir'], 1)

                if not os.path.exists(tgt_dir):
                    os.makedirs(tgt_dir, exist_ok=True)

                src_las_files.append(full_name)
                wrk_las_files.append(f'{full_name.split('.')[-2]}-processing.las')
                tgt_las_files.append(f'{full_name.split('.')[-2]}-processed.las'.replace(cfg['input_dir'], cfg['output_dir'], 1))

    print("Clustering...")
    # 1. Cluster
    for wrk, src in progressbar(zip(wrk_las_files, src_las_files)):
        with laspy.open(src) as fh:
            las = fh.read()
            
            cluster_classes(las.points, cfg['cluster'])

            las.write(wrk)

    print('Testing classes...')
    # 2. test
    existing_classes = set()

    for wrk in progressbar(wrk_las_files):
        with laspy.open(wrk) as fh:
            las = fh.read()

            existing_classes = existing_classes | get_existing_classes(las.points)

    print("Rearranging classes...")
    # 3. rearrange
    for wrk, tgt in progressbar(zip(wrk_las_files, tgt_las_files)):
        with laspy.open(wrk) as fh:
            las = fh.read()

            rearrange_classes(las.points, list(existing_classes))

            las.write(tgt)

        # 4. delete the intermediary file
        os.remove(wrk)


if __name__ == '__main__':
    main()