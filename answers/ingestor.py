import os
import pandas as pd
from tqdm import tqdm

def IngestData(dirpath):
    data = []  

    for filename in tqdm(os.listdir(dirpath),ascii=True):
        if filename.endswith(".txt"):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, "r") as file:
                for line in file:
                    
                    row = line.strip().split()
                    row.append(filename[:11])
                    row[0] = str(row[0])
                    row[1] = int(row[1])
                    row[2] = int(row[2])
                    row[3] = int(row[3])
                    row[4] = str(row[4])
                    row.append(row[0][:4])
                    data.append(row)

    df = pd.DataFrame(data, columns=["dt", "MaxTemp", "MinTemp", "PPT", "StationID", "Year"])
    df = df[(df['MaxTemp'] != -9999) & (df['MinTemp'] != -9999) & (df['PPT'] != -9999)]
    return df

def WeatherResult(df):
    result = df.groupby(['Year', 'StationID']).agg(
    AvgMaxTemp=('MaxTemp', 'mean'),
    AvgMinTemp=('MinTemp', 'mean'),
    AccPPT=('PPT', 'sum')
    )
    result = result.reset_index()
    return result
