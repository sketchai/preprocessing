from typing import Dict
import logging
import copy


from src.filters.abstract_filter import AbstractFilter
from src.filters.factory import pipeline_factory

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class PipelineFilter(AbstractFilter):
    """
        A filter that exectutes a pipeline each time self.process() is called.
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()

        self.conf_pipeline = conf_filter.get('sub_pipeline')

    def process(self, message: object) -> object:

        # Create a new pipeline and update the source
        curr_pipeline: Dict = copy.deepcopy(self.conf_pipeline)
        pipeline = pipeline_factory(curr_pipeline.add(message))

        # Launch the pipeline
        message = self.pipeline.execute()

        return message
