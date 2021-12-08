import pandas as pd

df1 = pd.DataFrame({'A': [1, 0, 0],
                    'B': [0, 0, 0],
                    'C': [0, 0, 0],
                    'D': [0, 0, 0]})
list_to_clean = [0,
                 1,
                 2,
                 4,
                 6,
                 7,
                 8,
                 9,
                 10,
                 11,
                 12,
                 13,
                 14,
                 15,
                 16,
                 17,
                 18,
                 19,
                 20,
                 21,
                 22,
                 23,
                 24,
                 25,
                 26,
                 27,
                 ]
for n in list_to_clean:
    df1[df1[df1.iloc[:, [n]].columns[0]].name] = df1[df1.iloc[:, [n]].columns[0] != None] = None
    df1 = df1.drop([df1[df1.iloc[:, [-1]].columns[0]].name], axis=1)
print(df1)