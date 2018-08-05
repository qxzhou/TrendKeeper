import json
import pandas as pd
import os.path
import numpy as np
import re #regular expression matching


def raw_data_cleanup(filename):
    """
    load rawdata.json and do basic cleanup
    -enter filename with extension as str, file should be in subdirectory raw_data

    param: filename, str
    return: DataFrame
    """

    if os.path.isfile(filename):
        print("{} is located in current directory".format(filename))

        with open(filename) as json_file:
            print(1)

            data = json.load(json_file)
        df = pd.DataFrame(data, columns=['date', 'location', 'category', 'keyword'])
        print("{} is imported into dataframe".format(filename))
        df.to_csv('./output.csv', index=False)
        # Generate city column from location
        city_list = []
        for i in df['location']:
            if ',' in i:
                city = i.split(',')[0]
                city_list.append(city)
            else:
                city_list.append(i)
        df['city'] = city_list

        # Datetime transformation

        # Check Top places (location) where news are coming from
        city_sort = df['city'].groupby(df['city']).count().sort_values(ascending=False)

        # Save DataFrame into csv file
        city_sort.to_csv('./city_sort.csv')

    else:
        print("{} does not exist in directory. Function was not complete.".format(filename))

    return

raw_data_cleanup('test.json')