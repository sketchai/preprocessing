from src.filters.catalog_source.source_list import SourceList
STOP_PIPELINE = 'STOP'  # No more data
END_SOURCE_PIPELINE = 'END_SOURCE'  # No more data into source

# BASIC CATALOG FILTERS

CATALOG_FILTERS = {'SourceList': SourceList}


# D_FILTERS = {'label': LabelFilter,
#              'count': CountElementFilter,
#              'type': ObjectTypeFilter}
