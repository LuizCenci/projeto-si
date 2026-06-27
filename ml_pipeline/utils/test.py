import pandas as pd
PATH = '../data/'
df = pd.read_csv(PATH + 'Stress_Dataset.csv')
print(df.head())