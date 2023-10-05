import pandas as pd
import wx
import numpy as np
import sqlite3
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
data = pd.read_csv(r'C:\Users\Atticus\Desktop\Crash_Statistics_Victoria.csv', index_col=0)


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(600, 500))

        self.panel = MainPanel(self)


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)