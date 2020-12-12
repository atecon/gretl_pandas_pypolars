# Performance comparison between Gretl, Python-Pandas and Python-Py-Polars reading csv-files and sorting a data set (frame)

After reading [this](https://www.kdnuggets.com/2020/12/rising-library-beating-pandas-performance.html) article comparing the performance of reading a csv file and sorting a large data set with 26 million rows and two columns, I wanted to see how Gretl performs in this competition.

Take into account that this 'project' only focuses on two aspects:

1) Reading performance for large csv files.

2) Performance of sorting the data set by the number of comments.


# Main results
1) Py-polars takes about 2.5 seconds to load a 360MB large csv file as a data frame. Pandas is about 5 times slower while Gretl needs 36 seconds for this.

2) Sorting 26 million records takes py-polars about 4.6 seconds and hence is just slightly faster than Pandas  with 5.8 sec. -- ok, still 20% percent. Gretl needs about 14 seconds for the same task.


# Technical details
## The data set
The data set ```users.csv``` can be obtained from kaggle [here](https://www.kaggle.com/colinmorris/reddit-usernames) (you need an account though). The csv file is about 360 MB large and contains the user name of any reddit account that has left at least one comment, and their number of comments. In total, 26 million users are listed.

## Hardware used
- Intel(R) Core(TM) i5-6600 CPU @ 3.30GHz
- 4 cores
- 4 threads
- 16GB RAM

## Program and library versions
The following program version were used:

**Gretl**

- version 2020f (using latest git version compiled on 2020-12-12)

- All commands applied make use of built-in procedures, and hence no 3rd party libraries are needed.

**Python**

- Python version 3.8.3 (anaconda distribution)

- Pandas version 1.0.5

- py-polars version 0.0.26

Both Pandas and py-polars can be installed by executing:
```
pip install pandas==1.0.5
pip install py-polars==0.0.26
```

# Replication code
The source code can be found in [this github repo](https://github.com/atecon/gretl_pandas_pypolars). For replication on your system, you need to get the csv data file from kaggle, and you should store it in a directory named ```./gretl_pandas_pypolars/data```.

## Gretl code
The Gretl source code is stored in ```./gretl/load_and_sort.inp```. Simply execute that file.


## Python code
The source code for running the Python stuff can be found in ```./python```. The file ```load_and_sort_with_pandas.py``` executes, as its name says, the stuff using the Pandas library. ```load_and_sort_with_pypolars.py``` does the same using the py-polars library, instead.

If you want to execute the Python code from inside gretl using the [```foreign```-block](http://gretl.sourceforge.net/gretl-help/cmdref.html#foreign) under Linux, adjust the ~/.gretl2rc configuration file such that you have the following entry directing to your favorite installed Python (environment). Mine looks like this:
```
python = /home/at/anaconda3/bin/python
```


The same can be done through the GUI menu:
Tool -> Preferences -> General -> Programs

# Results
The following table summarizes the timing of the respective job in seconds:

**Job** |   **Gretl** | **Pandas** | **Py-Polars**
-----------|:-----:|:------:|:---------:
Load csv   | 36.04 | 11.62  | 2.49
Sort data  | 14.37 | 5.80   | 4.62

Py-polars dominates Pandas by factor of 5 when it comes to reading a csv *and* transforming it into a data frame. When it comes to sorting, py-polars still dominates by about 20 percent. Gretl comes not even close to these results for both tasks.


# ISSUE: Storing a large data set as a gretl binary file
For large data sets its recommended to use gretl binary data files instead of csv files.

To store a data set as a gretl binary file, simply use the [```store``` command](http://gretl.sourceforge.net/gretl-help/cmdref.html#store):
```
store <FILENAME>.gdtb  # store current data set as gdtb file
```

It can be opened by the standard [```open``` command](http://gretl.sourceforge.net/gretl-help/cmdref.html#open):
```
open <FILENAME>.gdtb
```

I tried to run the following code:
```
clear
set verbose off
set workdir "/home/at/git/gretl_pandas_pypolars"

open "./data/users.csv" --quiet
store "./data/users.gdtb"
```

I experienced that storing ```users.csv``` as a gdtb-file took *very very long*. **Actually I gave up after an hour of computation.**



