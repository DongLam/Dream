from datetime import datetime, timezone, timedelta

import pymongo

from DataBet.settings import DATABASE_HOST
from crawler.Serializer.Serializer import MatchSerializer
from crawler.models import Match
from crawler.tele_bot import send_message


def detect():
    query = [
        {
            '$sort': {
                'dateTimeStamp': -1
            }
        }, {
            '$group': {
                '_id': {
                    't1': '$team1_tmp',
                    't2': '$team2_tmp',
                    's': '$site',
                    'dt': '$dateTimeStamp'
                },
                'docs': {
                    '$push': '$$ROOT'
                }
            }
        }, {
            '$project': {
                'match': {
                    '$slice': [
                        '$docs', 1
                    ]
                }
            }
        }, {
            '$sort': {
                'team1_tmp': -1,
                'team2_tmp': -1
            }
        }
    ]

    MONGODB_URI = DATABASE_HOST
    # Connect to your MongoDB cluster:
    client = pymongo.MongoClient(MONGODB_URI)
    # Get a reference to the "sample_mflix" database:
    db = client["Bet"]
    # Get a reference to the "movies" collection:
    collection = db["crawler_match"]
    list = []
    items = collection.aggregate(query)
    for item in items:
        matchSerializer = MatchSerializer(data=item['match'][0])

        if (matchSerializer.is_valid()):
            list.append(str(matchSerializer.data))
        else:
            print(matchSerializer.errors)
    list.sort()

    for result in list:
        print(result)


def lam():
    try:
        query = [
            {
                '$project': {
                    'timestamp': {
                        '$subtract': [
                            '$dateTimeStamp', datetime.now()
                        ]
                    },
                    'team1': '$team1',
                    'team2': '$team2',
                    'odds1': '$odds1',
                    'odds2': '$odds2',
                    'site': '$site',
                    'game': '$game',
                    'dateTimeStamp': '$dateTimeStamp',
                    'team1_tmp': '$team1_tmp',
                    'team2_tmp': '$team2_tmp',
                }
            }, {
                '$match': {
                    'timestamp': {
                        '$gt': -60000
                    }
                }
            }
        ]
        MONGODB_URI = DATABASE_HOST
        # Connect to your MongoDB cluster:
        client = pymongo.MongoClient(MONGODB_URI)
        # Get a reference to the "sample_mflix" database:
        db = client["Bet"]
        # Get a reference to the "movies" collection:
        collection = db["crawler_match"]
        items = collection.aggregate(query)

        list = []
        for item in items:
            matchSerializer = MatchSerializer(data=item)
            if matchSerializer.is_valid():
                list.append(matchSerializer.data)
        list = sorted(list, key=lambda d: (d['game'], d['team1_tmp']), reverse=True)

        lam = []
        for i in range(0, len(list) - 1):
            if list[i]['team2_tmp'] == list[i+1]['team2_tmp'] and list[i]['site'] != list[i+1]['site']:
                lam.append(list[i])
                lam.append(list[i+1])

        message = ''
        for result in lam:
            message = message + str(result) + '\n'
        # send_message(message)
        print(message)
    except Exception as e:
        print(e)

def detect_exception():
    try:
        query = [
            {
                '$project': {
                    'time_dif': {
                        '$subtract': [
                            '$dateTimeStamp', datetime.now()
                        ]
                    },
                    'team1': '$team1',
                    'team2': '$team2',
                    'odds1': '$odds1',
                    'odds2': '$odds2',
                    'site': '$site',
                    'game': '$game'
                }
            }, {
                '$sort': {
                    'time_dif': -1
                }
            }, {
                '$match': {
                    'time_dif': {
                        '$gte': -30000,
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        't1': '$team1_tmp',
                        't2': '$team2_tmp'
                    },
                    'o1': {
                        '$max': '$odds1'
                    },
                    'o2': {
                        '$max': '$odds2'
                    },
                    'docs': {
                        '$push': '$$ROOT'
                    }
                }
            }, {
                '$redact': {
                    '$cond': {
                        'if': {
                            '$or': [
                                {
                                    '$eq': [
                                        {
                                            '$ifNull': [
                                                '$odds1', '$$ROOT.o1'
                                            ]
                                        }, '$$ROOT.o1'
                                    ]
                                }, {
                                    '$eq': [
                                        {
                                            '$ifNull': [
                                                '$odds2', '$$ROOT.o2'
                                            ]
                                        }, '$$ROOT.o2'
                                    ]
                                }
                            ]
                        },
                        'then': '$$DESCEND',
                        'else': '$$PRUNE'
                    }
                }
            }, {
                '$project': {
                    'est': {
                        '$multiply': [
                            {
                                '$subtract': [
                                    '$o1', 1
                                ]
                            }, {
                                '$subtract': [
                                    '$o2', 1
                                ]
                            }
                        ]
                    },
                    'docs': '$docs'
                }
            }, {
                '$match': {
                    'est': {
                        '$gt': 1
                    }
                }
            }
        ]
        MONGODB_URI = DATABASE_HOST
        # Connect to your MongoDB cluster:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client["Bet"]
        collection = db["crawler_match"]
        items = collection.aggregate(query)

        list_result = []
        dem = 0
        for item in items:
            if (dem == 0):
                print(item)
                dem = dem + 1
            for i in item['docs']:
                matchSerializer = MatchSerializer(data=i)
                if matchSerializer.is_valid() and len(list_result) > 1:
                    tmp = list_result[-1]
                    if matchSerializer['team1'] == tmp['team1'] and matchSerializer['team2'] == tmp['team2'] and matchSerializer['site'] == tmp['site']:
                        list_result.pop()
                    else:
                        list_result.append(str(matchSerializer.data))
        message = ''
        for result in list_result:
            message = message + str(result) + '\n'
        if len(message) > 0:
            send_message(message)
        print('Done Detect')

    except Exception as e:
        print(e)

def format_msg(team1, team2, game, site):
    msg = 'Site: ' + site + 'Match: ' + team1 + '-' + team2 + ', Game: ' + game
    return msg