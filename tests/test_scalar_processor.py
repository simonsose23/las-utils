import numpy as np
from src.pc_class_processor import ScalarClassClusterer, main
import laspy

class MockLasObject():

    def __init__(self, scalar_array, scalar_field='mock_field_name', empty_col_name='foo'):
        self.remove_extra_dim_calls = []

        self.points = np.array(scalar_array, dtype=[(scalar_field, np.int8), (empty_col_name, np.int8)])

    def remove_extra_dim(self, scalar_field):
        self.remove_extra_dim_calls.append(scalar_field)

class MockClusterClassObject():
    
    def __init__(self):
        self.calls = []

    def execute(self, *args, **kwargs):
        self.calls.append({'args': args, 'kwargs': kwargs})

class MockLasReader():

    def __init__(self):
        self.write_calls = []

    def read(self, *args, **kwargs):
        return MockLasData(self.write_calls)

class MockLasData():

    def __init__(self, write_calls):
        self.write_calls = write_calls

    def write(self, *args, **kwargs):
        self.write_calls.append({'args': args, 'kwargs': kwargs})

def test_cluster_classes_clustering():
    # configure las object
    scalar_array = [1, 2, 3, 4, 5]
    las_object = MockLasObject(scalar_array)

    # prepare call
    scalar_field = 'mock_field_name'
    cluster_dict = {4: [2, 3], 6: [4, 5]}
    
    ScalarClassClusterer().execute(las_object, cluster_dict, scalar_field)

    assert np.array_equal(las_object.points[scalar_field], np.array([1, 4, 4, 6, 6]))
    assert len(las_object.remove_extra_dim_calls) == 0

def test_cluster_classes_rename():
    # configure las object
    scalar_array = [1]
    las_object = MockLasObject(scalar_array)

    ScalarClassClusterer().execute(las_object, {}, 'mock_field_name', 'foo')

    assert las_object.remove_extra_dim_calls == ['mock_field_name']
    assert np.array_equal(las_object.points['foo'], np.array([1]))

def test_cluster_classes_default_class():
    scalar_array = [1, 2, 3, 4]
    las_object = MockLasObject(scalar_array)

    cluster_dict = {2: [2, 3, 4]}
    
    ScalarClassClusterer().execute(las_object, cluster_dict, 'mock_field_name', default_class=3)

    assert np.array_equal(las_object.points['mock_field_name'], np.array([3, 2, 2, 2]))

def test_cluster_classes_wildcard():
    scalar_array = [1, 2, 31, 32, 33]
    las_object = MockLasObject(scalar_array)

    cluster_dict = {3: ['3x']}

    ScalarClassClusterer().execute(las_object, cluster_dict, 'mock_field_name')

    assert np.array_equal(las_object.points['mock_field_name'], np.array([1, 2, 3, 3, 3]))

def test_file_handling(monkeypatch):
    cluster_obj = MockClusterClassObject()
    mock_las_reader = MockLasReader()

    monkeypatch.setattr(laspy.LasReader, "read", mock_las_reader.read)
    monkeypatch.setattr(ScalarClassClusterer, "execute", cluster_obj.execute)

    cfg = {'input_dir': 'tests/data/', 'output_dir': 'tests/data/', 'cluster': {}, 'scalar_field': 'mock_field_name', 'rename': 'bar', 'default_class': 2}

    main(cfg)

    # check cluster call
    assert len(cluster_obj.calls) == 2
    
    call_args = cluster_obj.calls[0]['args']
    call_kwargs = cluster_obj.calls[0]['kwargs']

    assert call_args[1] == cfg['cluster']
    assert call_args[2] == cfg['scalar_field']

    assert call_kwargs['rename'] == cfg['rename']
    assert call_kwargs['default_class'] == cfg['default_class']

    # check for write call
    tgt_file_names = [ call['args'][0] for call in mock_las_reader.write_calls ]

    assert 'tests/data/foo-processed.las' in tgt_file_names
    assert 'tests/data/foo2-processed.las' in tgt_file_names