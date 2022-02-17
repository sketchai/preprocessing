from ..filteringpipeline.src.filters.abstract_filter import AbstractFilter


class FilterNormalization(AbstractFilter):
    """
        A filter that normalizes that applies homotheties and translations to cast angles, positions and lengths in a constant interval.
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()
        self.wrong_ob_cnt: int = 0

    def process(self, message: object) -> object:
        logger.debug(f'message received: {message}')
        if message.get('a'):
            message['a'] += 1
        if message.get('b'):
            self.wrong_ob_cnt += 1
        if message.get('c'):
            message.update({KO_FILTER_TAG: self.name})
        return message

# Operation de normalization 
# a. Line : CenterSegment (tâche element par element sur une séquence)
# b. Center Sketch : tâche dont l'operation s'effectue sur l'ensemble de la séquence
# c. Mise aux normes des distances : conversion + retrait si pas les bonnes unités. Opération sur l'opération
# d. Normalization des distances. Opération sur la séquence
# e. Conversion des angles 0, 2pi

#############
import numpy as np

from sketchgraphs.data import sequence
from maps.maps import *

paramsCoordsX = {
    datalib.EntityType.Point: 'x',
    datalib.EntityType.Line: 'pntX',
    datalib.EntityType.Circle: 'xCenter',
    datalib.EntityType.Arc: 'xCenter'
}
paramsCoordsY = {
    datalib.EntityType.Point: 'y',
    datalib.EntityType.Line: 'pntY',
    datalib.EntityType.Circle: 'yCenter',
    datalib.EntityType.Arc: 'yCenter'
}

paramsEntityLength = {
    datalib.EntityType.Point: ['x', 'y'],
    datalib.EntityType.Line: ['pntX', 'pntY', 'startParam', 'endParam'],
    datalib.EntityType.Circle: ['xCenter', 'yCenter', 'radius'],
    datalib.EntityType.Arc: ['xCenter', 'yCenter', 'radius']
}
constraintsLength = [
    datalib.ConstraintType.Distance,
    datalib.ConstraintType.Length,
    datalib.ConstraintType.Diameter,
    datalib.ConstraintType.Radius,
]
# parameter : 'length'

def normalization(seqs):
    """
    Applies homotheties and translations to cast angles, positions and lengths in a constant interval.
    """
    # center segments
    for i, seq in enumerate(seqs):
        for op in seq:
            if isinstance(op, sequence.NodeOp) and op.label==datalib.EntityType.Line:
                op.parameters['pntX'] += op.parameters['startParam'] * op.parameters['dirX']
                op.parameters['pntY'] += op.parameters['startParam'] * op.parameters['dirY']
                op.parameters['endParam'] -= op.parameters['startParam']
                op.parameters['startParam'] = 0

    # center sketch
    for i, seq in enumerate(seqs):
        pointsX = []
        pointsY = []
        for op in seq:
            if isinstance(op, sequence.NodeOp) and op.label in paramsCoordsX:
                pointsX.append(op.parameters[paramsCoordsX[op.label]])
                pointsY.append(op.parameters[paramsCoordsY[op.label]])
        baryX = np.mean(pointsX)
        baryY = np.mean(pointsY)
        for op in seq:
            if isinstance(op, sequence.NodeOp) and op.label in paramsCoordsX:
                op.parameters[paramsCoordsX[op.label]] -= baryX
                op.parameters[paramsCoordsY[op.label]] -= baryY

    # convert numerical values
    seqs1 = []

    for i, seq in enumerate(seqs):
        filtre = False
        for op in seq:
            if isinstance(op, sequence.EdgeOp) and op.label==datalib.ConstraintType.Angle:
                angle = op.parameters['angle']
                if ' DEGREE' in angle:
                    op.parameters['angle'] = float(angle.replace(' DEGREE', '')) * np.pi/180
                else:
                    filtre = True
            if isinstance(op, sequence.EdgeOp) and op.label in constraintsLength:
                if 'length' in op.parameters:  # some distances do not have length
                    length = op.parameters['length']
                else:
                    filtre = True
                    break
                if ' METER' in length:
                    op.parameters['length'] = float(length.replace(' METER', ''))
                else:
                    filtre = True
        if not filtre:
            seqs1.append(seq)

    # normalize lengths in [-1,1]
    seqs2 = []

    for i, seq in enumerate(seqs1):
        lengths = []
        for op in seq:
            if isinstance(op, sequence.NodeOp) and op.label in paramsEntityLength:
                for param in paramsEntityLength[op.label]:
                    lengths.append(abs(op.parameters[param]))
            elif isinstance(op, sequence.EdgeOp) and op.label in constraintsLength:
                lengths.append(abs(op.parameters['length']))
        normalization = max(lengths)
        if normalization==0:
            continue

        for op in seq:
            if isinstance(op, sequence.NodeOp) and op.label in paramsEntityLength:
                for param in paramsEntityLength[op.label]:
                    op.parameters[param] /= normalization
            elif isinstance(op, sequence.EdgeOp) and op.label in constraintsLength:
                op.parameters['length'] /= normalization

        seqs2.append(seq)

    # normalize angles in [0,2*pi]
    for i, seq in enumerate(seqs2):
        for op in seq:
            if isinstance(op, sequence.NodeOp) and op.label==datalib.ConstraintType.Angle:
                op.parameters['angle'] = op.parameters['angle']%(2*np.pi)
            if isinstance(op, sequence.NodeOp) and op.label==datalib.EntityType.Arc:
                op.parameters['startParam'] = op.parameters['startParam']%(2*np.pi)
                op.parameters['endParam'] = op.parameters['endParam']%(2*np.pi)
                
    print("{:.1%} of the sketches were discarded by the normalization.".format(1-len(seqs2)/len(seqs)))
                
    return seqs2
