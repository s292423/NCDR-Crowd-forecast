import pandas as pd
from datetime import datetime

temp = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

wanna_get_columns = ['﻿POPULATION', 'Age0019', 'Age2029', 'Age3039', 'Age4049', 'Age5059', 'Age6099', 'Grid500', 'TIME', 'TownID']
wanna_merge_csv = 'G_ID_Gird500.csv'


def read_csv_and_merge(month, grid):
    data = pd.read_csv('./txt/2018' + month + '.txt', encoding='utf-8')
    res = pd.merge(data, grid, on='Grid500', how='left')
    res = res[wanna_get_columns]

    return res


def clean_data_for_new_csv(month, res):

    temp_list_to_new_csv = []

    for index, row in res.iterrows():
        time = str(row["TIME"])[:-6]
        time = datetime.strptime(time, '%Y%m%d%H')
        time = time.strftime('%Y-%m-%d %H:%M:%S')
        site = row["Grid500"].split('_')
        temp_list_to_new_csv.append(
            [time, row["TownID"], site[0], site[1], row["Age0019"], row["Age2029"], row["Age3039"], row["Age4049"],
             row["Age5059"], row["Age6099"], row["﻿POPULATION"]])
    new_data = pd.DataFrame(temp_list_to_new_csv,
                            columns=['Time', 'TownID', 'Longitude', 'Latitude', 'Age1', 'Age2', 'Age3', 'Age4',
                                     'Age5', 'Age6',
                                     'Total'])
    new_data.to_csv("./output/2018" + month + ".csv")
    print(month)


def main():
    grid = pd.read_csv(wanna_merge_csv, encoding='utf-8')
    for i in temp:
        merge_csv = read_csv_and_merge(i, grid)
        clean_data_for_new_csv(i, merge_csv)


if __name__ == "__main__":
    main()
