import pandas as pd
import wx
import numpy as np
import sqlite3
import numpy as np
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
data = pd.read_csv("Crash_Statistics_Victoria.csv", index_col=0)


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(600, 500))

        self.panel = MainPanel(self)

self.panel = MainPanel(self)
self.SetBackgroundColour('light blue')

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)
        font = wx.Font(10, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD, underline=False, faceName="Comic Sans MS")
        dark_grey = wx.Colour(70, 70, 70)
        self.label = wx.StaticText(self, label = "Select Periods:", pos=(40, 0))
        self.label = wx.StaticText(self, label = "Date From:", pos=(5, 20))
        self.label = wx.StaticText(self, label = "Date To:", pos=(105, 20))
        self.label = wx.StaticText(self, label = "Alcohol Influence", pos=(170, 0))
        self.label = wx.StaticText(self, label = "Yes:", pos=(190, 20))
        self.label = wx.StaticText(self, label = "No:", pos=(230, 20))
        self.cb = wx.CheckBox(self, label= "", pos=(205, 45))
        self.cb = wx.CheckBox(self, label= "", pos=(235, 45))
        self.label = wx.StaticText(self, label="Hit and Run", pos=(300, 0))
        choices = choices = ['Yes', 'No']
        self.combobox = wx.ComboBox(self, choices=choices, pos=(315, 40), size=(75, 25))
        self.label = wx.StaticText(self, label="Keyword Description", pos=(420, 0))
        choices = ['speeding', 'alcohol', 'collision', 'distraction', 'other']
        self.combobox = wx.ComboBox(self, choices=choices, pos=(425, 40))
        self.btn = wx.Button(self, label="Apply/Reset", pos=(540, 10), size=(100, 50))
        self.label = wx.StaticText(self, label="Generate Graph", pos=(500, 90))
        self.label = wx.StaticText(self, label="Generate Table", pos=(500, 180))
        self.label = wx.StaticText(self, label="Export Data", pos=(500, 270))
        self.label = wx.StaticText(self, label=".", pos=(300, 250))
        self.text = wx.TextCtrl(self, pos=(4, 40), size=(60, 25))
        self.text = wx.TextCtrl(self, pos=(100, 40), size=(60, 25))
        self.btn = wx.Button(self, label="Go", pos=(540, 290), size=(35, 35))
        choices2 = ['Line graph', 'area graph', 'Pictograph', 'Bar graph']
        self.combobox = wx.ComboBox(self, choices=choices2, pos=(490, 110))
        choices3 = ['Binary table', 'Pie chart', 'Frequency table']
        self.combobox = wx.ComboBox(self, choices=choices3, pos=(465, 200))
        self.label.SetFont(font)
        self.SetSize(10, 10)


class MainApplication(wx.App):
    def oninit(self):
        self.frame = MainFrame(parent=None, title="Victorian Crash Analysis Tool")
        self.frame.Show()
        return True


app = MainApplication()
app.MainLoop()

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
data["ACCIDENT_DATE"] = pd.to_datetime(data["ACCIDENT_DATE"], format='%d/%m/%Y')
data["ACCIDENT_TIME"] = pd.to_datetime(data["ACCIDENT_TIME"], format='%H.%M.%S')

print("To select Time Period type 'Filter by date' or '1'")
print("To select a keyword type 'Keyword' or '2'")
print("To toggle hit and run entries off type 'Hit and run' or '3'")
print("To show filtered results type 'Display' or '4'")
print("To clear all filters type 'Clear' or '5'")
print("To view accidents per hour on average type 'Hourly' or '6'")
print("To view the percentage of accidents involving alcohol type 'Alcohol' or '7'")
print("To Exit type 'Exit'")
com = input("type a command (Commands are case sensitive) ")
startDate = '01/06/2013'
endDate = '03/02/2019'
keyWord = 0
hitAndRun = True
timings_hr = {}
axis = {}

while com != 'Exit':

    if com == 'Filter by date' or com == '1':
        startDate = input("Enter the time period as dd/mm/yyyy ")
        endDate = input("Enter the end period as dd/mm/yyyy ")
    elif com == 'Keyword' or com == '2':
        keyWord = input("Select a keyword ")
    elif com == 'Hit and run' or com == '3':
        hitAndRun = False
    elif com == 'Display' or com == '4':
        if keyWord != 0:
            if not hitAndRun:
                hitAndRunFilter = data["HIT_RUN_FLAG"].str.contains('No')
                dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
                wordFilter = data["ACCIDENT_TYPE"].str.contains(keyWord)
                dataFiltered = data[dateFilter & wordFilter & hitAndRunFilter]
                print(dataFiltered)
            else:
                dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
                wordFilter = data["ACCIDENT_TYPE"].str.contains(keyWord)
                dataFiltered = data[dateFilter & wordFilter]
                print(dataFiltered)
        else:
            if not hitAndRun:
                hitAndRunFilter = data["HIT_RUN_FLAG"].str.contains('No')
                dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
                dataFiltered = data[dateFilter & hitAndRunFilter]
                print(dataFiltered)
            else:
                dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
                print(data.loc[dateFilter])
    elif com == 'Clear' or com == '5':
        startDate = '01/06/2013'
        endDate = '03/02/2019'
        keyWord = 0
        hitAndRun = True
    elif com == 'Hourly' or com == '6':
        dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
        dataFiltered = data[dateFilter]
        diff = pd.to_datetime(endDate, format='%d/%m/%Y') - pd.to_datetime(startDate, format='%d/%m/%Y')
        for i in range(23):
            timings_hr[i] = diff.days / (len(dataFiltered[(dataFiltered['ACCIDENT_TIME'] >=
                                                           pd.to_datetime([f'{i}.00.00'], format='%H.%M.%S')[0]) & (
                                                                  dataFiltered['ACCIDENT_TIME'] <
                                                                  pd.to_datetime([f'{(i + 1)}.00.00'],
                                                                                 format='%H.%M.%S')[0])]))
            xaxis[i] = f'{i}-{(i + 1)}'
            i += 1
            timings_hr[23] = diff.days / (
                len(dataFiltered[
                        (dataFiltered['ACCIDENT_TIME'] >= pd.to_datetime([f'23.00.00'], format='%H.%M.%S')[0])]))
            xaxis[23] = f'23-24'
            x = np.array(
                [timings_hr[0], timings_hr[1], timings_hr[2], timings_hr[3], timings_hr[4], timings_hr[5],
                 timings_hr[6],
                 timings_hr[7], timings_hr[8], timings_hr[9], timings_hr[10], timings_hr[11], timings_hr[12],
                 timings_hr[13],
                 timings_hr[14], timings_hr[15], timings_hr[16], timings_hr[17], timings_hr[18], timings_hr[19],
                 timings_hr[20],
                 timings_hr[21], timings_hr[22], timings_hr[23]])

        y = np.array(
            [xaxis[0], xaxis[1], xaxis[2], xaxis[3], xaxis[4], xaxis[5], xaxis[6], xaxis[7], xaxis[8], xaxis[9], xaxis[10], xaxis[11], xaxis[12],
             xaxis[13], xaxis[14], xaxis[15], xaxis[16], xaxis[17], xaxis[18], xaxis[19], xaxis[20], xaxis[21], xaxis[22], xaxis[23]])
        plt.bar(y, x)
        plt.show()

    elif com == 'Alcohol' or com == '7':
        dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
        dataFiltered = data[dateFilter]
        alcohol_positive = np.sum(dataFiltered['ALCOHOLTIME'] == 'Yes')
        alcohol_no = np.sum(dataFiltered['ALCOHOLTIME'] == 'No')
        total = alcohol_no + alcohol_positive
        percent_yes = (total / alcohol_positive) * 100
        percent_no = (total / alcohol_no) * 100
        alpi = np.array([percent_yes, percent_no])
        mylabels = ["Yes", "No"]
        plt.pie(alpi, labels=mylabels)
        plt.show()
    else:
        print("Invalid Command")
    com = input("Type a command ")

print("Hope you enjoyed")
