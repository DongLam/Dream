from datetime import timezone,datetime
import requests
from celery.schedules import crontab
import pymongo
from crawler import constants
from crawler.Serializer.Serializer import MatchSerializer
from crawler.constants import *
from crawler.tele_bot import send_message, send_message_bo2
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def egb(timeStamp):
	try:
		url = "https://egb.com/bets?st=0&ut=0&active=true"
		response = requests.get(url, headers={"Accept": "application/json"})
		bets = response.json()['bets']
		i = 0
		for bet in bets:
			game = ''
			if bet['game']:
				game = get_game_egb(bet['game'])
			if game:

				match = {
					'team1': bet['gamer_1']['nick'],
					'team2': bet['gamer_2']['nick'],
					'odds1': bet['coef_1'],
					'odds2': bet['coef_2'],
					'site': constants.EGB,
					'game': game,
					'dateTimeStamp': timeStamp,
					'team1_tmp': change_name_to_tmp(bet['gamer_1']['nick']),
					'team2_tmp': change_name_to_tmp(bet['gamer_2']['nick'])
				}
				match = sort_team_name(match)
				matchSerializer = MatchSerializer(data=match)
				if matchSerializer.is_valid():
					matchSerializer.save()
					i = i + 1
		print("Done Egb: " + str(i))
	except Exception as e:
		print(e)


def bet_winner(timeStamp):
	try:
		url = constants.BET_WINNER_URL
		response = requests.get(url, headers={"Accept": "application/json"})
		bets = response.json()['Value']
		i = 0
		for bet in bets:
			try:
				game = ''
				if bet['L']:
					game = get_game_bet_winnner(bet['L'])
				if bet['O2'] == "LDLC" or bet['O1'] == "LDLC":
					print()
				if game:
					match = {
						'team1': bet['O1'],
						'team2': bet['O2'],
						'odds1': bet['E'][0]['C'],
						'site': constants.BET_WINNER,
						'game': game,
						'dateTimeStamp': timeStamp,
						'team1_tmp': change_name_to_tmp(bet['O1']),
						'team2_tmp': change_name_to_tmp(bet['O2']),
						'league': bet['L'],
						'datetime': bet['S']
					}
					if len(bet['E']) == 2:
						match['odds2'] = bet['E'][1]['C']
					match = sort_team_name(match)
					matchSerializer = MatchSerializer(data=match)
					if matchSerializer.is_valid():
						matchSerializer.save()
						i = i +1
			except Exception as e:
				print(e)
		print("Done Bet-Winner: " + str(i))
	except Exception as e:
		print(e)

def ps38(timeStamp):
	# 'https://www.ps3838.com/sports-service/sv/compact/events?l=3&lv=&me=0&mk=1&sp=12&locale=en_US'
	url = constants.PS38_URL
	response = requests.get(url, headers={"Accept": "application/json"})
	datas = response.json()['n']
	matches_save = []
	i = 0
	for data in datas:
		if len(data) > 2:
			leagues = data[2]
			for league in leagues:
				if len(league) > 2:
					matches = league[2]
					title = league[1]
					title_split = title.split(' - ')
					for match in matches:
						if match[2].find('(Kills)') == -1:
							name1 = match[1]
							name2 = match[2]
							rates = match[8]['0']
							for rate in rates:
								if rate.__class__ == list:
									if len(rate) == 7:
										bet = {
											'team1': name1,
											'team2': name2,
											'odds1': rate[1],
											'odds2': rate[0],
											'site': constants.PS38,
											'game': get_game_ps38(title_split[0]),
											'dateTimeStamp': timeStamp,
											'team1_tmp': change_name_to_tmp(name1),
											'team2_tmp': change_name_to_tmp(name2)
										}
										bet = sort_team_name(bet)
										matchSerializer = MatchSerializer(data=bet)
										if matchSerializer.is_valid():
											matchSerializer.save()
											i = i + 1
										else:
											print(matchSerializer.errors)
											print("Handicap or map", name1, name2)
										# else:
										#      print("Trash", name1, name2)
	print("Done PS38: " + str(i))

def sbotop(timeStamp):
	try:
		print("-----------SBOTOP----------------")
		url = constants.SPOTOP
		payload = {
			"GameCat": 1,
			"SportId": -99,
			"BaseLGIds": [
				-99
			],
			"EventMarket": -99,
			"MatchCnt": 500,
			"SortType": 1,
			"HasLive": False,
			"Token": "21f8a3869d1182272a8fa8b0bfefd39e",
			"Language": "vn",
			"BettingChannel": 1
		}
		response = requests.post(url, headers={"Accept": "application/json"}, json = payload)
		bets = response.json()['Sport']
		i = 0
		for bet in bets:
			try:
				game = ''
				if bet.get('SportName'):
					game = get_game_sbotop(bet['SportName'])
				if game:
					lgs = bet['LG']
					for lg in lgs:
						matches = lg['ParentMatch']
						for match in matches:
							tmp = {
								'team1': match['PHTName'],
								'team2': match['PATName'],
								'odds1': match['Match'][0]['Odds'][0]['SEL'][0]['Odds'],
								'odds2': match['Match'][0]['Odds'][0]['SEL'][1]['Odds'],
								'site': constants.SBOTOP,
								'game': game,
								'dateTimeStamp': timeStamp,
								'team1_tmp': change_name_to_tmp(match['PHTName']),
								'team2_tmp': change_name_to_tmp(match['PATName'])
							}
							tmp = sort_team_name(tmp)
							matchSerializer = MatchSerializer(data=tmp)
							if matchSerializer.is_valid():
								matchSerializer.save()
								i = i +1
			except Exception as e:
				print(e)
		print("Done SBOTOP: " + str(i))
	except Exception as e:
		print(e)

def stake_lol(timeStamp):
	chrome_options = Options()
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--window-size=1920x1080")
	# chrome_options.headless = True
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="E:\chromedriver.exe")
	url = "https://stake.games/sports/home/upcoming/league-of-legends"
	driver.get(url)
	while True:
		try:
			time.sleep(3)
			load_more = driver.find_element(By.CSS_SELECTOR, ".variant-subtle-link.line-height-150pct.text-size-default.spacing-none.weight-semibold.align-left.fullWidth.svelte-1aq1zn0")
			load_more.click()
		except Exception as e:
			break
	data = driver.find_element(By.XPATH, "/html/body").text
	data_list = data.split("Winner")
	del data_list[0]
	i = 0 
	print(len(data_list))
	for a in data_list:
		try:
			b = a.split("\n")

			tmp = {
				'team1': b[1],
				'odds1': float(b[2]),
				'team2': b[3],
				'odds2': float(b[4]),
				'site': constants.STAKE,
				'game': BET_LOL,
				'dateTimeStamp': timeStamp,
				'team1_tmp': change_name_to_tmp(b[1]),
				'team2_tmp': change_name_to_tmp(b[3])
			}
			tmp = sort_team_name(tmp)
			matchSerializer = MatchSerializer(data=tmp)
			if matchSerializer.is_valid():
				matchSerializer.save()
				i = i + 1
		except Exception as e:
			print(e)
			continue
	print("Done STAKE LOL: " + str(i))
	driver.close()

def stake_csgo(timeStamp):
	chrome_options = Options()
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--window-size=1920x1080")
	# chrome_options.headless = True
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="E:\chromedriver.exe")
	url = "https://stake.games/sports/home/upcoming/counter-strike"
	driver.get(url)
	while True:
		try:
			time.sleep(3)
			load_more = driver.find_element(By.CSS_SELECTOR, ".variant-subtle-link.line-height-150pct.text-size-default.spacing-none.weight-semibold.align-left.fullWidth.svelte-1aq1zn0")
			load_more.click()
		except Exception as e:
			break
	data = driver.find_element(By.XPATH, "/html/body").text
	data_list = data.split("Winner")
	del data_list[0]
	i = 0 
	print(len(data_list))
	for a in data_list:
		try:
			b = a.split("\n")

			tmp = {
				'team1': b[1],
				'odds1': float(b[2]),
				'team2': b[3],
				'odds2': float(b[4]),
				'site': constants.STAKE,
				'game': BET_CSGO,
				'dateTimeStamp': timeStamp,
				'team1_tmp': change_name_to_tmp(b[1]),
				'team2_tmp': change_name_to_tmp(b[3])
			}
			tmp = sort_team_name(tmp)
			matchSerializer = MatchSerializer(data=tmp)
			if matchSerializer.is_valid():
				matchSerializer.save()
				i = i + 1
		except Exception as e:
			print(e)
			continue
	print("Done STAKE LOL: " + str(i))
	driver.close()




def send_notice():
	query = [
			{
				'$project': {
					'timestamp': {
						'$subtract': [
							'$dateTimeStamp', datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
						]
					},
					'team1': '$team1',
					'team2': '$team2',
					'team1_tmp': '$team1_tmp',
					'team2_tmp': '$team2_tmp',
					'game': '$game',
					'odds1': '$odds1',
					'odds2': '$odds2',
					'site': '$site',
					'league': 1,
					'datetime': 1,
					'type': 1
				}
			}, {
				'$group': {
					'_id': {
						'x': '$team1_tmp',
						'y': '$team2_tmp',
						'z': '$game',
						'time': {
							'$round': [
							'$timestamp', -6
							]
						}
					},
					'a': {
						'$max': '$odds1'
					},
					'b': {
						'$max': '$odds2'
					},
					'c': {
						'$min': '$odds1'
					},
					'd': {
						'$min': '$odds2'
					},
					'sites': {
						'$addToSet': '$site'
					},
					'docs': {
						'$push': '$$ROOT'
					}
                    }
			}, {
				'$project': {
					'a': 1,
					'b': 1,
					'c': 1,
					'd': 1,
					'numbersOfSite': {
						'$size': '$sites'
					},
					'sites': 1,
					'docs': 1
				}
			}, {
				'$sort': {
					'a': 1
				}
			}, {
				'$match': {
					'numbersOfSite': {
						'$gt': 1
					}
				}
			}, {
				'$project': {
					'e': {
						'$multiply': [
							{
								'$subtract': [
									'$a', 1
								]
							}, {
								'$subtract': [
									'$b', 1
								]
							}
						]
					},
					'a': 1,
					'b': 1,
					'c': 1,
					'd': 1,
					'sites': 1,
					'docs': 1
                    }
			},{
				'$match': {
					'e': {
						'$gt': 1.2
					}
				}
			}, {
				'$sort': {
					'e': -1
				}
			}
		]

	MONGODB_URI = "mongodb://localhost:27017/bet?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
	# Connect to your MongoDB cluster:
	client = pymongo.MongoClient(MONGODB_URI)
	# Get a reference to the "sample_mflix" database:
	db = client["Bet"]
	# Get a reference to the "movies" collection:
	collection = db["crawler_match"]

	items = collection.aggregate(query)
	for item in items:
		arrays = item['docs']
		value = item['e']
		str_send = "game: " + item['_id']['z'] + " value = " + str(value) + "\n"
		for i in arrays:
			str_send = str_send + i['site'] +':\n\t ' + data_to_string(i) + "\n"
		send_message_bo2(str_send)
		# if i['type'] == 1:
		#      send_message_bo2(str_send)
		# else:
		#      send_message(str_send)
		print(str_send)

def data_to_string(data):
	string = "team1: " + data['team1'] + ", team2: " + data['team2']
	if data.get('odds1') is not None:
		string = string + ', odds1: ' + str(data.get('odds1'))
	if data.get('odds2') is not None:
		string = string + ', odds2: ' + str(data.get('odds2'))
	if data['site'] == 'BETWINNER':
		string = string + ', league: ' + data['league'] + ' , datetime: ' + datetime.fromtimestamp(int(data.get('datetime')), tz=timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
	return string

def change_name_to_tmp(team):
	result = team.upper().replace(" ", "").replace("-", "").replace("TEAM", "").replace("GAMING", "").\
		replace("ESPORTS", "").replace("ESPORT", "").replace("SPORTS", "").replace("(GAMBIT)", "").\
		replace("CHALLENGERS", "").replace("CHALL", "").replace("ECLUB", "").replace("CLAN", "")
	for item in MANUAL_NAME:
		if item[0] == result:
			result = item[1]
	return result


def get_game_bet_winnner(game):
	if BW_CSGO in game:
		return BET_CSGO
	if BW_LOL in game:
		return BET_LOL
	if BW_LOL2 in game:
		return BET_LOL
	if BW_STAR_CRAFT in game:
		return BET_STAR_CRAFT
	if BW_DOTA2 in game:
		return BET_DOTA2
	if BW_KOG in game:
		return BET_KOG
	if BW_KOG2 in game:
		return BET_KOG
	if BW_VAL in game:
		return BET_VAL
	if BW_PUBG in game:
		return BET_PUBG
	if BW_AOR in game:
		return BET_AOR
	else:
		return None

def get_game_egb(game):
	if EGB_CSGO in game:
		return BET_CSGO
	if EGB_LOL in game:
		return BET_LOL
	if EGB_STAR_CRAFT in game:
		return BET_STAR_CRAFT
	if EGB_DOTA2 in game:
		return BET_DOTA2
	if EGB_KOG in game:
		return BET_KOG
	if EGB_VAL in game:
		return BET_VAL
	if EGB_PUBG in game:
		return BET_PUBG
	if EGB_AOR in game:
		return BET_AOR
	else:
		return None

def get_game_ps38(game):
	if PS38_CSGO in game:
		return BET_CSGO
	if PS38_LOL in game:
		return BET_LOL
	if PS38_STAR_CRAFT in game:
		return BET_STAR_CRAFT
	if PS38_DOTA2 in game:
		return BET_DOTA2
	if PS38_KOG in game:
		return BET_KOG
	if PS38_VAL in game:
		return BET_VAL
	if PS38_PUBG in game:
		return BET_PUBG
	if PS38_AOR in game:
		return BET_AOR
	else:
		return None

def get_game_sbotop(game):
	if SBO_CSGO in game:
		return BET_CSGO
	if SBO_LOL in game:
		return BET_LOL
	if SBO_STAR_CRAFT in game:
		return BET_STAR_CRAFT
	if SBO_DOTA2 in game:
		return BET_DOTA2
	if SBO_KOG in game:
		return BET_KOG
	if SBO_VAL in game:
		return BET_VAL
	if SBO_PUBG in game:
		return BET_PUBG
	if SBO_AOR in game:
		return BET_AOR
	else:
		return None

def sort_team_name(match):
	match['team1_tmp'] = (match['team1_tmp'].encode('ascii', 'ignore')).decode("utf-8")
	match['team2_tmp'] = (match['team2_tmp'].encode('ascii', 'ignore')).decode("utf-8")
	if match['team1_tmp'] > match['team2_tmp']:
		team_tmp = match['team1']
		match['team1'] = match['team2']
		match['team2'] = team_tmp

		odd_tmp = match['odds1']
		match['odds1'] = match['odds2']
		match['odds2'] = odd_tmp

		team_tmp = match['team1_tmp']
		match['team1_tmp'] = match['team2_tmp']
		match['team2_tmp'] = team_tmp
	return match
