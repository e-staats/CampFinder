from pandas import read_csv

def load_data_from_csv(file_name):
    data = read_csv(file_name,  header=0)
    return data.values.tolist()