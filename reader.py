import pandas as pd
from pathlib import Path
import numpy as np
csv_folder = Path(r"C:\Users\andrs\PycharmProjects\connecting_CSV's_files")
csv_path = Path(list(csv_folder.glob('*.csv'))[0])

df = pd.read_csv(csv_path)
print(df.info())

# def funcccccc(text):
#     return '-' not in text

# df['invalid'] = df['floor'].apply(funcccccc)
# df = df[df['invalid']]
# df = df.drop('invalid', axis=1)

for column in df.columns:
    if (column != 'distance_from_centre' and
        column != 'filename' and
        column != 'price' and
        column != 'floor' and
        column != 'year_of_construction'):
        df[column] = df[column].apply(lambda x: x.replace(',', '.'))
        df[column] = df[column].astype(float)

print(df.info())
df.to_csv('FlatsInSaratov.csv', index=False, encoding="utf-8")
# for idx, row in df.iterrows():
#     print(row)

print(df[df.columns[:-2]])





