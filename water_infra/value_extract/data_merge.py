# takes the values extracted from export_v4 and combines them with meter capacities + acct numbers
def merge_values_with_df(merged_df, meter_readings_df, dials_df, reverse_flow_df, no_flow_days_df, date_read): 
    merged_df['MREAD'] = meter_readings_df['MREAD']
    merged_df['NDIAL'] = dials_df['NDIAL']
    merged_df['REVFLR'] = reverse_flow_df['REVFLR']
    merged_df['DAYSZR'] = no_flow_days_df['DAYSZR']
    merged_df['DTER'] = date_read