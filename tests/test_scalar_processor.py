import numpy as np
import src.pc_class_processor as pc_proc

class MockLasObject():

    def __init__(self, scalar_array, scalar_field='mock_field_name'):
        self.remove_extra_dim_calls = []

        self.points = np.array(scalar_array, dtype=[(scalar_field, np.int8)])

    def remove_extra_dim(self, scalar_field):
        self.num_remove_extra_dim_calls.append(scalar_field)

def test_cluster_classes_clustering():
    # configure las object
    scalar_array = [1, 2, 3, 4, 5]
    las_object = MockLasObject(scalar_array)

    # prepare call
    scalar_field = 'mock_field_name'
    cluster_dict = {4: [2, 3], 6: [4, 5]}
    
    pc_proc.cluster_classes(las_object, cluster_dict, scalar_field)

    assert np.array_equal(las_object.points[scalar_field], np.array([1, 4, 4, 6, 6]))
    assert len(las_object.remove_extra_dim_calls) == 0
