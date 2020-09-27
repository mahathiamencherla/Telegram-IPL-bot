import requests
from bs4 import BeautifulSoup


def getPointsTable() :
	url = "https://www.iplt20.com/points-table/2020"

	req = requests.get(url, "lxml")
	soup = BeautifulSoup(req.content, 'html.parser')

	tables = soup.findChildren('table')
	my_table = tables[0]
	rows = my_table.findChildren(['tr'])

	teamStanding = []
	played =[]
	won = []
	lost =[]
	tied = []
	netRR = []

	for row in rows:
		team = row.findChildren('span')
		if len(team) == 2:
			teamStanding.append(team[1].string)		
		cells = row.findChildren('td')[2:9]
		if len(cells) == 0 :
			continue
		played.append(cells[0].string)
		won.append(cells[1].string)
		lost.append(cells[2].string)
		tied.append(cells[3].string)
		netRR.append(cells[5].string)


	#print(teamStanding,played,won,lost,tied,netRR,sep="\n")
	return([teamStanding,played,won,lost,tied,netRR])