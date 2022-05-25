from typing import Dict
import logging
from filtering_pipeline import KO_FILTER_TAG
from filtering_pipeline.filters.abstract_filter import AbstractFilter

from sketchgraphs_vs_sam.convert.convert_sequence import convert_sequence

class FilterConvertSequence(AbstractFilter):
    def __init__(self, conf: Dict):
        self.name = 'FilterConvertSequence'
        super().__init__(conf)
        self.nb_nodes = conf.get('nb_nodes')
        self.nb_edges = conf.get('nb_edges')

    def process(self, message: Dict) -> Dict:  
        from sketchgraphs.data.sequence import NodeOp
        seq = message.get('sequence')
        try :
            convert_seq, nb_edges, nb_nodes = convert_sequence(seq)
            
        except Exception as e :
            print(f'e= {e}')
            cpt = 0
            for i,e in enumerate(seq) :
                if isinstance(e, NodeOp):
                    print(f'  {cpt}. {e}')
                    cpt += 1
                else :
                    print(f'     . {e}')
            raise AttributeError
        if convert_seq is None or nb_edges < self.nb_edges:
            message[KO_FILTER_TAG]=self.name
        else :
            message['sequence'] = convert_seq.sequence
        return message
