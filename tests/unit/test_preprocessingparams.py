import os
import sys


import unittest
import pickle
from experiments import DOF_MAX, L_MAX, L_MIN, N_BINS
from experiments.preprocessing_params import export_parameters
from sam.primitive import PrimitiveType
from sam.constraint import ConstraintType
from src.utils.logger import logger


class TestPreprocessingParams(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.output_path = 'tests/asset/out/mock_params.pkl'
        self.clean = True

    def test_preprocessing_params(self):

        export_parameters(fo=self.output_path)

        with open(self.output_path,'rb') as myfile:
            d_params = pickle.load(myfile)
        
        self.assertEqual(d_params['lMax'],L_MAX)
        self.assertEqual(d_params['lMin'],L_MIN)
        self.assertEqual(d_params['dof_max'],DOF_MAX)
        self.assertEqual(d_params['n_bins'],N_BINS)

        l_name_primitive = [key.name for key in PrimitiveType]
        for key, d in d_params['node_feature_dimensions'].items():
            self.assertTrue(key in l_name_primitive)
            self.assertIsInstance(d, dict)
            for k,v in d.items():
                self.assertIsInstance(k,str)
                self.assertIsInstance(v,int)

        l_name_constraint = [key.name for key in ConstraintType]
        for key, d in d_params['edge_feature_dimensions'].items():
            self.assertTrue(key in l_name_constraint)
            self.assertIsInstance(d, dict)
            for k,v in d.items():
                self.assertIsInstance(k,str)
                self.assertIsInstance(v,int)
            
        for key, n in d_params['node_idx_map'].items():
            if key in ['void','SN_pnt1','SN_pnt2','SN_center']:
                pass
            else:
                self.assertTrue(key in l_name_primitive)
            self.assertIsInstance(n, int)
        
        for key, n in d_params['edge_idx_map'].items():
            if key == 'Subnode':
                pass
            else:
                self.assertTrue(key in l_name_constraint)
            self.assertIsInstance(n, int)

        self.assertEqual(d_params['padding_idx'], len(d_params['node_idx_map'])-1)
        

    def tearDown(self) -> None:
        if self.clean and os.path.isfile(self.output_path):
            os.remove(self.output_path)

