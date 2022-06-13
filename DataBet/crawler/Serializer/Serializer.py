from rest_framework import serializers

from crawler.models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('team1',
                    'team2',
                    'odds1',
                    'odds2',
                    'site',
                    'game',
                    'dateTimeStamp',
                    'team1_tmp',
                    'team2_tmp',
                    'league',
                    'datetime')