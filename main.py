from google_flights import GoogleFlights
import datetime
from time import sleep
import yaml

with open('config.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print('config', data)

period_end = data['period']['end']
holidays = data['holidays']
vacation_days = data['vacation_days']
result = {
    'price': 10000,
    'start': '',
    'end': ''
}

gf = GoogleFlights(data['origin'], data['destination'])

curr_start = data['period']['start']

while True:
    #calculate the end date
    vac_days = 1 if curr_start.weekday() < 5 else 0
    end = curr_start
    while vac_days < vacation_days:
        end += datetime.timedelta(days=1)
        if period_end < end:
            print(result)
            exit(0)
        elif end.weekday() < 5 and end not in holidays:
            vac_days += 1
    print(curr_start, end)
    # get the cheapest price for this period
    price = gf.get_cheapest_price(curr_start, end)
    print('price', price)
    if price < result['price']:
        result['price'] = price
        result['start'] = curr_start
        result['end'] = end
    curr_start += datetime.timedelta(days=1)

