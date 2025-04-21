# helper_functions.py

from typing import Tuple

def generate_token_key(pat: int, row: int, col: int) -> Tuple[int, int, int]:
    ''' Function for generating keys for the token hash '''
    # Return a tuple key for efficient lookup
    return (pat, row, col)

