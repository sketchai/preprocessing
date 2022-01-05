from abc import abc
from typing import Dict

class AbstractFilter(abc):

    def __init__(self, conf_filter : Dict = {}):
        self.wrong_ob_cnt : int = 0


    @abstractmethod
    def check(self, ob: object) -> bool:
        raise NotImplementedError("check function must be implemented")
    
    def check_last(self, ob:object):
        return self.check(ob)

    def update_wrong_ob(self) :
        self.wrong_ob_cnt += 1 








