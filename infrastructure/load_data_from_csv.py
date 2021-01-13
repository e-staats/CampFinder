from pandas import read_csv

def load_data_from_csv(file_name):
    data = read_csv(file_name,  header=0)
    return data.values.tolist()

if __name__ == "__main__":
    print(load_data_from_csv("C:\\Users\\erick\\python\\wi-park-scraper\\WI-park-scraper\\park_data\\wi_regions.csv"))