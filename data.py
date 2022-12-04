import pandas as pd

def locate_data(contact_name):
    try:
        temp = data.set_index('Contact Name')

        return temp.loc[[contact_name]][['Order Code', 'SKU', 'Product Category', 'Name']]
    except:
        return None

data = pd.read_excel('/Users/youwai/Desktop/Final Year Project/Dreamshop Master_list (Jan-Jul).xlsx', header=0)