import pandas as pd

data1 = {
    'Code': [1, 2, 3],
    'Name': ['Company1', 'Company2', 'Company3'],
    'Value': [200, 300, 400],
    'coluna04': [6, 7 ,8]
}
df1 = pd.DataFrame(data1, columns=['Code', 'Name', 'Value', 'coluna04'])

data2 = {
    'Code': [2],
    'Name': ['Company2'],
    'Value': [1000],
}

df2 = pd.DataFrame(data2, columns=['Code', 'Name', 'Value'])

res = df2.set_index(['Code',
                     'Name'
                     ])\
         .combine_first(df1.set_index(['Code',
                                       'Name'
                                       ]))\
         .reset_index()
print(res)
