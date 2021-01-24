# get date and league through argv or argparse
# get auctions started and players cut from that day
# get ottoneu data: last 10 auctions and maybe roster %
# using pybaseball, scrape statcast info
	# v2: scrape RoS steamer / zips projections
# format data into email and send
import requests
from bs4 import BeautifulSoup
auction_url = "https://ottoneu.fangraphs.com/953/transactions"
resp = requests.get(auction_url)
soup = BeautifulSoup(resp.content, 'html.parser')
table = soup.find('table')
print(len(table))
thead = [th.get_text() for th in table.find('thead').find_all('th')]
print(thead)
trows = [tr for tr in table.find('tbody').find_all('tr')]
# filter for correct transaction type and only current transactions
#  get player name and take link to player page
# then use lookup to get player data
# append this link to the main url?
print([a['href'] for a in trows[0].find_all('a') if "playercard" in a['href']])
