# -*- coding:utf-8 -*
import pandas as pd
from numpy import nan as NA
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from pandas.io.parsers import TextFileReader
import json
import requests
import seaborn as sns

df = pd.DataFrame(np.arange(25).reshape(5,5),
                       columns=['a', 'b', 'c', 'd', 'e'],
                       index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])

print(df)