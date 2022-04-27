from typing import Dict
import logging
import numpy as np
from collections import defaultdict

from filtering_pipeline.filters.abstract_filter import AbstractFilter

from src.utils.bounding_box import compute_coords_of_entity
from src.utils.normalize import normalize_op
from filtering_pipeline import KO_FILTER_TAG
from src.utils.discretization import MARGIN

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

CHECK_MARGIN = MARGIN/10 # margin is smaller during checking

def update_dict(d) :
    for key,elt in d.items():
        if isinstance(elt, str):
            d[key] = [elt]
    return d


class FilterBoundingBox(AbstractFilter):
    """
        This filter
        - collects the values of the parameters to normalize 
            with the FilterCollectParamValue custom request
        - stores the x,y coords of the op
        - then computes a bounding box and normalizes the parameters

    """

    def __init__(self, conf: Dict = {}):
        super().__init__(conf)
        self.name = 'FilterBoundingBox'
        self.request_coord = update_dict(conf.get('request_coord'))
        self.request_length = update_dict(conf.get('request_length'))
        self.x_coords = []
        self.y_coords = []
        self.max_length = 0
        self.values = defaultdict(list)
        self.references = defaultdict(list)



    def collect(self, message: Dict, additional_parameters: Dict) -> Dict:
        """
        This function saves the parameters values and references into a dict
        """
        op = message.get('op')
        for param in additional_parameters:
            param_value = op.__dict__.get(param)
            self.values[param].append(param_value)
            self.references[param].append(op)
        return message
        
    def process(self, message: object) -> object:
        """
        If the operation corresponds to one of the requested couple (type, label), apply function self.apply_function()
        """
        op = message.get('op')
        
        # Collect phase

        # -- Collect the coordinates
        for name, additional_parameters in self.request_coord.items():
            if op.type.name == name:
                message = self.collect(message, additional_parameters)
                x_coords, y_coords = compute_coords_of_entity(op) 
                self.x_coords.extend(x_coords)
                self.y_coords.extend(y_coords)
        # Collect phase
        for name, additional_parameters in self.request_length.items():
            if op.type.name == name:
                message = self.collect(message, additional_parameters)
                # -- Collect the length
                for elt in additional_parameters:
                    self.max_length = max(op.__dict__.get(elt),self.max_length)
        return message

    def last_process(self, message: object) -> object:
        logger.debug(f'ref= {self.references}')
        x_max, x_min = max(self.x_coords), min(self.x_coords)
        y_max, y_min = max(self.y_coords), min(self.y_coords)

        l_max = max(
            (x_max - x_min),
            (y_max - y_min),
            self.max_length)

        if np.isclose(l_max,0.): # a revoir : racine de 2 ?
            l_max = 1.

        for key, reference_list in self.references.items():
            normalize_op(key, reference_list, coeff = {'xmin': x_min, 'ymin' : y_min, 'lmax': l_max})
            

        if not self._check_normalization():
            message[KO_FILTER_TAG] = self.name
        return message

    def _check_normalization(self,margin = CHECK_MARGIN)->bool:
        for key, reference_list in self.references.items():
            if key in ['x', 'y']: # coordinates
                for reference in reference_list:
                    value = reference.__dict__.get(key)
                    if value < (0 - margin) or value > (1+ margin):
                        logger.debug(f'found bad {key} in {reference}, v = {value}')
                        return False
            elif key in ['center', 'pnt1', 'pnt2']: # points
                for reference in reference_list:
                    point = reference.__dict__.get(key)
                    for v in [point.x, point.y]:
                        if v < (0 - margin) or v > (1+ margin):
                            logger.debug(f'found bad {key} in {reference}, v = {v}')
                            return False
            elif key in ['length','radius']: # length
                for reference in reference_list:
                    value = reference.__dict__.get(key)
                    if value < (-2**.5 - margin) or value > (2**.5+ margin):
                        logger.debug(f'found bad {key} in {reference}, v = {value}')
                        return False
        return True