import pandas as pd

# Create a list of values we're importing
values_to_be_imported = {'DISP14','MREAD','NDIAL','REVFLR','DAYSZR', 'DTER'}

#Create a dictionary for the lengths of the fields
length_dict = pd.read_csv('transfer_files/length_dict.csv').set_index('NAME')['LENGTH'].to_dict()

# Create a class for fixed-width lines 
class FixedWidthFieldLine(): 
    fields = length_dict

    def __init__(self):
        for field in self.fields:
            setattr(self, field, "")

    def __str__(self):
        return "".join([getattr(self, field_name).ljust(width) for field_name, width in self.fields.items()])


