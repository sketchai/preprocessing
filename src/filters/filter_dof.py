from typing import Dict
import logging
from ..filteringpipeline.src.filters.abstract_filter import AbstractFilter
from src.sketchgraphs.sketchgraphs.data.dof import get_sequence_dof

class FilterDof(AbstractFilter):
  def __init__(conf:Dict) :   
     # mettre les arguments dont on a besoin
     pass

  def process(self,message : Dict) -> Dict: # to implement
    seq = message['sequence']
    array_dof = get_sequence_dof(seq)
    dof = sum(array_dof)
    message['dof'] = dof
    return message
