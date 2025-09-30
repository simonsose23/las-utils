# LAS Utils

A collection of tools to process scalar fields 3D point clouds (in LAS/LAZ format)

## Point Cloud Class Processor: `pc_class_processor.py`

Remap point cloud scalar fields used for classification.

The operations are specified by a Hydra configuration file:

| Key             | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `input_dir`     | Path to directory with point clouds to process                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `output_dir`    | Path to directory where processed point clouds should be stored. Processed point clouds will have the suffix `-processed.{las,laz}`                                                                                                                                                                                                                                                                                                                                 |
| `scalar_field`  | Name of scalar field that contains the classification info. If in doubt, use `classification`                                                                                                                                                                                                                                                                                                                                                                       |
| `cluster`       | Dictionary with value pairs $(x, Y)$. $Y=[y_1, \dots, y_n]$, where every $y_i$ with $1\leq i \leq n$ is a wildcard or an class id that should be clustered together. The resulting class will have $x$ as class ID. If you want to cluster a lot of classes together, you can use a wildcard: Replacing the last digits of the id with 'x' will include all possible ids that start with the non-x digits. For example, '19x' will include all ids from 190 to 199. |
| `rename`        | Optional. Name to rename the scalar field that contains the classification info to. If using a scalar name that is reserved by the LAS standard, keep in mind the possible values (for example, 'classification' is only assigned 5 bits, so only values 0-31)                                                                                                                                                                                                      |
| `default_class` | Optional. Class to assign to points that have not been remapped. If None, non-remapped points will be deleted.                                                                                                                                                                                                                                                                                                                                                      |

## Point Cloud Scalar Merger: `pc_scalar_merger.py`

Merge a scalar field onto another scalar field.

Configuration:
|Key|Value|
|---|-----|
|`pc_folder`|Path to the directory with all the point clouds to process.|
|`from_scalar`|Name of scalar field to read the values from|
|`onto_scalar`|Name of scalar field to write the values to|
|`merge_values`|Values from `from_scalar` to write to `onto_scalar`|
|`onto_values`|Optional. Values of `onto_scalar` to write values `from_scalar` onto. It can be thought of as a mask to `onto_scalar`.|
|`write_offset`|Integer value by which to offset `from_scalar` values before writing them into `onto_scalar`. Should be `max(point_cloud['onto_scalar']) + 1`|

## Multi-Point-Cloud Class Histogram: `mult_class_hist.py`

Plot the class distribution of all point cloud datasets in the given folder. A point cloud dataset is a folder containing point clouds.

`mult_class_hist_w_perf.py` plots the class distribution and superimposes the reverse $iou$ of the given class $iou$ values.

## Confusion Matrices: `confmat.py`

Plot confusion matrices of predicted point clouds.

`python confmat.py <point cloud folder> <ground truth scalar name> <predicted scalar name>`
