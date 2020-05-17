from tkinter import *
# importing libraries
import os
import numpy as np
import requests  # for fetching
from bs4 import BeautifulSoup
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# extracting data from website
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
URL = 'https://www.mohfw.gov.in/'

SHORT_HEADERS = ['SNo', 'State/UT', 'Confirmed',
                 'Cured', 'Death']

response = requests.get(URL).content
#Parsing the data
soup = BeautifulSoup(response, 'html.parser')
header = extract_contents(soup.tr.find_all('th'))

stats = []
all_rows = soup.find_all('tr')

for row in all_rows:
    stat = extract_contents(row.find_all('td'))
    if stat:
        if len(stat) == 4:
            # last row
            stat = ['', *stat]
            stats.append(stat)
        elif len(stat) == 5:
            stats.append(stat)
# cleaning the data
stats[-1][1] = "Total Cases"
stats.remove(stats[-1])
flat_list=[]
flat_list.extend(SHORT_HEADERS)
def flatten(stats):
    for x in stats:
        if(type(x) is list):
            flatten(x)
        else:
            flat_list.append(x)
flatten(stats)
s=flat_list.index("Andaman and Nicobar Islands")
flat_list[s]="A & N Islands"


"""
# Tabulating the data
def coronaTable():
    
    table = tabulate(stats, headers=SHORT_HEADERS, tablefmt="pipe")
    print(table)
    
"""

# Create csv file
my_df = pd.DataFrame(stats)
my_df.to_csv('output.csv', index=False, header=['SNo', 'State/UT', 'Confirmed', 'Cured', 'Death'])


# India Covid-19 Cases State-wise
def totalGraph():
    stats.sort(key=lambda x: int(x[2]))
    stats.reverse()

    objects = []
    for row in stats:
        objects.append(row[1])
    y_pos = np.arange(len(objects))

    performance = []
    for row in stats:
        performance.append(int(row[2]))

    sum_cases = sum(performance)
    # print(sum_cases)

    # Common features for all graphs
    fig, ax = plt.subplots(figsize=(15, 8))
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    # Remove x,y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    # # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)
    # Add x,y gridlines
    ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
    # Show top values
    ax.invert_yaxis()
    for i in ax.patches:
        ax.text(i.get_width() + 500, i.get_y() + 0.5, str(round((i.get_width()), 2)),
                fontsize=10, fontweight='bold', color='grey')

    ax.barh(y_pos, performance, align='center', alpha=0.45,
            color='blue',
            )

    ax.set_title('India Covid-19 Cases' + '                ' + 'Total Cases = {}'.format(sum_cases),
                 loc='center', pad=3)

    plt.xlim(0, 1200)
    plt.xlabel('Number of Confirmed Cases')
    plt.yticks(y_pos, objects)
    plt.tight_layout()
    plt.show()


# India Covid-19 Deaths State-wise
def deathGraph():
    # 2. India Deaths
    stats.sort(key=lambda x: int(x[4]))
    stats.reverse()
    objects = []
    for row in stats:
        objects.append(row[1])
    y_pos = np.arange(len(objects))

    death = []
    for row in stats:
        death.append(int(row[4]))

    sum_deaths = sum(death)
    # Common features for all graphs
    fig, ax = plt.subplots(figsize=(15, 8))
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    # Remove x,y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    # # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)
    # Add x,y gridlines
    ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
    # Show top values
    ax.invert_yaxis()
    for i in ax.patches:
        ax.text(i.get_width() + 500, i.get_y() + 0.5, str(round((i.get_width()), 2)),
                fontsize=10, fontweight='bold', color='grey')

    ax.barh(y_pos, death, align='center', alpha=0.8,
            color='crimson')
    ax.set_title('India Covid-19 Deaths' + '                ' + 'Total Cases = {}'.format(sum_deaths),
                 loc='center', pad=5)

    plt.xlim(0, 70)
    plt.xlabel('No. of Deaths')

    plt.yticks(y_pos, objects)
    plt.tight_layout()

    plt.show()


# India Covid-19 Cured cases State-wise
def curedGraph():
    # 3. India Cured

    stats.sort(key=lambda x: int(x[3]))
    stats.reverse()

    objects = []
    for row in stats:
        objects.append(row[1])
    y_pos = np.arange(len(objects))

    cured = []
    for row in stats:
        cured.append(int(row[3]))

    sum_cured = sum(cured)

    # Common features for all graphs
    fig, ax = plt.subplots(figsize=(15, 8))
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    # Remove x,y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    # # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)
    # Add x,y gridlines
    ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
    # Show top values
    ax.invert_yaxis()
    for i in ax.patches:
        ax.text(i.get_width() + 500, i.get_y() + 0.5, str(round((i.get_width()), 2)),
                fontsize=10, fontweight='bold', color='grey')

    ax.barh(y_pos, cured, align='center', alpha=0.8,
            color='#2c786c')

    ax.set_title('India Covid-19 Cured' + '                ' + 'Total Cases = {}'.format(sum_cured),
                 loc='center', pad=5)

    plt.xlim(0, 90)
    plt.xlabel('No. of People Cured')

    plt.yticks(y_pos, objects)
    plt.tight_layout()
    plt.show()

#Creating GUI 
root=Tk()
class Covid_19:
    def __init__(self,root):
        self.root=root
        self.root.title("Covid-19 Updates")
        self.homepage()

    def homepage(self):
        self.frame = Frame(root, bg="#e6f7ff", height=450, width=700)
        self.frame.pack()
        self.frame.pack_propagate(0)
        img=PhotoImage(file='')
        font1=('Times',18,'bold underline')
        font2=("Times",14,"bold")
        l=Label(self.frame, text="COVID-19 INDIA STATEWISE LIVE UPDATES",width=60,font=font1,bg="white",fg="#005580")
        l.pack(padx=10,pady=40)
        b=Button(self.frame, text="Statewise Table of Covid-19",command=lambda: self.coronaTable(), width=50,bg="white",font=font2,fg="#005580")
        b.pack(padx=10, pady=10)
        b = Button(self.frame, text="India Covid-19 graph", command=totalGraph, width=50,bg="white",font=font2,fg="#005580")
        b.pack(padx=10, pady=10)
        b = Button(self.frame, text="India Covid-19 Death Graph", command=deathGraph, width=50,bg="white",font=font2,fg="#005580")
        b.pack(padx=10, pady=10)
        b = Button(self.frame, text="India Covid-19 Cured Graph", command=curedGraph, width=50, bg="white",font=font2,fg="#005580")
        b.pack(padx=10, pady=10)
        footer=Label(self.frame, text="Source: Ministry of Health and Family Welfare of India")
        footer.pack(side=BOTTOM,fill="x")

    def coronaTable(self):
        self.temp_root=Toplevel()
        self.temp_frame=Frame(self.temp_root,height=1700,width=780,bg="#e6f7ff")
        self.temp_frame.pack()
        self.temp_frame.pack_propagate(0)
        self.lab = Label(self.temp_frame, width=50, text="Statewise Table of Covid-19",bg="white")
        self.lab.grid(row=0, column=1, columnspan=3, padx=10,pady=10)

        self.data=flat_list
        self.text1 = []
        r = 1
        c = 0
        for val in self.data:
            b = Label(self.temp_frame, width=20,text=val,bg="white")
            b.grid(row=r, column=c, padx=6, pady=1)
            b.grid_propagate(0)
            self.text1.append(b)
            c += 1
            if c == 5:
                r += 1
                c = 0


c=Covid_19(root)
root.mainloop()
