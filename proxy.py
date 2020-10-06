import requests
from bs4 import BeautifulSoup

def get_proxies():
    proxies = []
    count = 0
    url = "https://free-proxy-list.net/"
    req = requests.get(url, "lxml")
    soup = BeautifulSoup(req.content, 'html.parser')
    tables = soup.findChildren('table')
    my_table = tables[0]
    rows = my_table.findChildren(['tr'])    
    for row in rows:
        count += 1
        if count == 22:
            break
        cell = row.findChildren('td')
        if len(cell) > 0:          
            proxy = cell[0].string+":"+cell[1].string
            proxies.append(proxy)    
    return proxies
print("proxy.py")
proxies = get_proxies()
print("got proxy")

def get_working_proxy():        
    global proxies
    while (True):
        if proxies == []:
            print("getting new list")
            proxies = get_proxies()
        count = 1
        while proxies != []:
            print(count,len(proxies)," proxies in list",end="\n")          
            count += 1
            return proxies.pop()