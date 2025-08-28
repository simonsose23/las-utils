# Taken from laspy docs: https://laspy.readthedocs.io/en/latest/examples.html
import laspy
import numpy as np

# 0. Creating some dummy data
my_data_xx = np.array([2])
my_data_yy = np.array([2])
my_data_zz = np.array([2])
my_data = np.hstack((my_data_xx.reshape((-1, 1)), my_data_yy.reshape((-1, 1)), my_data_zz.reshape((-1, 1))))

# 1. Create a new header
header = laspy.LasHeader(point_format=3, version="1.2")
header.add_extra_dim(laspy.ExtraBytesParams(name="random", type=np.int32))
header.offsets = np.min(my_data, axis=0)
header.scales = np.array([0.1, 0.1, 0.1])

# 2. Create a Las
las = laspy.LasData(header)

las.x = my_data[:, 0]
las.y = my_data[:, 1]
las.z = my_data[:, 2]
las.random = [3]

las.write("new_file.las")