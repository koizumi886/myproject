from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import datetime
import requests as rq  # サーバにURLを送るためのライブラリ

class SampleAPIView(APIView):
    def get(self, request):
        weather = getWeather()
        return Response("weather: " + weather, status=status.HTTP_200_OK)


class DateTimeView(APIView):
    def get(self, request):
        datetime_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        return Response(datetime_str, status=status.HTTP_200_OK)


class IndexView(TemplateView):
    template_name = "index.html"
    
def getWeather():
    url = 'https://weather.tsukumijima.net/api/forecast/city/'
    r = rq.get(url + '170010') # 天気を調べる
    天気= r.json() # 得られた結果をJSON形式に変更する
    telop = 天気['forecasts'][1]['telop'] # 真ん中の数字は、0:今日 1:明日 2:明後日を表す
    return telop
