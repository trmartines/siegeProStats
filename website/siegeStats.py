# -*- coding: utf-8 -*-
"""
Created on Thu May  6 17:31:18 2021

@author: tyler
"""
import requests
from bs4 import BeautifulSoup
from flask import Flask 
from flask import request 
import pandas as pd
#get the map bans into text form and into 2d array
def getMapScores(soup):
    #basic bs4 code to give the rest of the function ability to see the shittily written html 1/?
    games=soup.find('div',class_='col-12 col-lg-9')
    gamecount=games.find('ol')
    mapnum = gamecount.findAll(class_=("game"))
    #intitialize all the vars outside of the for loops so thier is also updated outside
    #instead of just inside the for loops
    winningTeam=[]
    sidescoreF=[]
    score=[]
    winningTeamName=[]
    mapWon=[]
    #below iterates for each occurence of li in mapnum and creates a set of arrays that can be put
    #into a nice compact dataframe and then sent to the function that groups all the dataframes
    for li in mapnum:
       winningTeamName.append(li.find('span',class_='game__text__team').text)
       mapWon.append(li.find('span',class_='game__text__won').text)
       score.append(li.find('span',class_='game__text__score').text)
       sidescorecon=li.find('div',class_='game__rounds-w fs-xs pt-3')
       sidescore = sidescorecon.find_all('div')
       #iterate for each team and store thier sidescores at the end of the iterations
       for x in range(2):
           sidescore[x]=sidescore[x].text
           if x ==1:
               sidescoreF.append(sidescore)
    data=[winningTeam,sidescoreF,score,winningTeamName,mapWon] 
    df=pd.DataFrame(data)  
    return df    
def getMapBans(soup):
    #like who writes HTML and doesnt use ids? like im a shitty programmer and even i use ids 2/?
    banContainer = soup.find('div', class_='row row--padded match__bans')
    mapBansCon = banContainer.find('tbody')
    mapBanRows = mapBansCon.find_all('tr')
    #initialize vars outside of loops again
    mapBans=[]
    z=0
    for tr in mapBanRows:
    #probably a better way to do this but z makes a jank counter for number of trs in mapBanRows
    #also gives me the ability to put the teams on the top of the bans so you can see who banned what
        z=z+1
    for x in range(z+1):
        #use counter to turn the range here into a variable that can change depending on match
        #only used to work with a modified map pool/older map pool but seems to still be broke
        #for other reasons (FIX RETARD. YEA YOU)
        if x==0:
            mapBans.append(getTeams(soup))
        #this if else sets the top row of the map bans as the team names. 
        else:
            mapBans.append(mapBanRows[x-1].find_all('td'))
    for x in range (z+1):  
       for y in range(3):
           if x>0:
               mapBans[x][y] = mapBans[x][y].text
    return mapBans
def getOpBans(soup):
    #its just the right thing to do for reasons like this. im trying to scrape data and i need
    #a bunch of extra lines so i can point to some generic div nested inside 100 other divs 3/?
    opBanCon = soup.find('ol',class_='ban__ops__list list-group list-group-flush')
    opBans = opBanCon.find_all('li')
    for x in range(4):
        opBans[x]=opBans[x].text
    df=pd.DataFrame(opBans)
    df=df[0].str.replace(' banned','')
    return df
#get all the stats into text form and in 2d array
def getStats(soup):
    #worst part is the lack of class names on some of this shit. instead of just using classes use
    #ids AND classes so you can properly label shit. like how does the bot that writes this work? 4/?
    statsTable = soup.find("table", class_="table table-sm table-hover table--stats table--player-stats js-dt--player-stats js-heatmap w-100")
    tbody = statsTable.find("tbody")
    players_list = tbody.find_all("tr")
    #initialize vars outside of loops again
    stats=[]
    #this for loop does the same thing as the others and gets the stats all in text form 
    for x in range(10):
        stats.append(players_list[x].find_all('td'))
    for x in range(10):
        for y in range(13):
            stats[x][y]=stats[x][y].text
    return stats
def getTeams(soup):
    #tiny method that gets the team names and puts them into an array formatted so it can go at the
    #top of the map bans and label who banned what
     teamA = soup.find('th', class_='team--a px-0')
     teamB = soup.find('th', class_='team--b px-0')
     teams=[teamA.text,' ',teamB.text]
     return teams 
def getUrl():
    #this method sets the page that stats are being taken from. very basic but backbone of program
   url=input('input siege.gg url: ')
   #url ='https://siege.gg/matches/5363-nal-na-beastcoast-vs-soniqs'
   page = requests.get(url).text
   soup = BeautifulSoup(page, 'lxml')
   return soup
def createFinalDF(site): 
    #creates the DF that updates the CSV and is shown in the terminal. ez enough
    fScores = pd.DataFrame(getMapScores(site))
    fBans = pd.DataFrame(getOpBans(site))
    fMapBans = pd.DataFrame(getMapBans(site))
    fStats = pd.DataFrame(getStats(site))
    finalDFDis=pd.concat([fStats,fMapBans,fBans,fScores],axis=1)
    print(finalDFDis)
    return finalDFDis
def runAgain(site,fdf,csvName):
    #method that organizes thibngs if you want to add another match to the sheet. changes csv not url
    #seems to be broken of you want to mix match formats (b05/b03/b01/b02) not sure why.
    #has something to do with the (scale?) and the fact that append is just concat in disguise
    #not too sure but need to fix if i want to make this a thing.
    fstats.append(getStats(site))
    fMBans.append(getMapBans(site))
    seperator=[[]*10]
    sdf=pd.DataFrame(seperator)
    fdf=fdf.append(sdf)
    fdf=fdf.append(createFinalDF(site))
    fdf.to_csv(csvName)
    print(fdf)
    againQ(site, fdf,csvName)
def newSheet(url,csvName):
    #this function runs on startup of the program and when user deciudes to create a new sheet
    #it simply gets a new url and changes the name of the csv you are saving to
    fdf=createFinalDF(url)
    fdf.to_csv(csvName)
    print('you cannot mix and match set types ex. b01/b02/b03/b05 dont try or you will break your spreadsheet. create a new sheet to work with other set types')
    againQ(url,fdf,csvName)
    return url
def againQ(soup,fdf,csvName):
    if input('add more matches to current sheet?(y/n): ') =='y':
        runAgain(getUrl(),fdf,csvName)
    else:
        if input('Would you like to create another sheet?(y/n): ')=='y':
            newSheet(getUrl(),getcsvName())
def getcsvName():
    name=input("input name for csv to save under (filename.csv): ")
    return name
fstats=[]
fMBans=[]
print("SiegeStats Made by Tyler9x 5/2/2021. Enjoy. Give Feedback to Tyler9x 9848 on discord. v0.4.1 To close program exit terminal.")
print("Instructions:")
print(" 1. Enter the full url of the siegegg page you want stats from")
print(" 2. Enter the name that you want the spreadsheet to save as INCLUDE .csv")
print(" 3. Choose option to either add another match to current sheet or create a new sheet")
print(" 4. repeat")
site=newSheet(getUrl(),getcsvName())

#i guarantee the bot that writes these sites doesnt have any comments. like atleast i comment. my
#spaghetti code isnt even that bad but damn siegegg get yourself better programmers.
#
#Special Shoutout to stackoverflow,pandas documentation and the countless sites that explain bs4
#the bs4 documentation is horrible and pretty much useless compared to the random sites that
#explain it. i think i can say im ok at python now too. thats pretty cool :)

#112315431986374952626173











