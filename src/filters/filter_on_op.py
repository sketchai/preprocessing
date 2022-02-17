from typing import Dict
import logging
import copy


from src.filteringpipeline.src.filters.catalog_filter.subpipeline_filter import SubPipelineFilter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class OpSubPipelineFilter(SubPipelineFilter):
    """
        A filter that exectutes a pipeline each time self.process() is called.
    """

    def update_conf_pipeline(self, message) -> object:
        return {self.source_name: {'parms': {'l_data': message.get('data')}}}
