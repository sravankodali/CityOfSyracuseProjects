from schema_extract.create_position_dict import create_start_positions_dict
from value_extract.parse_export_v4 import parse_export_v4
from value_extract.data_merge import merge_values_with_df
from schema_extract.import_export_alignment import values_to_be_imported
from schema_extract.import_export_alignment import length_dict
from schema_extract.import_export_alignment import FixedWidthFieldLine

import pandas as pd
from tqdm import tqdm
import time

def main(): 
    print("Starting the process...")

    # Parse the export_v4.txt file, returns dataframes of values
    print("Parsing export_v4.txt...")
    account_numbers_df, meter_readings_df, dials_df, reverse_flow_df, no_flow_days_df, date_read = parse_export_v4('transfer_files/export_v4.txt')

    # Load the meter_caps file separately
    print("Loading meter_caps.csv...")
    meter_caps = pd.read_csv('transfer_files/meter_caps.csv')
    meter_caps.rename(columns={'METER CAPACITY': 'Meter_Capacity'}, inplace=True)

    # Merge account numbers with meter_caps (single Account # column)
    print("Merging data...")
    merged_df = pd.merge(meter_caps, account_numbers_df.rename(columns={'DISP14': 'ACCOUNT #'}), on='ACCOUNT #', how='inner')
    merged_df.rename(columns={'ACCOUNT #': 'DISP14'}, inplace=True)
  
    # Add data to the merged DataFrame
    merge_values_with_df(merged_df, meter_readings_df, dials_df, reverse_flow_df, no_flow_days_df, date_read)
    
    # Create dictionary with start positions from schema for as/400 import to confirm values are in the right spots
    print("Creating start positions dictionary...")
    start_positions_dict = {}
    create_start_positions_dict(length_dict, start_positions_dict)
    # print("Start positions dictionary created:", start_positions_dict)
    print("The following features are being imported: ", values_to_be_imported)

    print("Writing to output file...")
    with open("output/import.txt", "w") as output_file:
        for _, row in tqdm(merged_df.iterrows(), total=merged_df.shape[0]):
            line = FixedWidthFieldLine()
            for key in start_positions_dict:
                if key in values_to_be_imported:
                    setattr(line, key, str(row[key]))
            output_file.write(str(line) + "\n")
            time.sleep(0.01)

    print("Process completed successfully.")

if __name__ == "__main__": 
    main()

# things left to do: check if anything else from radio_meta_deta can be parsed from v4
# if so, here are the steps: 
# (1) add column name to values_to_be_imported in schema_extract/import_export_alignment
# (2) actually extract it in value_extract/parse_export_v4, and create a dataframe for it 
# (3) go to value_extract/data_merge and add a line to merge this new data
