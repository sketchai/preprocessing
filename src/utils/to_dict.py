from collections import defaultdict
from typing import Dict
import collections.abc
import yaml
from sam.constraint import ConstraintType
from sam.primitive import PrimitiveType
PRIMITIVE_TYPE_MAPPING = {p.name: p for p in PrimitiveType}
CONSTRAINT_TYPE_MAPPING = {c.name: c for c in ConstraintType}

yaml.add_constructor(u'!PrimitiveType', (lambda l,n : PRIMITIVE_TYPE_MAPPING[l.construct_scalar(n)]))
yaml.add_constructor(u'!ConstraintType', (lambda l,n : CONSTRAINT_TYPE_MAPPING[l.construct_scalar(n)]))

try:
    from sketchgraphs.data.sequence import NodeOp, EdgeOp, EntityType, ConstraintType as SG_ConstraintType, SubnodeType
    SG_ENTITY_TYPE_MAPPING = {e.name: e for e in EntityType}
    SG_CONSTRAINT_TYPE_MAPPING = {c.name: c for c in SG_ConstraintType}
    SG_SUBNODE_TYPE_MAPPING = {s.name: s for s in SubnodeType}

except ModuleNotFoundError:
    SG_ENTITY_TYPE_MAPPING = defaultdict(lambda : None)
    SG_CONSTRAINT_TYPE_MAPPING = defaultdict(lambda : None)
    SG_SUBNODE_TYPE_MAPPING = defaultdict(lambda : None)

yaml.add_constructor(u'!SGEntityType', (lambda l,n : SG_ENTITY_TYPE_MAPPING[l.construct_scalar(n)]))
yaml.add_constructor(u'!SGConstraintType', (lambda l,n : SG_CONSTRAINT_TYPE_MAPPING[l.construct_scalar(n)]))
yaml.add_constructor(u'!SGSubnodeType', (lambda l,n : SG_SUBNODE_TYPE_MAPPING[l.construct_scalar(n)]))

def yaml_to_dict(file_path: str) -> Dict:
    with open(file_path, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        return data
    return None


def update_nested_dict(d: Dict, u: Dict) -> Dict:
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_nested_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d
