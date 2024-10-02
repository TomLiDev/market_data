from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StockData, ForexData

import requests
import json


APIKEY = 'EPM8MUYDLLTJHU0D' 
#replace 'my_alphav_api_key' with your actual Alpha Vantage API key obtained from https://www.alphavantage.co/support/#api-key


DATABASE_ACCESS = True 
#if False, the app will always query the Alpha Vantage APIs regardless of whether the stock data for a given ticker is already in the local database

def forex(request):
    return render(request, 'forex.html', {})

@csrf_exempt
def get_forex_data(request):
    if request.is_ajax():
        symbol = request.POST.get('symbol', 'null')
        print("2nd forex test in views for symbol", symbol)
        tempSymbol = "EURUSD"

        if DATABASE_ACCESS == True:
            #checking if the database already has data stored for this ticker before querying the Alpha Vantage API
            if ForexData.objects.filter(symbol=symbol).exists():
                print("1st in views for forex", symbol, tempSymbol) 
                #We have the data in our database! Get the data from the database directly and send it back to the frontend AJAX call
                entry = ForexData.objects.filter(symbol=symbol)[0]
                print("TEST3", entry.data)
                return HttpResponse(entry.data, content_type='application/json')
            print("in here 2")

        forex_data = requests.get(f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey={APIKEY}').json()
        print("second forex test in views", forex_data)

        forex_output = {}
        forex_output['prices'] = forex_data

        tempForex = ForexData(symbol=symbol, data=json.dumps(forex_output))
        tempForex.save()

    return HttpResponse(json.dumps(forex_output), content_type='application/json')


#view function for rendering home.html
def home(request):
    return render(request, 'home.html', {})


@csrf_exempt
def get_stock_data(request):
    if request.is_ajax():
        #get ticker from the AJAX POST request
        ticker = request.POST.get('ticker', 'null')
        ticker = ticker.upper()
        print("In here", ticker)

        if DATABASE_ACCESS == True:
            #checking if the database already has data stored for this ticker before querying the Alpha Vantage API
            if StockData.objects.filter(symbol=ticker).exists(): 
                #We have the data in our database! Get the data from the database directly and send it back to the frontend AJAX call
                entry = StockData.objects.filter(symbol=ticker)[0]
                print("1st inside views")
                print("2nd inside views", entry.symbol)
                print("3rd if already exisits")
                return HttpResponse(entry.data, content_type='application/json')
            print("in here 2")

        #obtain stock data from Alpha Vantage APIs
        #get adjusted close data
        price_series = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={APIKEY}&outputsize=full').json()
        print("test for price data", price_series)
        #get SMA (simple moving average) data
        sma_series = requests.get(f'https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval=daily&time_period=10&series_type=close&apikey={APIKEY}').json()

        #test
        daily_price = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={APIKEY}').json()
        print("TEST for daily", daily_price)
        #package up the data in an output dictionary 
        output_dictionary = {}
        output_dictionary['prices'] = price_series
        output_dictionary['sma'] = sma_series
        output_dictionary['daily'] = daily_price

        #save the dictionary to database
        temp = StockData(symbol=ticker, data=json.dumps(output_dictionary))
        temp.save()

        #return the data back to the frontend AJAX call 
        return HttpResponse(json.dumps(output_dictionary), content_type='application/json')

    else:
        message = "Not Ajax"
        return HttpResponse(message)

