import requests
from datetime import datetime

class TrainManager:
    def __init__(self):
        self.url_train_price = "https://www.trainman.in/services/fare"
        self.url_train_details = 'https://api.railyatri.in/api/trains-between-station-from-wrapper.json'

    def train_price(self, from_st, to_st, t_num):
        params = {
            "origin": from_st,
            "dest": to_st,
            "tcode": t_num,
            "concession_code": "NONE",
            "age_group": "ADULT",
            "percentage_booked": "50",
            "key": "012562ae-60a9-4fcd-84d6-f1354ee1ea48"
        }
        headers = {
            "accept": "application/json, text/plain, /",
            "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
            "cookie": "AKA_A2=A; _gcl_au=1.1.453746515.1718111633; _ga=GA1.1.563653219.1718111636; _ga_2XGDR0QTJT=GS1.1.1718111635.1.1.1718111839.0.0.0",
            "priority": "u=1, i",
            "referer": "https://www.trainman.in/fare/16615",
            "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
        }

        response = requests.get(self.url_train_price, params=params, headers=headers)
        d_price = {}
        if response.status_code == 200:
            data = response.json()
            if 'fare' in data:
                for k, v in data['fare'].items():
                    if v['GN'] != '':
                        d_price[k] = v['GN']
                    else:
                        return None
                return d_price
            else:
                return None
        else:
            return None

    def get_train_details(self, from_code, to_code, date, way, time_filter):
        d = {}
        params = {
            'from': from_code,
            'to': to_code,
            'dateOfJourney': date,
            'action': 'train_between_station',
            'controller': 'train_ticket_tbs',
            'device_type_id': '6',
            'from_code': from_code,
            'from_name': from_code,
            'journey_date': date,
            'journey_quota': '',
            'to_code': to_code,
            'to_name': to_code,
            'user_id': '-171712006'
        }
        headers = {
            'accept': 'application/json, text/plain, /',
            'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
            'if-none-match': 'W/"b4668b9055f92ce6c0b70b72b4c156cd"',
            'lang': 'English',
            'origin': 'https://www.railyatri.in',
            'priority': 'u=1, i',
            'referer': 'https://www.railyatri.in/',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }

        response = requests.get(self.url_train_details, params=params, headers=headers)

        if response.status_code == 200:
            train_details = response.json()
        else:
            print("Failed to fetch data:", response.status_code)
            return None

        if train_details['train_between_stations']:
            flag = 0
            filtered_trains = []
            for train in train_details['train_between_stations']:
                if time_filter:
                    if way == 1:
                        arrival_time = datetime.strptime(train['to_sta'], '%H:%M')
                        if arrival_time <= time_filter:
                            filtered_trains.append(train)
                    else:
                        arrival_time = datetime.strptime(train['from_std'], '%H:%M')
                        if arrival_time >= time_filter:
                            filtered_trains.append(train)
                else:
                    filtered_trains.append(train)
            flag = 0
            for i in filtered_trains:
                flag = 1
                price = self.train_price(i['from'], i['to'], i['train_number'])
                if price and len(d) < 6:
                    d[i['train_number']] = {'train_name': i['train_name'], 'date': date, 'from_time': i['from_sta'],
                                            'to_time': i['to_std'], 'distance': i['distance'],
                                            'available_class': price,
                                            'from': i['from'], 'to': i['to']}
            if flag == 1:
                return 1, d
            else:
                for i in train_details['train_between_stations']:
                    price = self.train_price(i['from'], i['to'], i['train_number'])
                    if price and len(d) < 6:
                        d[i['train_number']] = {'train_name': i['train_name'], 'date': date,
                                                'from_time': i['from_sta'],
                                                'to_time': i['to_std'], 'distance': i['distance'],
                                                'available_class': price,
                                                'from': i['from'], 'to': i['to']}
                return 1, d

        if train_details['reserved_trains']:
            flag = 0
            filtered_trains = []
            for train in train_details['reserved_trains']:
                if time_filter:
                    if way == 1:
                        arrival_time = datetime.strptime(train['to_sta'], '%H:%M')
                        if arrival_time <= time_filter:
                            filtered_trains.append(train)
                    else:
                        arrival_time = datetime.strptime(train['from_std'], '%H:%M')
                        if arrival_time >= time_filter:
                            filtered_trains.append(train)
                else:
                    filtered_trains.append(train)
            flag = 0
            for i in filtered_trains:
                flag = 1
                price = self.train_price(i['from'], i['to'], i['train_number'])
                if price and len(d) < 6:
                    d[i['train_number']] = {'train_name': i['train_name'], 'date': date, 'from_time': i['from_sta'],
                                            'to_time': i['to_std'], 'distance': i['distance'],
                                            'available_class': price,
                                            'from': i['from'], 'to': i['to']}
            if flag == 1:
                return 1, d
            else:
                for i in train_details['reserved_trains']:
                    price = self.train_price(i['from'], i['to'], i['train_number'])
                    if price and len(d) < 6:
                        d[i['train_number']] = {'train_name': i['train_name'], 'date': date,
                                                'from_time': i['from_sta'],
                                                'to_time': i['to_std'], 'distance': i['distance'],
                                                'available_class': price,
                                                'from': i['from'], 'to': i['to']}
                return 1, d

        if train_details['alternate_trains']:
            flag = 0
            filtered_trains = []
            for train in train_details['alternate_trains']:
                if time_filter:
                    if way == 1:
                        arrival_time = datetime.strptime(train['to_std'], '%H:%M')
                        if arrival_time <= time_filter:
                            filtered_trains.append(train)
                    else:
                        arrival_time = datetime.strptime(train['from_sta'], '%H:%M')
                        if arrival_time >= time_filter:
                            filtered_trains.append(train)
                else:
                    filtered_trains.append(train)
            flag = 0
            for i in filtered_trains:
                flag = 1
                price = self.train_price(i['from'], i['to'], i['train_number'])
                if price and len(d) < 6:
                    d[i['train_number']] = {'train_name': i['train_name'], 'date': date, 'from_time': i['from_sta'],
                                            'to_time': i['to_std'], 'distance': i['distance'],
                                            'available_class': price,
                                            'from': i['from'], 'to': i['to']}
            if flag ==             1:
                return 1, d
            else:
                for i in train_details['alternate_trains']:
                    price = self.train_price(i['from'], i['to'], i['train_number'])
                    if price and len(d) < 6:
                        d[i['train_number']] = {'train_name': i['train_name'], 'date': date,
                                                'from_time': i['from_sta'],
                                                'to_time': i['to_std'], 'distance': i['distance'],
                                                'available_class': price,
                                                'from': i['from'], 'to': i['to']}
                return 1, d

        if train_details['nearby_station']:
            l = []
            for i in train_details['nearby_station']:
                l.append(i['to_code'])
            return 2, l
        else:
            return 1, None

