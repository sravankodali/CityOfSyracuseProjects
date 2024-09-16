import pandas as pd

# use the lengths dictionary to create a dictionary with the start positions: 
def create_start_positions_dict(length_dict, start_positions_dict): 
    current_position = 0
    for key, length in length_dict.items():
        start_positions_dict[key.upper()] = current_position
        current_position += length
    



