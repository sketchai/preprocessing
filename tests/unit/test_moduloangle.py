import sys

import unittest
import numpy as np

from src.filters.on_exchangeformat.filter_moduloangle import FilterModuloAngle
from src.utils.logger import logger

from sam.catalog_primitive import Arc
from sam.catalog_constraint import Angle



class TestFilterModuloAngle(unittest.TestCase):
    
    def test_process(self):

        conf_filter = {'request':
            {
                'ARC': ["angle_start","angle_end"],
                'ANGLE': "angle"
            }
        }
        filter1 = FilterModuloAngle(conf_filter)


        # testing arc node
        arc = Arc(status_construction=False, center=[0., 5.], radius=1, angles=[38.2*180, 38.5*180])
        message = filter1.process({'op': arc})
        
        op = message.get('op')
        angle_start = op.__dict__.get('angle_start')
        angle_end = op.__dict__.get('angle_end')
        self.assertAlmostEqual(angle_start, 0.2*np.pi)
        self.assertAlmostEqual(angle_end, 0.5*np.pi)

        # testing angle constraint
        angle = Angle(references= [1,2], angle= 51*180)
        message = filter1.process({'op': angle})

        op = message.get('op')
        self.assertAlmostEqual(op.__dict__.get('angle'), np.pi)
