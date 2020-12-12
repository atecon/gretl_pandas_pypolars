import timeit
import pypolars as pl

start = timeit.default_timer()
df = pl.read_csv('./data/users.csv')
stop = timeit.default_timer()
print('Loading csv file took pypolars: ', stop - start)

start = timeit.default_timer()
df.sort(by_column='n', reverse=True)
stop = timeit.default_timer()
print('Sorting the data frame took pypolars: ', stop - start)
