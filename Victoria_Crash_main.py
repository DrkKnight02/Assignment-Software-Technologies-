import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import wx 

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
data = pd.read_csv("Crash_Statistics_Victoria.csv",index_col=0)

