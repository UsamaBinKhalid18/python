import csv
import os
import sys


def yearReport(address):
    results = {}
    files = os.listdir(sys.argv[2]+'/')
    for filename in files:
        year = int(str(filename).split('_')[2])
        if year in results.keys():
            max_temp = results[year][0]
            min_temp = results[year][1]
            max_hum = results[year][2]
            min_hum = results[year][3]
        else:
            max_temp = 0
            min_temp = 100
            min_hum = 100
            max_hum = 0
        with open(address+filename) as file:
            csv_reader = csv.reader(file, delimiter=',')
            row_count = 0
            for row in csv_reader:
                if row:
                    if row_count == 0:
                        row_len = len(row)
                        index_of_max_temp = row.index('Max TemperatureC')
                        index_of_min_temp = row.index('Min TemperatureC')
                        index_of_max_hum = row.index('Max Humidity')
                        index_of_min_hum = row.index(' Min Humidity')
                    elif len(row) == row_len:
                        if (row[index_of_max_temp]):
                            max_temp = max(max_temp, int(
                                row[index_of_max_temp]))

                        if (row[index_of_min_temp]):
                            min_temp = min(min_temp, int(
                                row[index_of_min_temp]))

                        if (row[index_of_max_hum]):
                            max_hum = max(max_hum, int(row[index_of_max_hum]))

                        if (row[index_of_min_hum]):
                            min_hum = min(min_hum, int(row[index_of_min_hum]))
                    row_count += 1
        results[year] = [max_temp, min_temp, max_hum, min_hum]


    print("\n%-15s%-15s%-15s%-15s%-15s" %
          ("Year", "MAX Temp", "MIN Temp", "MAX Humidity", "MIN Humidity"))
    print("-"*75)
    for key in sorted(results.keys()):
        res = results[key]
        print("%-15s%-15s%-15s%-15s%-15s" %
              (key, res[0], res[1], res[2], res[3]))


def hottestDay(address):
    files = os.listdir(sys.argv[2]+'/')
    results = {}
    for filename in files:
        year = int(str(filename).split('_')[2])
        if year in results.keys():
            day = results[year][0]
            temp = results[year][1]
        else:
            day = -1
            temp = 0
        with open(address+filename) as file:
            csv_reader = csv.reader(file, delimiter=',')
            row_count = 0
            for row in csv_reader:
                if row:
                    if row_count == 0:
                        row_len = len(row)
                        index_of_max_temp = row.index('Max TemperatureC')
                        if 'PKT' in row:
                            index_of_date = row.index('PKT')
                        else:
                            index_of_date = row.index('PKST')

                    elif len(row) == row_len:
                        if (row[index_of_max_temp] and int(row[index_of_max_temp]) > temp):
                            temp = int(row[index_of_max_temp])
                            day = row[index_of_date]

                    row_count += 1
        results[year] = [day, temp]


    print("\n%-15s%-15s%-15s" % ("Year", "Date", "Temprature"))
    print("-"*36)
    for key in sorted(results.keys()):
        print("%-15s%-15s%-15s" % (key, results[key][0], results[key][1]))


if len(sys.argv) != 3 or sys.argv[1] not in ["1", "2"]:
    print("""
    Usage: weatherman [report#] [data_dir]

    [Report #]
    1 for Annual Max/Min Temperature
    2 for Hottest day of each year

    [data_dir]
    Directory containing weather data files
    """)
    sys.exit()

if (sys.argv[1] == "1"):
    yearReport(sys.argv[2])
else:
    hottestDay(sys.argv[2])
