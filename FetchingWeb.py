from bs4 import BeautifulSoup
from lxml import html
import urllib.request
# import requests
import csv
import pyodbc
import pandas as pd


i,j=1,0;
n=[]
fullcontnt=[]
contnt=[]

# Fetching the Webpage.......
content=urllib.request.urlopen("https://www.infoplease.com/homework-help/history/collected-state-union-addresses-us-presidents")
# Using the BeautifulSoup
webpg = BeautifulSoup(content, 'lxml')

#print(webpg.prettify())

print("--------------------------------------------------------------------------------------------------------------------------")

# Searching for all the name of the President and Date Addressed present in the <a> tags in <dt> ....
for link in webpg.find_all('dt'):

    print("Document no:.",i)

    print("Tag:",link)

    href = link.find('a')
    fetchedlink = href.get('href')
    frwdlink = "https://www.infoplease.com" #attaching the prefix to all the incomplete links

    addlink = "".join((frwdlink, fetchedlink))

    print("Href:",addlink)  #final links which would direct us to correct webpage of each President


    presidentpg =urllib.request.urlopen(addlink)
    individpg = BeautifulSoup(presidentpg, 'lxml') #Again using BeautifulSoup to fetch all teh contents from each Presidents Addresses


    name = link.find('a').text   #Searching for <a>tags which contains the addressed text...
    # print("Name and date:", name)

    n.append(name)
    # print("Full name",n)

    fs = name.split("(")   #Separating Name from Date
    print("Name:",fs[0])


    excep = ["Opening Remarks", "Military Sacrifices", "Economic Agenda", "A Hopeful Society"]  #Removing some of the unnecessary links present in the webpage...

    if fs[0] in excep :
        continue


    fs[1] = fs[1].replace(')','')
    print("Date:",fs[1])

    # print(fs[1])

    # Replacing some incorrect links with the proper links to direct us to correct webpages...

    bush = ['February 27, 2001']
    bush_2 = ['January 31, 1990']
    clinton = ['January 27, 2000']
    clinton_2 = ['January 19, 1999']

    if fs[1] in bush :
        addlink = addlink.replace('https://www.infoplease.com', 'https://www.infoplease.com/homework-help/us-documents/state-union-address-george-w-bush-february-27-2001')
        print(addlink)

    if fs[1] in bush_2:
        addlink = addlink.replace('https://www.infoplease.com/t/hist/state-of-the-union/20/node/4985', 'https://www.infoplease.com/homework-help/us-documents/state-union-address-george-w-bush-january-31-1990')
        print(addlink)


    if fs[1] in clinton :
        addlink = addlink.replace('https://www.infoplease.com', 'https://www.infoplease.com/homework-help/us-documents/state-union-address-william-j-clinton-january-27-2000')
        print(addlink)

    if fs[1] in clinton_2:
        addlink = addlink.replace('https://www.infoplease.com/t/hist/s', 'https://www.infoplease.com/homework-help/us-documents/state-union-address-william-j-clinton-january-19-1999')
        print(addlink)

    # Creating text files and inserting content of each President's Addresses...
    path = 'F:/Cleveland State University/Spring 20/Big Data/Assignment 1/InfoUnionAddress_{}.txt'.format(name)
    file = open(path,"a+")


    for pg in individpg.find_all('p'):

        stp = pg.find('img')
        start = pg.find('a')
        if start in pg:
            continue;
        if stp in pg:
            break;

        # print(pg.text)
        full_text = pg.text
        file.write(full_text)

        contnt = full_text
        # print(contnt)

    contnt = ''.join(map(str, contnt))
    #print(contnt)

    fullcontnt = contnt
    print(fullcontnt)

    file.close()


    i=i+1;

    # Opening a CSV file and storing all the info of each file into this CSV file for future usage...

    csv_file = "F:/Cleveland State University/Spring 20/Big Data/Assignment 1/state_union_add.csv"
    with open(csv_file, 'a') as state_file:
        file_writer = csv.writer(state_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        file_writer.writerow([fs[0], fs[1], addlink, path, full_text])

    # Conneccting to the database......
    #
    # conn = pyodbc.connect('Driver={SQL Server};'
    #                   'Server=LAPTOP-65BJT1KQ;'
    #                   'Database=nixdb;'
    #                   'Trusted_Connection=yes;')
    #
    # print("Database Connected")
    #
    # cursor = conn.cursor()
    #
    # cursor.execute('''INSERT INTO nixdb.dbo.StateUnionAddresses(President, [Date of Union Address], [Link to Address], Filename_Address, Text_Address)
    #                     VALUES(?,?,?,?,?)''', fs[0], fs[1], addlink, path, full_text)
    #
    #
    # cursor.close()
    #
    # conn.commit()
    #
    # conn.close()

    print("Data inserted")

    # Creating a big text file for inserting all President's data into a single file with President name and date.....
    #
    # bigfile = 'F:/Cleveland State University/Spring 19/Big Data/Assignment 3 Due 4/Website/AllPresidentAddresses.txt'
    # bigf = open(bigfile,"a+")
    #
    # bigf.write(name)
    # bigf.write("\n")
    #
    # for pg in individpg.find_all('p'):
    #
    #     stp = pg.find('img')
    #     start = pg.find('a')
    #     if start in pg:
    #         continue;
    #     if stp in pg:
    #         break;
    #
    #     # print(pg.text)
    #     fulltxt = pg.text
    #     bigf.write(fulltxt)
    #
    #
    # bigf.write("\n")
    #
    # bigf.close()
    #

#
# names,dates,links,filepths,txts=[500],[],[],[],[]
#
#
#
#
# with open(csv_file, 'r') as union_file:
#     readCSV = csv.reader(union_file, delimiter=',')
#     for row in readCSV:
#         name=row[0]
#         date=row[1]
#         link=row[2]
#         filepth=row[3]
#         txt=row[4]
#
#         names.append(name)
#         dates.append(date)
#         links.append(link)
#         filepths.append(filepth)
#         txts.append(txt)
#
#     print(names)
