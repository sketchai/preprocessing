from typing import Dict
import logging
import numpy as np

from src.filters.utils.filter_collectparamvalue import FilterCollectParamValue
from sketchgraphs.data.sequence import EdgeOp, NodeOp, EntityType, ConstraintType
from src.utils.bounding_box import compute_coords_of_entity
from filtering_pipeline import KO_FILTER_TAG

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterBoundingBox(FilterCollectParamValue):
    """
        This filter
        - collects the values of the parameters to normalize 
            with the FilterCollectParamValue custom request
        - stores the x,y coords of the op
        - then computes a bounding box and normalizes the parameters

    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__(conf_filter)
        self.name = 'FilterBoundingBox'
        self.x_coords = []
        self.y_coords = []
        self.max_length = 0

    def process(self, message):
        message = super().process(message)
        op = message['op']
        if isinstance(op,NodeOp):
            x_coords, y_coords = compute_coords_of_entity(op)
            self.x_coords.extend(x_coords)
            self.y_coords.extend(y_coords)
        if isinstance(op,EdgeOp):
            if 'length' in op.parameters:
                self.max_length = max(op.parameters['length'],self.max_length)
        return message

    def last_process(self, message: object) -> object:
        
        x_max, x_min = max(self.x_coords), min(self.x_coords)
        y_max, y_min = max(self.y_coords), min(self.y_coords)

        l_max = max(
            (x_max - x_min),
            (y_max - y_min),
            self.max_length)

        if np.isclose(l_max,0.):
            l_max = 1.

        for key, reference_list in self.references.items():
            if key in ['x','pntX','xCenter']:
                for reference in reference_list:
                    reference[key] = (reference[key] - x_min)/l_max
            elif key in ['y','pntY','yCenter']:
                for reference in reference_list:
                    reference[key] = (reference[key] - y_min)/l_max
            elif key in ['length','radius','startParam','endParam']:
                for reference in reference_list:
                    reference[key] = reference[key]/l_max

        return message