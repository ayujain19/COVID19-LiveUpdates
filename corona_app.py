import requests                 #This package is used to get the html data
from bs4 import BeautifulSoup   #This package is used to format the html data in easily understanding form and also used for content scraping.
import plyer
from tkinter import *
from tkinter import messagebox, filedialog
import pandas as pd

def scrap():
    def notifyme(title, message):
        plyer.notification.notify(title=title, message=message, app_icon='corona.ico', timeout=10)


    url = "https://www.worldometers.info/coronavirus/"
    r = requests.get(url)
    # print(r.text)

    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify())
    tablebody = soup.find('tbody')
    # print(tablebody)

    tablerow = tablebody.find_all('tr')

    notifycountry = data.get()  #get the data through entry widget
    if notifycountry == '':
        notifycountry = 'india'

    countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases = [], [], [], [], [], [], []
    serious, totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion = [], [], [], [], []
    headers = ['countries', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases',
               'serious', 'totalcases_permillion', 'totaldeaths_permillion', 'totaltests', 'totaltests_permillion']

    for i in tablerow:
        id = i.find_all('td')
        if id[1].text.strip().lower() == notifycountry:
            totalcases1 = int(id[2].text.strip().replace(',', ''))
            totaldeaths1 = id[4].text.strip()
            newcases1 = id[3].text.strip()
            newdeaths1 = id[5].text.strip()
            notifyme('Corona Virus Details In {}'.format(notifycountry),
                     'Total Cases : {}\nTotal Deaths : {}\nNew Cases : {}\nNew Deaths : {}'.format(totalcases1,
                                                                                                   totaldeaths1,
                                                                                                   newcases1,
                                                                                               newdeaths1))

        countries.append(id[1].text.strip())  # strip is used to remove spaces.
        total_cases.append(int(id[2].text.strip().replace(',', '')))
        new_cases.append(id[3].text.strip())
        total_deaths.append(id[4].text.strip())
        new_deaths.append(id[5].text.strip())
        total_recovered.append(id[6].text.strip())
        active_cases.append(id[7].text.strip())
        serious.append(id[8].text.strip())
        totalcases_permillion.append(id[9].text.strip())
        totaldeaths_permillion.append(id[10].text.strip())
        totaltests.append(id[11].text.strip())
        totaltests_permillion.append(id[12].text.strip())

    df = pd.DataFrame(list(zip(countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases,serious, totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion))
                      ,columns=headers)
    con = df.sort_values('total_cases', ascending=False)
    for k in formatlist:
        if k == 'html':
            path2 = '{}/alldata.html'.format(path)
            con.to_html(r'{}'.format(path2))
        if k == 'json':
            path2 = '{}/alldata.json'.format(path)
            con.to_json(r'{}'.format(path2))
        if k == 'csv':
            path2 = '{}/alldata.csv'.format(path)
            con.to_csv(r'{}'.format(path2))
    if len(formatlist) != 0:
        messagebox.showinfo("Notification", "Corona Record is Successfully Saved at {}".format(path2), parent=root)

def download():
    global path
    if(len(formatlist) != 0):
        path = filedialog.askdirectory()
    else:
        pass
    scrap()
    formatlist.clear()
    htmlbtn.configure(state='normal')
    jsonbtn.configure(state='normal')
    csvbtn.configure(state='normal')


def html():
    formatlist.append('html')
    htmlbtn.configure(state='disabled', bg="white", fg="black")
def json():
    formatlist.append('json')
    jsonbtn.configure(state='disabled',bg="white", fg="black")
def csv():
    formatlist.append('csv')
    csvbtn.configure(state='disabled',bg="white", fg="black")


root = Tk()
root.title("COVID-19")
root.geometry('530x300+500+100')   #To open app at fixed position
root.minsize(530,300)
root.maxsize(530,300)
root.config(bg="yellow")
root.iconbitmap('corona.ico')

formatlist = []
path=''
# ***********************************************Labels*********************
intro = Label(root, text="Corona Virus Information", font=("Verdana", 22, 'italic bold'), bg="yellow")
intro.pack()

label1 = Label(root, text="Notify Country", font=("Verdana", 18,'bold'), bg="yellow", fg="blue")
label1.place(x=10, y=70)

label2 = Label(root, text="Download In :", font=("Verdana", 18,'bold'), bg="yellow", fg="blue")
label2.place(x=10, y=150)

# *****************************************Entry******************
data = StringVar()
entry1 = Entry(root, textvariable=data, font=("Verdana", 15,'bold'), bg="black", fg="white", width=21, relief=RIDGE, bd=3)
entry1.place(x=220, y=70)

# ********************************************Buttons***************

htmlbtn = Button(root, text="HTML", bg="black", fg="white", font=("Verdana", 12,'bold'), relief=RIDGE, bd=3, command=html)
htmlbtn.place(x=220, y=150)

jsonbtn = Button(root, text="JSON", bg="black", fg="white", font=("Verdana", 12,'bold'), relief=RIDGE, bd=3, command=json)
jsonbtn.place(x=320, y=150)

csvbtn = Button(root, text="CSV", bg="black", fg="white", font=("Verdana", 12,'bold'), relief=RIDGE, bd=3, command=csv)
csvbtn.place(x=420, y=150)

submitbtn = Button(root, text="Submit", bg="brown", fg="pink", font=("Verdana", 16,'bold'), relief=RIDGE, bd=3, command=download)
submitbtn.place(x=200, y=250)

root.mainloop()