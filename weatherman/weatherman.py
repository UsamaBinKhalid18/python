import csv
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
import argparse

@dataclass
class WeatherData:
    max_temp:int
    min_temp:int
    max_hum:int
    min_hum:int

    def default_weather_data():
        return WeatherData(float('-inf'), float('inf'), float('-inf'), float('+inf'))


@dataclass
class HottestDay:
    date:str
    temp:int

    def default_hottest_day():
        return HottestDay('',float('-inf'))


def year_report(directory):
    results = defaultdict(WeatherData.default_weather_data)
    filenames = os.listdir(directory + '/')
    for filename in filenames:
        year = int(str(filename).split('_')[2])
        data = results[year]
        file_handler = open(directory + filename)
        csv_data = csv.reader(file_handler, delimiter=',')
        data=process_year(csv_data, data)
        file_handler.close()

    print(f"{'Year':15}{'Max Temp':15}{'Min Temp':15}{'Max Humidity':15}{'Min Humidity':15}")
    print('-'*75)
    for key in sorted(results.keys()):
        data=results[key]
        print(f'{key:<15}{data.max_temp:<15}{data.min_temp:<15}{data.max_hum:<15}{data.min_hum:<15}')

def process_year(csv_data, data: WeatherData):
    def my_min(row,prev_value,index):
        if not row[index]:
            return prev_value
        return min(prev_value,int(row[index]))
    
    def my_max(row,prev_value,index):
        if not row[index]:
            return prev_value
        return max(prev_value,int(row[index]))

    header=next(csv_data)
    if not header:
        header=next(csv_data)
    index_of_min_temp=header.index('Min TemperatureC')
    index_of_max_temp=header.index('Max TemperatureC')
    index_of_min_hum=header.index(' Min Humidity')
    index_of_max_hum=header.index('Max Humidity')
    for row in csv_data:
        if not row or len(row)==1:
            continue
        data.min_temp=my_min(row,data.min_temp,index_of_min_temp)
        data.min_hum=my_min(row,data.min_hum,index_of_min_hum)
        data.max_temp=my_max(row,data.max_temp,index_of_max_temp)
        data.max_hum=my_max(row,data.max_hum,index_of_max_hum)
    return data

def hottest_day(directory):
    filenames = os.listdir(directory + '/')
    results = defaultdict(HottestDay.default_hottest_day)
    for filename in filenames:
        year = int(str(filename).split('_')[2])
        data = results[year]
        file_handler = open(directory + filename)
        csv_data = csv.reader(file_handler, delimiter=',')
        data=process_hottest_day(csv_data, data)
        file_handler.close()
    
    print(f"{'Year':15}{'Date':15}{'Temperature':15}")
    print("-"*45)
    for year in sorted(results.keys()):
        print(f'{year:<15}{results[year].date:<15}{results[year].temp:<15}')

def process_hottest_day(csv_data,data: HottestDay):
    header=next(csv_data)
    if not header:
        header=next(csv_data)
    index_of_temp=header.index('Max TemperatureC')
    index_of_date=-1
    if 'PKST' in header:
        index_of_date=header.index('PKST')
    else:
        index_of_date=header.index('PKT')
    for row in csv_data:
        if not row or len(row)==1:
            continue
        if row[index_of_temp] and int(row[index_of_temp])>data.temp :
            data.temp=int(row[index_of_temp])
            data.date=row[index_of_date]
    return data

def main():

    parser=argparse.ArgumentParser(description='Weather Report')
    parser.add_argument('report',type=int,help='1 for Annual Report, 2 for Hottest Day')
    parser.add_argument('data_dir',type=str,help='Directory containing weather data')
    args=parser.parse_args()
    if (args.report==1):
        year_report(args.data_dir)
    else:
        hottest_day(args.data_dir)

if __name__=='__main__':
        main()
