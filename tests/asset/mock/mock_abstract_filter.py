from typing import Dict
import logging
from src.filters.catalog.abstract_filter import AbstractFilter


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class MockFilter(AbstractFilter):
    def __init__(self, conf_filter: Dict = {}):
        self.wrong_ob_cnt: int = 0

    def check(self, ob: object) -> bool:
        logger.debug(f'message received : {ob}')
        if ob.get('a'):
            ob['a'] += 1
        if ob.get('b'):
            self.wrong_ob_cnt += 1
        return ob

    def check_last(self, ob: object):
        logger.debug(f'message received : {ob}')
        return 'Is last'
