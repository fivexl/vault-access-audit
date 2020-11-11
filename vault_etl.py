import pandas
import os
import json
import sys

def json_file_to_df(file_path):
    df = pandas.DataFrame()
    print(f'Reading {file_path}')
    with open(file_path) as data_file:
        for json_obj in data_file:
            unfilteres_df = pandas.json_normalize(json.loads(json_obj))
            unfilteres_df.drop(unfilteres_df.filter(regex='^(?:response|request).data.*').columns, axis=1, inplace=True)
            df = df.append(unfilteres_df)
    return df

logs_path = sys.argv[1]
out_path = sys.argv[2]

print(f'Processing {logs_path} and storing result to {out_path}')

df = pandas.DataFrame()

if os.path.isdir(logs_path):
    print(f'{logs_path} is a dir. Parse all files inside it')
    for dir_name, subdirs, files in os.walk(logs_path):
        for file_name in files:
            file_path = os.path.join(logs_path, dir_name, file_name)
            df.append(json_file_to_df(file_path))
elif os.path.isfile(logs_path):
    print(f'{logs_path} is a file. Parse it')
    df = json_file_to_df(logs_path)
else:
    print(f'{logs_path} is not a dir or path. Do not know what to do')
    sys.exit(1)

print('Resulting data frame')
print(df)
print(f'Writing to {out_path}')
df.to_parquet(out_path, compression='gzip')
