#!/usr/bin/python3

import datetime
from datetime import datetime, timedelta
import schedule
import os


def update_date(country):
    _country_ = country.lower().replace(" ", "_")
    country = country.lower().replace(" ", "")

    dir_path = os.path.dirname(os.path.realpath(__file__))[0:56] + "/" + country + ".html"
    print(dir_path)

    date_aot = str(datetime.today())[0:10]
    date_aoy = str(datetime.today() - timedelta(days=1))[0:10]
    date_ao2 = str(str(datetime.today() - timedelta(days=2))[0:10])
    date_ao3 = str(str(datetime.today() - timedelta(days=2))[0:10])

    with open(dir_path, 'r') as f:
        newstr = """"""
        for line in f.readlines():
            if date_aoy in line:
                newstr += line.replace(date_aoy, date_aot)
            elif date_ao2 in line:
                newstr += line.replace(date_ao2, date_aot)
            elif date_ao3 in line:
                newstr += line.replace(date_ao3, date_aot)
            else:
                newstr += line
    f.close()

    with open(dir_path, 'w') as f:
        f.write(newstr)

# if __name__ == "__main__":
#     country = str(sys.argv[1])
#     update_date(country)

mycountries = ['World', 'United States', 'United Kingdom', 'Italy', 'Spain', 'France', 'China']
for country in mycountries:
    update_date(country)
