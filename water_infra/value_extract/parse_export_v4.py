import pandas as pd

# Function to parse the export_v4.txt file to extract necessary data and convert into dataframes
# Uses the radio_meta_data schema 
def parse_export_v4(file_path):
    account_numbers = []
    meter_readings = []
    reverse_flow = []
    no_of_dials = []
    no_flow_days = []
    date_read = ""
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('COMHD'):
                date_read = line[9:17].strip()
            if line.startswith('PRMD'):
                account_no = line[103:122].strip()
                account_numbers.append({
                    'DISP14': account_no
                })
            elif line.startswith('RDGDT'):
                dial_no = line[49:50].strip()
                no_of_dials.append({
                    'NDIAL': dial_no
                })
                meter_read = line[98:107].strip()
                meter_readings.append({
                    'MREAD': meter_read
                })
                nf = line[112].strip()
                no_flow_days.append({
                    'DAYSZR': nf
                })
                rf = line[113].strip()
                reverse_flow.append({
                    'REVFLR': rf
                })

    # Create DataFrames
    account_numbers_df = pd.DataFrame(account_numbers)
    meter_readings_df = pd.DataFrame(meter_readings)
    dials_df = pd.DataFrame(no_of_dials)
    reverse_flow_df = pd.DataFrame(reverse_flow)
    no_flow_days_df = pd.DataFrame(no_flow_days)
    
    return account_numbers_df, meter_readings_df, dials_df, reverse_flow_df, no_flow_days_df, date_read


