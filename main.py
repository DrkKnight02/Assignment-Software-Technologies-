import pandas as pd
import wx
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


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)

        font = wx.Font(10, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=False, faceName="")

        self.label = wx.StaticText(self, label="Select Periods:", pos=(40, 0))
        self.label = wx.StaticText(self, label="Date From:", pos=(5, 20))
        self.label = wx.StaticText(self, label="Date To:", pos=(105, 20))
        self.label = wx.StaticText(self, label="Alcohol Influence", pos=(170, 0))
        self.label = wx.StaticText(self, label="Yes:", pos=(190, 20))
        self.label = wx.StaticText(self, label="No:", pos=(230, 20))
        self.cb = wx.CheckBox(self, label="", pos=(205, 45))
        self.cb = wx.CheckBox(self, label="", pos=(235, 45))
        self.label = wx.StaticText(self, label="Casuality Amount", pos=(300, 0))
        choices = choices = ['1', '2', '3', '4', '5', 'Over 6']
        self.combobox = wx.ComboBox(self, choices=choices, pos=(315, 40), size=(75, 25))
        self.label = wx.StaticText(self, label="Keword Descripition", pos=(420, 0))
        choices = ['speeding', 'alcohol', 'collision', 'distraction', 'other']
        self.combobox = wx.ComboBox(self, choices=choices, pos=(425, 40))
        self.btn = wx.Button(self, label="Go", pos=(540, 10), size=(50, 50))
        #self.label = wx.StaticText(self, label="Generate", pos=(530, 70))
        self.label = wx.StaticText(self, label="Generate Graph", pos=(500, 90))
        #self.label = wx.StaticText(self, label="Generate", pos=(530, 160))
        self.label = wx.StaticText(self, label="Generate Table", pos=(500, 180))
        #self.label = wx.StaticText(self, label="Export", pos=(540, 250))
        self.label = wx.StaticText(self, label="Export Data", pos=(500, 270))
        self.label = wx.StaticText(self, label=".", pos=(300, 250))
        self.text = wx.TextCtrl(self, pos=(4, 40), size=(60, 25))
        self.text = wx.TextCtrl(self, pos=(100, 40), size=(60, 25))
        self.btn = wx.Button(self, label="Go", pos=(540, 290), size=(35, 35))
        choices2 = ['Line graph', 'area graph', 'Pictograph', 'Bar graph', 'Histogram']
        self.combobox = wx.ComboBox(self, choices=choices2, pos=(490, 110))
        choices3 = ['Binary table', 'Pie chart', 'Frequency table', 'Plot', 'Grid']
        self.combobox = wx.ComboBox(self, choices=choices3, pos=(465, 200))
        self.label.SetFont(font)
        self.SetSize(10, 10)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(parent=None, title="Victorian Crash Analysis Tool")
        self.frame.Show()
        return True


app = MyApp()
app.MainLoop()

connection = sqlite3.connect("x.db")
cursor = connection.cursor()
data["ACCIDENT_DATE"] = pd.to_datetime(data["ACCIDENT_DATE"], format='%d/%m/%Y')
data["ACCIDENT_TIME"] = pd.to_datetime(data["ACCIDENT_TIME"], format='%H.%M.%S')

print("To select Time Period enter 'Filter by date' or '1'")
print("To select a keyword enter 'Keyword' or '2'")
print("To toggle hit and run entries off enter 'Hit and run' or '3'")
print("To show filtered data enter 'Display' or '4'")
print("To clear all filters enter 'Clear' or '5'")
print("To view accidents per hour on average enter 'Hourly' or '6'")
print("To view the percentage of accidents involving alcohol enter 'Alcohol' or '7'")
print("To quit enter 'Quit'")
com = input("Enter a command (Commands are case sensitive) ")
startDate = '01/06/2013'
endDate = '03/02/2019'
kWord = 0
hitAndRun = True
houra = {}
xax = {}

while com != 'Quit':

    if com == 'Filter by date' or com == '1':
        startDate = input("Enter the start date as dd/mm/yyyy ")
        endDate = input("Enter the end date as dd/mm/yyyy ")
    elif com == 'Keyword' or com == '2':
        kWord = input("Enter a keyword to filter by ")
    elif com == 'Hit and run' or com == '3':
        hitAndRun = False
    elif com == 'Display' or com == '4':
        if kWord != 0:
            if hitAndRun == False:
                harFilter = data["HIT_RUN_FLAG"].str.contains('No')
                dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
                wordFilter = data["ACCIDENT_TYPE"].str.contains(kWord)
                dataFiltered = data[dateFilter & wordFilter & harFilter]
                print(dataFiltered)
            else:
                dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
                wordFilter = data["ACCIDENT_TYPE"].str.contains(kWord)
                dataFiltered = data[dateFilter & wordFilter]
                print(dataFiltered)
        else:
            if hitAndRun == False:
                harFilter = data["HIT_RUN_FLAG"].str.contains('No')
                dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
                dataFiltered = data[dateFilter & harFilter]
                print(dataFiltered)
            else:
                dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
                print(data.loc[dateFilter])
    elif com == 'Clear' or com == '5':
        startDate = '01/06/2013'
        endDate = '03/02/2019'
        kWord = 0
        hitAndRun = True
    elif com == 'Hourly' or com == '6':
        dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
        dataFiltered = data[dateFilter]
        diff = pd.to_datetime(endDate, format='%d/%m/%Y') - pd.to_datetime(startDate, format='%d/%m/%Y')
        for i in range(23):
            houra[i] = diff.days / (len(dataFiltered[(dataFiltered['ACCIDENT_TIME'] >=
                                                      pd.to_datetime([f'{i}.00.00'], format='%H.%M.%S')[0]) & (
                                                                 dataFiltered['ACCIDENT_TIME'] <
                                                                 pd.to_datetime([f'{(i + 1)}.00.00'],
                                                                                format='%H.%M.%S')[0])]))
            xax[i] = f'{i}-{(i + 1)}'
            i += 1
        houra[23] = diff.days / (
            len(dataFiltered[(dataFiltered['ACCIDENT_TIME'] >= pd.to_datetime([f'23.00.00'], format='%H.%M.%S')[0])]))
        xax[23] = f'23-24'
        x = np.array(
            [houra[0], houra[1], houra[2], houra[3], houra[4], houra[5], houra[6], houra[7], houra[8], houra[9],
             houra[10], houra[11], houra[12], houra[13], houra[14], houra[15], houra[16], houra[17], houra[18],
             houra[19], houra[20], houra[21], houra[22], houra[23]])
        y = np.array(
            [xax[0], xax[1], xax[2], xax[3], xax[4], xax[5], xax[6], xax[7], xax[8], xax[9], xax[10], xax[11], xax[12],
             xax[13], xax[14], xax[15], xax[16], xax[17], xax[18], xax[19], xax[20], xax[21], xax[22], xax[23]])
        plt.bar(y, x)
        plt.show()
    elif com == 'Alcohol' or com == '7':
        dateFilter = (data["ACCIDENT_DATE"] >= startDate) & (data["ACCIDENT_DATE"] <= endDate)
        dataFiltered = data[dateFilter]
        alye = np.sum(dataFiltered['ALCOHOLTIME'] == 'Yes')
        alno = np.sum(dataFiltered['ALCOHOLTIME'] == 'No')
        tot = alno + alye
        perye = (tot / alye) * 100
        perno = (tot / alno) * 100
        alpi = np.array([perye, perno])
        mylabels = ["Yes", "No"]
        plt.pie(alpi, labels=mylabels)
        plt.show()
    else:
        print("Bad command")
    com = input("Enter a command ")

print("Thank you.")

# objectidover = data[data["ACCIDENT_DATE"] < "2/7/2013"]

# print(objectidover)
