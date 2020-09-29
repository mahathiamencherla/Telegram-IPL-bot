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

def pointsTableParser(table):
	beautyTable = "Teams    Played    Won    Lost    Tied      Net RR\n"
	table[0] = [i.ljust(10,' ') for i in table[0]]
	# print("Teams\tPlayed\tWon\tLost\tTied\t Net RR")
	for i in range(len(table)):
		print(len(table[0][i]))
		# print(table[0][i],"\t",table[1][i],"\t",table[2][i],"\t",table[3][i],"\t",table[4][i],"\t",table[5][i],"\t")
		beautyTable += table[0][i] + table[1][i]+"            "+table[2][i]+"            "+table[3][i]+"          "+table[4][i]+"        "+table[5][i]
		beautyTable += "\n"	
	return beautyTable

# table = getPointsTable()
# pointsTableParser(table)