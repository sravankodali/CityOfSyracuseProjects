# Import necessary libraries
from arcgis.gis import GIS
from arcgis import features
from arcgis.features import FeatureLayer
import pandas as pd
import arcpy
import os
import datetime as dt
 
def connect_to_gis(url, username, password):
    gis = GIS(url, username, password)
    print(f"Connected to {gis.properties.urlKey}.{gis.properties.customBaseUrl}")
    return gis
 

def read_csv_data(filepath):
    try:
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully from {filepath}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
 
def filter_illegal_setouts(df):
    original_count = df.shape[0]
    df_clean = df[df["Summary"] == "Illegal Setouts"]
    print(f"{original_count - df_clean.shape[0]} features have been removed from the table.")
    return df_clean
 
def save_as_csv(df, filepath):
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")
 
# Converting CSV to a feature class using ArcPy
def convert_csv_to_feature_class(csv_file, out_feature_class, x_field, y_field):
    try:
        arcpy.management.XYTableToPoint(csv_file, out_feature_class, x_field, y_field)
        print(f"Feature class created successfully at {out_feature_class}")
    except Exception as e:
        print(f"Error in creating feature class: {e}")
 
# Function to copy feature layer from ArcGIS Online to local geodatabase
def copy_feature_layer_to_gdb(url, gdb_path, layer_name):
    try:
        arcpy.FeatureClassToFeatureClass_conversion(url, gdb_path, layer_name)
        print(f"Feature layer copied to {gdb_path}")
    except Exception as e:
        print(f"Error copying feature layer: {e}")
 
def summarize_within(in_polygons, in_features, out_feature_class, group_field):
    try:
        arcpy.analysis.SummarizeWithin(
            in_polygons=in_polygons,
            in_sum_features=in_features,
            out_feature_class=out_feature_class,
            keep_all_polygons="KEEP_ALL",
            sum_fields="Request_type Sum;Id Sum;Minutes_to_closed Mean",
            sum_shape="ADD_SHAPE_SUM",
            shape_unit="SQUAREKILOMETERS",
            group_field=group_field,
            add_min_maj="NO_MIN_MAJ",
            add_group_percent="NO_PERCENT"
        )
        print(f"Summarize Within completed, output saved at {out_feature_class}")
    except Exception as e:
        print(f"Error in Summarize Within: {e}")
 
def publish_feature_class(gis, feature_class, title, snippet):
    item_properties = {
        "title": title,
        "type": "Feature Service",
        "snippet": snippet,
        "access": "private"  # Make it public if needed
    }
    try:
        item = gis.content.add(item_properties=item_properties, data=feature_class)
        print(f"Feature class published successfully with title: {title}")
        return item
    except Exception as e:
        print(f"Error in publishing feature class: {e}")
        return None
 
def main():
    gis = connect_to_gis('https://syr.maps.arcgis.com', 'SECRET', 'SECRET!')
   
    csv_filepath = r'.\csv_datasets\SYRCityline_Requests_(2021-Present).csv'
    df = read_csv_data(csv_filepath)
    df_clean = filter_illegal_setouts(df)
 
    cleaned_csv_filepath = "./data_outputs/illegal_setout.csv"
    save_as_csv(df_clean, cleaned_csv_filepath)
 
    out_feature_class = r"C:\Users\jscharf\Desktop\API Code\Syr-OpenDataNotebooks\Illegal_Setouts_Summary_Map.gdb\illegal_setout_lat_long3"
    x_field = "Lng"  # Replace with the correct longitude field
    y_field = "Lat"  # Replace with the correct latitude field
    convert_csv_to_feature_class(cleaned_csv_filepath, out_feature_class, x_field, y_field)
 
    neighborhoods_url = "https://services.arcgis.com/uDTUpUPbk8X8mXwl/arcgis/rest/services/Syracuse_Neighborhoods/FeatureServer/0"
    gdb_path = r"C:\Users\jscharf\Desktop\API Code\Syr-OpenDataNotebooks\Illegal_Setouts_Summary_Map.gdb"
    copy_feature_layer_to_gdb(neighborhoods_url, gdb_path, "Syracuse_Neighborhoods")
 
    in_features = r"C:\Users\jscharf\Desktop\API Code\Syr-OpenDataNotebooks\Illegal_Setouts_Summary_Map.gdb\illegal_setout_lat_long3"
    local_neighborhoods = r"C:\Users\jscharf\Desktop\API Code\Syr-OpenDataNotebooks\Illegal_Setouts_Summary_Map.gdb\Syracuse_Neighborhoods"
    out_feature_class_summary = r"C:\Users\jscharf\Desktop\API Code\Syr-OpenDataNotebooks\Illegal_Setouts_Summary_Map.gdb\Syracuse_Neighborhoods_SummarizeWithin_2"
    summarize_within(local_neighborhoods, in_features, out_feature_class_summary, "Category")
 
    feature_class_to_publish = r"C:\Users\jscharf\Desktop\API Code\Syr-OpenDataNotebooks\Illegal_Setouts_Summary_Map.gdb\Syracuse_Neighborhoods_SummarizeWithin_2"
    title = "Illegal Setout Summarized Within"
    snippet = f"Summarized illegal setouts data - {dt.datetime.today().strftime('%Y-%m-%d')}"
    publish_feature_class(gis, feature_class_to_publish, title, snippet)
 
if __name__ == "__main__":
    main()