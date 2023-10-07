import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import wx

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
data = pd.read_csv("Crash_Statistics_Victoria.csv", index_col=0)

import wx


class TheFrame(wx.Frame):
    def __init__(self, parent, title):
        super(TheFrame, self).__init__(parent, title=title, size=(600, 500))

        self.panel = ThePanel(self)


class ThePanel(wx.Panel):
    def __init__(self, parent):
        super(ThePanel, self).__init__(parent)

        font = wx.Font(10, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=False, faceName="")

        self.label = wx.StaticText(self, label="Filter by date:", pos=(50, 0))
        self.label = wx.StaticText(self, label="From:", pos=(5, 20))
        self.label = wx.StaticText(self, label="To:", pos=(105, 20))
        self.label = wx.StaticText(self, label="To:", pos=(105, 20))
        self.label = wx.StaticText(self, label="Include", pos=(225, 0))
        self.label = wx.StaticText(self, label="Hit + Run", pos=(218, 15))
        self.label = wx.StaticText(self, label="Incidents", pos=(220, 30))
        self.label = wx.StaticText(self, label="Filter by Description", pos=(350, 0))
        self.label = wx.StaticText(self, label="Keyword Search:", pos=(310, 20))
        self.label = wx.StaticText(self, label="Cause Filter:", pos=(450, 20))
        self.label = wx.StaticText(self, label="Generate", pos=(530, 70))
        self.label = wx.StaticText(self, label="Graph", pos=(540, 90))
        self.label = wx.StaticText(self, label="Generate", pos=(530, 160))
        self.label = wx.StaticText(self, label="Table", pos=(540, 180))
        self.label = wx.StaticText(self, label="Export", pos=(540, 250))
        self.label = wx.StaticText(self, label="Results", pos=(540, 270))
        self.label = wx.StaticText(self, label=".", pos=(300, 250))
        self.text = wx.TextCtrl(self, pos=(4, 40), size=(60, 25))
        self.text = wx.TextCtrl(self, pos=(100, 40), size=(60, 25))
        self.text = wx.TextCtrl(self, pos=(315, 40), size=(75, 25))
        self.btn = wx.Button(self, label="Go", pos=(540, 10), size=(35, 35))
        self.btn = wx.Button(self, label="Go", pos=(540, 290), size=(35, 35))
        self.cb = wx.CheckBox(self, label="", pos=(235, 45))
        choices = ['speeding', 'alcohol', 'collision', 'distraction', 'other']
        self.combobox = wx.ComboBox(self, choices=choices, pos=(425, 40))
        choices2 = ['Line graph', 'area graph', 'Pictograph', 'Bar graph', 'Histogram']
        self.combobox = wx.ComboBox(self, choices=choices2, pos=(490, 110))
        choices3 = ['Binary table', 'Pie chart', 'Frequency table', 'Plot', 'Grid']
        self.combobox = wx.ComboBox(self, choices=choices3, pos=(465, 200))
        self.label.SetFont(font)
        self.SetSize(10, 10)

