import sys


import unittest
import numpy as np

from src.utils.bounding_box import compute_coords_of_entity
from src.filters.on_exchangeformat.filter_boundingbox import FilterBoundingBox

from sam.catalog_primitive import *
from sam.catalog_constraint import *
from sam.sketch import Sketch

from filtering_pipeline import KO_FILTER_TAG
from src.utils.logger import logger

class TestFilterBoundingBox(unittest.TestCase):

    def test_last_process(self):
        sketch = Sketch()
        sketch.add(Point(point = [1., 2.]))
        sketch.add(Circle(center = [3., 4. ], radius = 5.))
        sketch.add(Distance(references=[1,2], distance_min = 6.))
        sketch.add(Length(references=[10], length = 6.))
        sketch.add(Radius(references=[48], radius = 6.))
        arc = Arc(center = [7., -7.], radius = 7., angles = [.5*np.pi,np.pi])
        arc.add_points_startend()
        sketch.add(arc)
        sketch.add(Line(pnt1 = [8.,-8.], pnt2 = [9.,10.]))

        self.conf_filter = {
            'request_coord': {
                'POINT' : ['x', 'y'],
                'LINE' : ['pnt1', 'pnt2'],
                'ARC' : ['pnt1', 'pnt2','center'],
                'CIRCLE' : 'center',
            },
            'request_length': {
                'ARC' : 'radius',
                'CIRCLE' : 'radius',
                # 'DISTANCE': 'distance_min',
                'LENGTH': 'length',
                'RADIUS': 'radius',
            }}


        filter1 = FilterBoundingBox(conf=self.conf_filter)

        for op in sketch.sequence:
            message = {'op': op}
            message = filter1.process(message)

        message = filter1.last_process(message)
        

        # check that the NodeOps are in the box
        for op in sketch.sequence:

            x_coords, y_coords = compute_coords_of_entity(op)
            for coord in x_coords + y_coords:
                self.assertGreater(coord,-0.0001)
                self.assertLess(coord,1.0001)
        
        # check that EdgeOps are also normalized
        constraints_parameter = [
            # sketch.sequence[2].distance_min,
            sketch.sequence[3].length,
            sketch.sequence[4].radius,
        ]
        logger.info(f'message: {constraints_parameter}')
        for parameter in constraints_parameter:
            self.assertGreater(parameter,-2**0.5 + 1e-4)
            self.assertLess(parameter,2**0.5 + 1e-4)

