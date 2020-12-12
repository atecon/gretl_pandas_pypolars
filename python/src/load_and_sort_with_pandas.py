import timeit
import pandas as pd

start = timeit.default_timer()
df = pd.read_csv('./data/users.csv')
stop = timeit.default_timer()
print('Loading csv file took Pandas: ', stop - start)

start = timeit.default_timer()
df.sort_values('n', ascending=False)
stop = timeit.default_timer()
print('Sorting the data frame took Pandas: ', stop - start)
