# containers/column_context.py

from typing import Dict, Union, Any

class ColumnContext:
    ''' Contains data for '''
    def __init__(self):
        pitch: Union[int, None] = None
        inst: Union[int, None] = 0
        vol: Union[int, None] = 15
        effects: Dict[str, Any] = {}

