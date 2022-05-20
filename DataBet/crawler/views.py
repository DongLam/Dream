from datetime import timezone, datetime

import pymongo
import requests
from django.http import HttpResponse

from rest_framework.views import APIView
from crawler import constants
from crawler.Serializer.Serializer import MatchSerializer
from crawler.constants import BET_WINNER
from crawler.models import Match
from crawler.tele_bot import send_message


class Crawl(APIView):
    def get(self, request):
        url = "https://egb.com/bets?st=0&ut=0&active=true"
        response = requests.get(url, headers={"Accept": "application/json"})
        bets = response.json()['bets']
        matches = []
        i = 1
        j = 1
        for bet in bets:
            if bet['game'] and 'CS:GO' in bet['game']:
                match = {
                    'team1': bet['gamer_1']['nick'],
                    'team2': bet['gamer_2']['nick'],
                    'odds1': bet['coef_1'],
                    'odds2': bet['coef_2'],
                    'site': constants.EGB,
                    'game': bet['game']
                }
                matches.append(match)
                matchSerializer = MatchSerializer(data=match)
                if matchSerializer.is_valid():
                    matchSerializer.save()
        return (response.json()['user_time'])


class Lam(APIView):
    def get(self, request):
        url = constants.BET_WINNER_URL
        response = requests.get(url, headers={"Accept": "application/json"})
        bets = response.json()['Value']
        matches = []
        for bet in bets:
            if len(bet['E']) < 2:
                continue
            if bet['L'] and 'CS:GO' in bet['L']:
                match = {
                    'team1': bet['O1'],
                    'team2': bet['O2'],
                    'odds1': bet['E'][0]['C'],
                    'odds2': bet['E'][1]['C'],
                    'game': 'CS:GO',
                    'site': constants.BET_WINNER

                }
                matches.append(match)
                matchSerializer = MatchSerializer(data=match)

                if matchSerializer.is_valid():
                    matchSerializer.save()
        return HttpResponse(1)


def get_data_bet_winner():
    datas=Match.objects.filter(site=BET_WINNER)
    message=''
    i=0
    for data in datas:
        i = i + 1
        message += '\n' + str(MatchSerializer(data).data)
        if i > 20:
            break

    send_message(message)


class Trieu(APIView):
    def post(self, request):

        from .tasks import crawl_task
        crawl_task()
        return HttpResponse(2)



    def get(self, request):
        from crawler.craw import send_notice
        send_notice()

        return HttpResponse(1)

    def put(self, request):
        query = [
                    {
                        '$sort': {
                            'team1': -1,
                            'team2': -1,
                            'dateTimeStamp': -1
                        }
                    }, {
                        '$group': {
                            '_id': {
                                't1': '$team1_tmp',
                                't2': '$team2_tmp',
                                # 's': '$site'
                            },
                            'docs': {
                                '$push': '$$ROOT'
                            }
                        }
                    # }, {
                    #     '$project': {
                    #         'match': {
                    #             '$slice': [
                    #                 '$docs', 1
                    #             ]
                    #         }
                    #     }
                    # }, {
                    #     '$sort': {
                    #         'team1': -1,
                    #         'team2': -1
                    #     }
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
        arr = []
        dem3 = 0
        dem2 = 0
        dem1 = 0
        demegb = 0
        for item in items:

            if len(item['docs']) == 1:

                dem1 = dem1 + 1
                if item['docs'][0]['site'] == 'EGB':
                    arr.append(item)
                    demegb = demegb + 1
                    print(item['docs'][0]['team1_tmp'], item['docs'][0]['team2_tmp'])
            if len(item['docs']) == 2:
                dem2 = dem2 + 1
            if len(item['docs']) > 2:
                dem3 = dem3 + 1



        print(dem1, dem2, dem3, demegb)
        return HttpResponse(arr)
