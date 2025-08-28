import numpy as np
import src.pc_class_processor as pc_proc

def test_helloworld():
    scalar_field = 'mock_field_name'

    pr = np.array([1, 2, 3, 1], dtype=[(scalar_field, np.int8)])

    assert set([1, 2, 3]) == pc_proc.get_existing_classes(pr, scalar_field)