from bs4 import BeautifulSoup
import requests
import threading

finalteamnames = []

#Getting Team Names 
def getTeamNames(ramen,finalteamnames):

	teamNames =[]
	for tname in ramen.find_all('h2'):
		teamNames.append(tname.get_text())
	global team1
	global team2
	team1=teamNames[0]
	team2=teamNames[1]
	finalteamnames.append(team1)
	finalteamnames.append(team2)

# Thread for getting team data
def getTeamLink(ramen):

	global link
	link=[]
	element =ramen.select('a.name')
	for team in element:
		link.append(team.get('href'))

finalteamdata=[]
def getTeamData(link,finalteamdata):
	global rating,worldrank,earnings,winrate	

	URL="https://www.gosugamers.net"+link
	headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'}
	page=requests.get(URL,headers=headers)
	noodles = BeautifulSoup(page.content, 'html.parser')
	
	data=[]
	for i in noodles.select('div.row.text-right'):
		data.append(i.getText())
	
	splitted=[]
	splitted=(data[1].split('\n'))
	
	x = [str for str in splitted if str]
	
	rating=x[1].replace(" ","")
	rating=rating.replace(",","")
	worldrank=x[4].replace(" ","")
	worldrank=worldrank.replace(",","")
	earnings=x[7].replace(" ","")
	earnings=earnings.replace(",","")
	if earnings=="-":
		earnings="0"
	winrate=x[10].replace(" ","")
	winrate=winrate.replace(",","")
	if winrate=="-":
		winrate="0"

	finalteamdata.append(rating)
	finalteamdata.append(worldrank)
	finalteamdata.append(earnings)
	finalteamdata.append(winrate)

	


def getPlayerLink(ramen):
	
	global playerlistslink
	playerlinks=[]

	for plinks in ramen.select("a.player"):
		playerlinks.append(plinks.get('href'))

	playerlistslink=[]
	print(playerlinks)

	[playerlistslink.append(x) for x in playerlinks if x not in playerlistslink]

	
		


finalplayernames=[]
	
def getPlayerName(ramen,finalplayernames):
	global players
	players=[]
	player=[]

	for pname in ramen.select("div[class=name]"):
		player.append(pname.getText())
	
	for p in player:
		pl=p.replace(" ","")
		pl=pl.replace("\n","")
		players.append(pl)
	newplayers=[]
	for pl in players:
		newplayers.append(pl)


	[finalplayernames.append(x) for x in newplayers if x not in finalplayernames]
	


finalplayerdata=[]


def getPlayerData(links,finalplayerdata):
	global prating,pworldrank,pearnings,pwinrate	

	URL="https://www.gosugamers.net"+links
	
	headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'}
	page=requests.get(URL,headers=headers)
	noodles = BeautifulSoup(page.content, 'html.parser')

	data=[]
	for i in noodles.select('div.row.text-right'):
		data.append(i.getText())
	
	splitted=[]
	splitted=(data[1].split('\n'))
	

	x = [str for str in splitted if str ]

	# for i in x:

	prating=x[1].replace(" ","")
	prating=prating.replace(",","")
	if prating=="-":
		prating="0"
	elif prating=="":
		prating="error"
	pworldrank=x[4].replace(" ","")
	pworldrank=pworldrank.replace(",","")
	if pworldrank=="-":
		pworldrank="0"
	elif pworldrank=="":
		pworldrank="error"
	pearnings=x[7].replace(" ","")
	pearnings=pearnings.replace(",","")
	if pearnings=="-":
		pearnings="0"
	elif pearnings=="":
		pearnings="error"
	pwinrate=x[len(x)-2].replace(" ","")
	pwinrate=pwinrate.replace(",","")
	if pwinrate=="-":
		pwinrate="0"
	elif pwinrate=="":
		pwinrate="error"
	# print(rating, worldrank,earnings,winrate)
	finalplayerdata.append(prating)
	finalplayerdata.append(pworldrank)
	finalplayerdata.append(pearnings)
	finalplayerdata.append(pwinrate)




print("-----------------------WELCOME TO THE FUTURE!-------------------------")

URL=input("Enter URL:")
# URL="https://www.gosugamers.net/dota2/tournaments/42645-dota-pro-circuit-2021-season-1/matches/387115-496-gaming-vs-execration"
headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'}
page=requests.get(URL,headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')


threadnamelink=[]
get_name_thread=threading.Thread(target=getTeamNames, args=(soup,finalteamnames))
get_name_thread.start()
threadnamelink.append(get_name_thread)


get_link_thread=threading.Thread(target=getTeamLink,args=(soup,))
get_link_thread.start()
threadnamelink.append(get_link_thread)

get_playerlinks_thread=threading.Thread(target=getPlayerLink,args=(soup,))
get_playerlinks_thread.start()
threadnamelink.append(get_playerlinks_thread)

get_PlayerName_thread=threading.Thread(target=getPlayerName,args=(soup,finalplayernames))
get_PlayerName_thread.start()
threadnamelink.append(get_PlayerName_thread)

for process in threadnamelink:
	process.join()

	

teamdatathread=[]
	#when link is scrapped we exectue a function here to get those data
get_teamdata1_thread=threading.Thread(target=getTeamData,args=(link[0],finalteamdata))

teamdatathread.append(get_teamdata1_thread)

get_teamdata2_thread=threading.Thread(target=getTeamData,args=(link[1],finalteamdata))

teamdatathread.append(get_teamdata2_thread)

for process in teamdatathread:
	process.start()
	process.join()

getplayerdatathread=[]



if(len(playerlistslink)==10):
	get_PlayerData_thread0=threading.Thread(target=getPlayerData,args=(playerlistslink[0],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread0)
	get_PlayerData_thread1=threading.Thread(target=getPlayerData,args=(playerlistslink[1],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread1)
	get_PlayerData_thread2=threading.Thread(target=getPlayerData,args=(playerlistslink[2],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread2)
	get_PlayerData_thread3=threading.Thread(target=getPlayerData,args=(playerlistslink[3],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread3)
	get_PlayerData_thread4=threading.Thread(target=getPlayerData,args=(playerlistslink[4],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread4)
	get_PlayerData_thread5=threading.Thread(target=getPlayerData,args=(playerlistslink[5],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread5)
	get_PlayerData_thread6=threading.Thread(target=getPlayerData,args=(playerlistslink[6],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread6)
	get_PlayerData_thread7=threading.Thread(target=getPlayerData,args=(playerlistslink[7],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread7)
	get_PlayerData_thread8=threading.Thread(target=getPlayerData,args=(playerlistslink[8],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread8)
	get_PlayerData_thread9=threading.Thread(target=getPlayerData,args=(playerlistslink[9],finalplayerdata))
	getplayerdatathread.append(get_PlayerData_thread9)
	for process in getplayerdatathread:
		process.start()
		process.join()
else:
	print("Not enough players")
	

print(finalteamnames) #
print(finalteamdata)
print(finalplayernames)
print(finalplayerdata)

#saving the data to file for processing later

print("\n\t\t\tMatch Details")
print("Names:\t\t"+finalteamnames[0]+"\t \t \t \t "+finalteamnames[1])
print("WorldRank\t"+finalteamdata[1]+"\t \t \t \t \t"+finalteamdata[5])
print("Rating\t\t"+finalteamdata[0]+"\t \t \t \t \t"+finalteamdata[4])
print("Earnings\t"+finalteamdata[2]+"\t \t \t \t \t"+finalteamdata[6])
print("AllTime Winrate\t"+finalteamdata[3]+"\t \t \t \t \t"+finalteamdata[7])

print("\n\t\t\tPlayer details")
print("\n\t"+finalteamnames[0]+"\t \t \t \t"+finalteamnames[1])
print(finalplayernames[0],finalplayerdata[0],finalplayerdata[1],finalplayerdata[2],finalplayerdata[3],"\t\t\t\t",finalplayernames[5],finalplayerdata[20],finalplayerdata[21],finalplayerdata[22],finalplayerdata[23])
print(finalplayernames[1],finalplayerdata[4],finalplayerdata[5],finalplayerdata[6],finalplayerdata[7],"\t\t\t\t",finalplayernames[6],finalplayerdata[24],finalplayerdata[25],finalplayerdata[26],finalplayerdata[27])
print(finalplayernames[2],finalplayerdata[8],finalplayerdata[9],finalplayerdata[10],finalplayerdata[11],"\t\t\t\t",finalplayernames[7],finalplayerdata[28],finalplayerdata[29],finalplayerdata[30],finalplayerdata[31])
print(finalplayernames[3],finalplayerdata[12],finalplayerdata[13],finalplayerdata[14],finalplayerdata[15],"\t\t\t\t",finalplayernames[8],finalplayerdata[32],finalplayerdata[33],finalplayerdata[34],finalplayerdata[35])
print(finalplayernames[4],finalplayerdata[16],finalplayerdata[17],finalplayerdata[18],finalplayerdata[19],"\t\t\t\t",finalplayernames[9],finalplayerdata[36],finalplayerdata[37],finalplayerdata[38],finalplayerdata[39])


returned1=[]
returned2=[]
plearn1=[finalplayerdata[2],finalplayerdata[6],finalplayerdata[10],finalplayerdata[14],finalplayerdata[18]]
plearn2=[finalplayerdata[22],finalplayerdata[26],finalplayerdata[30],finalplayerdata[34],finalplayerdata[38]]

plearn1 = [item.replace("$", "") for item in plearn1]
plearn2 = [item.replace("$", "") for item in plearn2]

sum1=0
sum2=0
for items in plearn1:
	sum1+=int(items)
for items in plearn2:
	sum2+=int(items)
print('AVERAGE: ',sum1,"\t\t\t\t",'AVERAGE: ',sum2)