# Performance comparison between Gretl, Python-Pandas and Python-Py-Polars reading csv-files and sorting a data set (frame)
After reading [this article on kdnuggets](https://www.kdnuggets.com/2020/12/rising-library-beating-pandas-performance.html) comparing the performance of reading a csv file and sorting a large data set with 26 million rows and two columns, I wanted to see how the open-source statistics and econometrics software [Gretl](gretl.sourceforge.net/) performs in this competition.

Take into account that this 'project' only focuses on two aspects:

1) Reading performance for large csv files.
2) Performance of sorting the data set by the number of comments.


# Main results
1) Py-polars takes about 2.5 seconds to load a 360 MB large csv file as a data frame. Pandas is about 5 times slower while Gretl needs 36 seconds for this.
2) However, making use of clever indexing, Gretl needs only about 12 seconds to load the csv file.
3) Sorting 26 million records takes py-polars about 4.6 seconds and hence is just slightly faster than Pandas with 5.8 sec. -- ok, still 20% percent. Latest experimental Gretl version 2020f needs about 7.8 seconds for the same task.


# Technical details
## The data set
The data set ```users.csv``` can be obtained from kaggle [here](https://www.kaggle.com/colinmorris/reddit-usernames) (you need an account though). The csv file is about 360 MB large and contains the following columns:

1) ```author```: user name of any reddit account that has left at least one comment, and
2) ```n```: their number of comments

In total, 26 million users are listed.

## Hardware used
- Intel(R) Core(TM) i5-6600 CPU @ 3.30GHz
- 4 cores
- 4 threads
- 16GB RAM

## Program and library versions
The following program version were used:

## Gretl
- Version 2020f (experimental, using latest git version compiled on 2020-12-21).\
- All commands applied make use of built-in procedures, and hence no 3rd party libraries are needed.

### Python
- Python version 3.8.3 (anaconda distribution) \
- Pandas version 1.0.5 \
- py-polars version 0.0.26 \

Both Pandas and py-polars can be installed by executing:
```
pip install pandas==1.0.5
pip install py-polars==0.0.26
```

# Replication code
The source code can be found in [this github repo](https://github.com/atecon/Gretl_pandas_pypolars). For replication on your system, you need to get the csv data file from kaggle, and you should store it in a directory named ```./Gretl_pandas_pypolars/data```.

## Gretl code
The Gretl source code is stored in ```./Gretl/load_and_sort.inp```. Simply run this script file with Gretl.


## Python code
The source code for running the Python stuff can be found in ```./python```. The file ```load_and_sort_with_pandas.py``` executes, as its name says, the stuff using the Pandas library. ```load_and_sort_with_pypolars.py``` does the same using the py-polars library, instead.

### Execute Python code via Gretl
If you want to execute the Python code from inside Gretl using the [```foreign```-block](http://Gretl.sourceforge.net/Gretl-help/cmdref.html#foreign) under Linux, adjust the ~/.Gretl2rc configuration file such that you have the following entry directing to your favorite installed Python (environment). Mine looks like this:
```
python = /home/at/anaconda3/bin/python
```


The same can be done through the GUI menu:
Tool -> Preferences -> General -> Programs

# Results
The following table summarizes the timing of the respective job in seconds:

**Job** |   **Gretl** | **Pandas** | **Py-Polars**
-----------|:-----:|:------:|:---------:
Load csv   | 31.32 | 11.62  | 2.49
Load csv ('obs')    | 11.93 | --  | --
Sort data  | 7.78 | 5.80   | 4.62
Write gbin | 2.41 | --  | --
Load gbin  | 5.76 | --  | --

## Reading csv

Py-polars dominates Pandas by factor of 5 when it comes to reading a csv *and* transforming it into a data frame. Reading and loading the csv as it is takes Gretl abut 32 seconds!

**However**, renaming the 'author' column header to 'obs' allows Gretl to index much quicker which leads to a loading time if 11.93 seconds which is close to that of Pandas.

## Sorting
When it comes to sorting, py-polars still dominates Pandas by about 20 percent. While Pandas needs about 5.8 seconds, latest Gretl version takes 'only' 2 seconds longer to sort this huge data set -- I would say: that's not that bad.


## Comment on Gretl version before 2020f
At the time of writing this, the current developing gretl version is 2020f. If you execute this Gretl script with an older version you will see that sorting this large data set takes at least as twice as long. Allin Cottrell has improved the code on sorting, as [mentioned here](https://gretlml.univpm.it/hyperkitty/list/gretl-users@gretlml.univpm.it/thread/2S62T2T23GMHQL4FKJH7KJHIWIYYPXRH/#V5FATZTNC2ELPUUHWJK4R3MIT7ULWNKD).


# Some comments on Gretl and large data sets
## Do not -- really -- use the gdt/b data format for large data sets
Gretl's default data set is the ```gdt``` data format which is in fact an xml file holding the actual data and some metadata. It is, however, well known that xml is very inefficient when it comes to large data sets. "Libxml2 is having to allocate a ton of memory to parse the entire document.", as Allin Cottrell writes [here](https://Gretlml.univpm.it/hyperkitty/list/Gretl-users@Gretlml.univpm.it/message/V5FATZTNC2ELPUUHWJK4R3MIT7ULWNKD/). Thus, trying to store the data set as gdtb/b file, and opening that file will blow up memory consumption.

Gretl also allows you store this gdt file in a compressed way holding things in the ```gdtb``` file format. Do not try to store the ```users``` data set as gdtb -- the compression takes literally hours.

## New forthcoming feature -- uncompressed binary data set
As a result of this little comparison, leading Gretl developer Allin Cottrell [started to experiment with a new uncompressed binary data set](https://Gretlml.univpm.it/hyperkitty/list/Gretl-users@Gretlml.univpm.it/message/V5FATZTNC2ELPUUHWJK4R3MIT7ULWNKD/). The ```gbin``` data format stores only minimal metadata (variable names, observation markers if present, basic time-series info) but does *currently* not handle string-valued series.

The stored gbin data set as slightly larger with 394 MB compared to the csv 359 MB.

Writing the gbin data file takes only 2.41 seconds (!) on my machine which is amazingly fast.

Reading this almost 400 MB large binary data set takes about 5.7 seconds and hence is twice as fast as reading a csv file with an 'obs' column as described before.

This new data format is really great news. Let's hope that it will also support string-based values at some time.
