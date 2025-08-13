# LAS Utils

A collection of tools to process scalar fields 3D point clouds (in LAS/LAZ format)

## Point Cloud Class Processor: `pc_class_processor.py`

Perform multiple operations on point cloud scalar fields used for classification. It performs:
- Clustering: Merge multiple classes together into one class
- Testing: Classes without a point assigned to it are removed (can be overridden)
- Rearrange: Reassign class IDs so that no gap exists
- Rename: Rename the classification scalar field name

The operations are specified by a Hydra configuration file:

| Key | Value |
|-----|-------|
|`input_dir`|Path to directory with point clouds to process|
|`output_dir`|Path to directory where processed point clouds should be stored. Processed point clouds will have the suffix `-processed.{las,laz}`
|`scalar_field`|Name of scalar field that contains the classification info. If in doubt, use `classification`|
|`cluster`|List [$x_1, \dots, x_n$], where every $x_i$ with $1\leq i \leq n$ is a list of class IDs that should be clustered together. The resulting class will have the class ID of the smallest class ID in $x_i$|
|`rename`|Optional. Name to rename the scalar field that contains the classification info to.|
|`remap`|Optional. If given, the rearrange step mentioned above will be skipped. A list of key-value-pairs are expected, where the key corresponds to the class ID of the source point cloud that was already clustered (keep the cluster class ID assignment rule in mind!) and the value corresponds to the new, desired class ID

## Point Cloud Scalar Merger: `pc_scalar_merger.py`

Merge an scalar field onto another scalar field.

Configuration:
|Key|Value|
|---|-----|
|`pc_folder`|Path to the directory with all the point clouds to process.|
|`from_scalar`|Name of scalar field to read the values from|
|`onto_scalar`|Name of scalar field to write the values to|
|`merge_values`|Values from `from_scalar` to write to `onto_scalar`|
|`write_offset`|Integer value by which to offset `from_scalar` values before writing them into `onto_scalar`. Should be `max(point_cloud['onto_scalar']) + 1`|

## Multi-Point-Cloud Class Histogram

Plot the class densities of all point cloud datasets in the given folder. A point cloud dataset is a folder with point clouds.