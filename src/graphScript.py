#!/usr/bin/python3

__author__ = "Jonathan Mo"
__credits__ = ["Jonathan Mo"]
__email__ = "jm9hx@virginia.edu"

import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import time
import gc



def find_dates(graph_type: str):
    '''
    finds the dates in ourworldindata.org csv file
    :param graph_type: string of graph type
    :return: a list of dates as strings
    '''
    datafile = urllib.request.urlopen(
        'https://covid.ourworldindata.org/data/ecdc/' + graph_type)
    dates_list = []

    for line in datafile.readlines():
        line = line.decode('utf-8').strip()
        row = line.split(",")
        dates_list.append(row[0])
    datafile.close()
    return dates_list


def find_cases(column: int, graph_type: str):
    '''
    finds total cases for given population (world or country)
    :param column: the column number for csv file
    :param graph_type: string of graph type
    :return: a list of total cases (or deaths) for inputted location
    '''
    datafile = urllib.request.urlopen(
        'https://covid.ourworldindata.org/data/ecdc/' + graph_type)
    num_cases = []

    for line in datafile.readlines():
        line = line.decode('utf-8').strip()
        row = line.split(",")
        num_cases.append(row[column])
    datafile.close()
    return num_cases


def find_index(country: str, graph_type: str):
    '''
    finds index of country in csv file
    :param country: string of inputted country
    :param graph_type: string of graph type
    :return: index (column) that the country is located in the csv file
    '''
    datafile = urllib.request.urlopen(
        'https://covid.ourworldindata.org/data/ecdc/' + graph_type)
    line = datafile.readline()
    line = line.decode('utf-8').strip()
    countries_list = line.split(",")
    index = countries_list.index(country)
    datafile.close()
    return index


def plot_single(country: str, graph_type: str):
    '''
    plot total/new cases or total/new deaths vs. dates starting from 2020-01-01
    :param country: string of inputted country
    :param graph_type: string of graph type
    :return: void
    '''
    csv = ''
    if (graph_type == "total confirmed cases"):
        csv = "total_cases.csv"
    if (graph_type == "total deaths"):
        csv = "total_deaths.csv"
    if (graph_type == "new confirmed cases"):
        csv = "new_cases.csv"
    if (graph_type == "new deaths"):
        csv = "new_deaths.csv"

    # handle edge cases for when country name is different between websites
    if " And" in country:
        country = country.replace("And", "and")
    if "Cote D'Ivoire" in country:
        country = "Cote d'Ivoire"
    if " Of" in country:
        country = country.replace("Of", "of")
    if " The" in country:
        country = country.replace("The", "the")
    if "Sint Maarten (Dutch Part)" in country:
        country = "Sint Maarten (Dutch part)"

    # find index of country in csv file
    index = find_index(country, graph_type)
    # get full list of dates in csv file
    dates_list = find_dates(csv)
    # get full list of cases/deaths in csv file
    cases_strs = find_cases(index, csv)

    # if country is china, set x-axis dates to be earlier for they're data occurring earlier
    if (country.lower() == "china"):
        # make China graph start from Jan 15
        cases_strs = cases_strs[15:]
        dates_list = dates_list[15:]
    else:
        # make all other country graphs start on ~march 4
        cases_strs = cases_strs[64:]
        dates_list = dates_list[64:]

    total_cases_ints = []
    for i in cases_strs:
        # check for when csv file has empty string instead of 0
        if (i == ""):
            i = 0
        total_cases_ints.append(int(i))

    # check if today's (most recent) data was not published
    if (total_cases_ints[-1] == 0):
        total_cases_ints[-1] = total_cases_ints[-2]

    # most recent case/death/date number, aot = as of today
    cases_aot = total_cases_ints[-1]
    # imported datetime to get str and sliced string to only show date, no hours/minutes
    date_aot = str(datetime.today())[0:10]
    highest_cases = max(total_cases_ints)

    my_graph = plt
    my_graph.figure(figsize=(15, 7.5))
    # graph the data as cases (or deaths) vs. dates in red
    my_graph.plot(dates_list, total_cases_ints, color='red')

    # show ticks on xaxis spaced out by week (7 days)
    my_graph.xticks(np.arange(1, len(dates_list), 7))
    # angle labels to show better
    my_graph.xticks(rotation=30)

    # manually space out the y-axis spacings
    if highest_cases <= 10:
        ystepsize = 1
    elif highest_cases <= 20:
        ystepsize = 2
    elif highest_cases <= 50:
        ystepsize = 5
    elif highest_cases <= 100:
        ystepsize = 10
    elif highest_cases <= 200:
        ystepsize = 20
    elif highest_cases <= 500:
        ystepsize = 30
    elif highest_cases <= 1000:
        ystepsize = 50
    elif highest_cases <= 2000:
        ystepsize = 100
    elif highest_cases <= 3000:
        ystepsize = 200
    elif highest_cases <= 4000:
        ystepsize = 200
    elif highest_cases <= 5000:
        ystepsize = 250
    elif highest_cases <= 10000:
        ystepsize = 500
    elif highest_cases <= 20000:
        ystepsize = 1000
    elif highest_cases <= 50000:
        ystepsize = 2500
    elif highest_cases <= 100000:
        ystepsize = 5000
    elif highest_cases <= 200000:
        ystepsize = 10000
    elif highest_cases <= 500000:
        ystepsize = 25000
    elif highest_cases <= 1000000:
        ystepsize = 50000
    elif highest_cases <= 2500000:
        ystepsize = 100000
    elif highest_cases <= 3000000:
        ystepsize = 200000
    elif highest_cases <= 3500000:
        ystepsize = 200000
    elif highest_cases <= 4000000:
        ystepsize = 250000
    elif highest_cases <= 4500000:
        ystepsize = 250000
    elif highest_cases <= 5000000:
        ystepsize = 500000
    elif highest_cases <= 6000000:
        ystepsize = 500000
    else:
        ystepsize = 500000

    # use np.arange to make y-axis slightly larger (1.1 times) than highest y-value on graph
    ylabel = np.arange(0, int(highest_cases * 1.1), ystepsize)
    # rotate ticks to show numbers better
    my_graph.yticks(ylabel, ylabel, rotation=30)

    my_graph.autoscale(
        enable=True,
        axis='x',
        tight=True)
    my_graph.grid(True)
    myStr = str(date_aot) + ": " + str(cases_aot)

    # annotate graph to show date and value of most recent date along with an arrow pointing to said value
    my_graph.annotate(
                      (myStr).center(len(myStr)) + "\n" + graph_type.title(),
                      xy=(date_aot, cases_aot),
                      xycoords='data',
                      xytext=(dates_list[-2], 1.1 * highest_cases),
                      textcoords='data',
                      arrowprops=dict(arrowstyle='->',
                                      color='black',
                                      lw=2))  # label last point on graph with an arrow
    # set title of graph
    my_graph.title('Covid-19 ' + graph_type.title() + ' Across ' + country.title() + " as of " + date_aot,
        fontsize=14,
        weight='bold')  # label things
    my_graph.xlabel('Date', fontsize=12, weight='bold')

    # set y-axis label of graph depending on graph type
    if "death" in graph_type.lower() or "deaths" in graph_type.lower():
        my_graph.ylabel('Number of Deaths', fontsize=12, weight='bold')
    else:
        my_graph.ylabel('Number of Cases', fontsize=12, weight='bold')

    # change graph name to replace spaces with underscores for purpose of saving as a .png file
    graph_type = graph_type.replace(" ", "_")
    country = country.lower().replace(" ", "_")

    # get working directory
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/graphs/" + country

    # if directory for that country is not yet made, make it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # save to that directory
    plt.savefig(dir_path + "/" + country + "_" + graph_type + "_" + date_aot + ".png",
        dpi=500,
        transparent=True)

    # to reclaim memory after each function call
    my_graph.clf()
    my_graph.close('all')
    gc.collect()


def plot_four(country: str):
    '''
    plot total cases, total deaths, new cases, new deaths starting from 2020-01-01
    :param country: string of inputted country
    :return: void
    '''
    my_graph = plt
    my_graph.figure(figsize=(15, 7.5))

    # handle edge cases for when countries are named differently between websites
    if " And" in country:
        country = country.replace("And", "and")
    if "Cote D'Ivoire" in country:
        country = "Cote d'Ivoire"
    if " Of" in country:
        country = country.replace("Of", "of")
    if " The" in country:
        country = country.replace("The", "the")
    if "Sint Maarten (Dutch Part)" in country:
        country = "Sint Maarten (Dutch part)"

    total_cases = "total_cases.csv"
    total_deaths = "total_deaths.csv"
    new_cases = "new_cases.csv"
    new_deaths = "new_deaths.csv"
    graph_type = "Total Cases, Total Deaths, New Cases, and New Deaths"

    ############################################### GRAPH TOTAL CASES ###############################################
    # find index of country in total cases csv file
    total_cases_index = find_index(country, total_cases)
    # get full list of dates in total cases csv file
    total_cases_dates_list = find_dates(total_cases)
    # get full list of cases in total cases csv file
    total_cases_strs = find_cases(total_cases_index, total_cases)

    # if country is china, set x-axis dates to be earlier for they're data occurring earlier
    if (country.lower() == "china"):
        # make china start on jan 15
        total_cases_strs = total_cases_strs[15:]
        total_cases_dates_list = total_cases_dates_list[15:]
    else:
        # otherwise country starts on ~march 3
        total_cases_strs = total_cases_strs[64:]
        total_cases_dates_list = total_cases_dates_list[64:]

    total_cases_ints = []
    for i in total_cases_strs:
        # check for when csv file has empty string instead of 0
        if (i == ""):
            i = 0
        total_cases_ints.append(int(i))
    # check if today's (most recent) data was not published
    if (total_cases_ints[-1] == 0):
        total_cases_ints[-1] = total_cases_ints[-2]

    # graph the data as total cases vs. dates, label in blue
    my_graph.plot(total_cases_dates_list, total_cases_ints, color='blue', label="Total Cases " +
                  "in " + country + ": " + str(total_cases_ints[-1]))


    ############################################### GRAPH TOTAL DEATHS ###############################################
    # find index of country in total deaths csv file
    total_deaths_index = find_index(country, total_deaths)
    # get full list of dates in total deaths csv file
    total_deaths_dates_list = find_dates(total_deaths)
    # get full list of cases in total deaths csv file
    total_deaths_strs = find_cases(total_deaths_index, total_deaths)

    # if country is china, set x-axis dates to be earlier for they're data occurring earlier
    if (country.lower() == "china"):
        # make china start on jan 15
        total_deaths_strs = total_deaths_strs[15:]
        total_deaths_dates_list = total_deaths_dates_list[15:]
    else:
        # otherwise country starts on ~march 3
        total_deaths_strs = total_deaths_strs[64:]
        total_deaths_dates_list = total_deaths_dates_list[64:]

    total_deaths_ints = []
    for i in total_deaths_strs:
        # check for when csv file has empty string instead of 0
        if (i == ""):
            i = 0
        total_deaths_ints.append(int(i))
    # check if today's (most recent) data was not published
    if (total_deaths_ints[-1] == 0):
        total_deaths_ints[-1] = total_deaths_ints[-2]

    # graph the data as total deaths vs. dates, label in red
    my_graph.plot(total_deaths_dates_list, total_deaths_ints, color='red', label="Total Deaths " +
                  "in " + country + ": " + str(total_deaths_ints[-1]))


    ################################################ GRAPH NEW CASES ################################################
    # find index of country in new cases csv file
    new_cases_index = find_index(country, new_cases)
    # get full list of dates in new cases csv file
    new_cases_dates_list = find_dates(new_cases)
    # get full list of cases in new cases csv file
    new_cases_strs = find_cases(new_cases_index, new_cases)

    # if country is china, set x-axis dates to be earlier for they're data occurring earlier
    if (country.lower() == "china"):
        # make china start on jan 15
        new_cases_strs = new_cases_strs[15:]
        new_cases_dates_list = new_cases_dates_list[15:]
    else:
        # otherwise country starts on ~march 3
        new_cases_strs = new_cases_strs[64:]
        new_cases_dates_list = new_cases_dates_list[64:]

    new_cases_ints = []
    for i in new_cases_strs:
        # check for when csv file has empty string instead of 0
        if (i == ""):
            i = 0
        new_cases_ints.append(int(i))
    # check if today's (most recent) data was not published
    if (new_cases_ints[-1] == 0):
        new_cases_ints[-1] = new_cases_ints[-2]

    # graph the data as new cases vs. dates, label in green
    my_graph.plot(new_cases_dates_list, new_cases_ints, color='green', label="New Cases " +
                  "in " + country + ": " + str(new_cases_ints[-1]))


    ################################################ GRAPH NEW DEATHS ################################################
    # find index of country in new deaths csv file
    new_deaths_index = find_index(country, new_deaths)
    # get full list of dates in new deaths csv file
    new_deaths_dates_list = find_dates(new_deaths)
    # get full list of cases in new deaths csv file
    new_deaths_strs = find_cases(new_deaths_index, new_deaths)

    # if country is china, set x-axis dates to be earlier for they're data occurring earlier
    if (country.lower() == "china"):
        # make china start on jan 15
        new_deaths_strs = new_deaths_strs[15:]
        new_deaths_dates_list = new_deaths_dates_list[15:]
    else:
        # make all other country graphs start on ~march 3
        new_deaths_strs = new_deaths_strs[64:]
        new_deaths_dates_list = new_deaths_dates_list[64:]

    new_deaths_ints = []
    for i in new_deaths_strs:
        # check for when csv file has empty string instead of 0
        if (i == ""):
            i = 0
        new_deaths_ints.append(int(i))
    # check if today's (most recent) data was not published
    if (new_deaths_ints[-1] == 0):
        new_deaths_ints[-1] = new_deaths_ints[-2]

    # graph the data as new deaths vs. dates, label in orange
    my_graph.plot(new_deaths_dates_list, new_deaths_ints, color='orange', label="New Deaths " +
                  "in " + country + ": " + str(new_deaths_ints[-1]))

    # most recent date, aot = as of today
    date_aot = str(datetime.today())[0:10]
    highest_cases = max(total_cases_ints)

    # show ticks on xaxis spaced out by week (7 days)
    my_graph.xticks(np.arange(1, len(total_cases_dates_list), 7))
    # angle labels to show better
    my_graph.xticks(rotation=30)

    # manually space out the y-axis spacings
    if highest_cases <= 10:
        ystepsize = 1
    elif highest_cases <= 20:
        ystepsize = 2
    elif highest_cases <= 50:
        ystepsize = 5
    elif highest_cases <= 100:
        ystepsize = 10
    elif highest_cases <= 200:
        ystepsize = 20
    elif highest_cases <= 500:
        ystepsize = 30
    elif highest_cases <= 1000:
        ystepsize = 50
    elif highest_cases <= 2000:
        ystepsize = 100
    elif highest_cases <= 3000:
        ystepsize = 200
    elif highest_cases <= 4000:
        ystepsize = 200
    elif highest_cases <= 5000:
        ystepsize = 250
    elif highest_cases <= 10000:
        ystepsize = 500
    elif highest_cases <= 20000:
        ystepsize = 1000
    elif highest_cases <= 50000:
        ystepsize = 2500
    elif highest_cases <= 100000:
        ystepsize = 5000
    elif highest_cases <= 200000:
        ystepsize = 10000
    elif highest_cases <= 500000:
        ystepsize = 25000
    elif highest_cases <= 1000000:
        ystepsize = 50000
    elif highest_cases <= 2500000:
        ystepsize = 100000
    elif highest_cases <= 3000000:
        ystepsize = 200000
    elif highest_cases <= 3500000:
        ystepsize = 200000
    elif highest_cases <= 4000000:
        ystepsize = 250000
    elif highest_cases <= 4500000:
        ystepsize = 250000
    elif highest_cases <= 5000000:
        ystepsize = 500000
    elif highest_cases <= 6000000:
        ystepsize = 500000
    else:
        ystepsize = 500000

    # use np.arange to make y-axis slightly larger (1.1 times) than highest y-value on graph
    ylabel = (np.arange(0, int(highest_cases * 1.1), ystepsize)).tolist()
    # rotate ticks to show numbers better
    my_graph.yticks(ylabel, ylabel, rotation=30)

    my_graph.autoscale(
        enable=True,
        axis='x',
        tight=True)                   # tight bound it
    my_graph.grid(True)

    my_graph.title(
        'Covid-19 ' +
        graph_type.title() +
        ' Across ' +
        country.title() +
        ' as of ' +
        date_aot,
        fontsize=14,
        weight='bold')  # label things
    my_graph.xlabel('Date', fontsize='12', weight='bold')
    my_graph.ylabel('Number of Cases', fontsize='12', weight='bold')
    my_graph.legend(loc="upper left")

    # change graph name to replace spaces with underscores for purpose of saving as png
    country = country.lower().replace(" ", "_")
    # get working directory
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/graphs/" + country

    # if directory for that country is not yet made, make it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    plt.savefig(dir_path + "/" + country + "_allfour_" + date_aot + ".png",
        dpi=500,
        transparent=True)  # save to that directory

    # to reclaim memory after each function call
    my_graph.clf()
    my_graph.close('all')
    gc.collect()

countries = [
    'World',
    'Afghanistan',
    'Albania',
    'Algeria',
    'Andorra',
    'Angola',
    'Anguilla',
    'Antigua and Barbuda',
    'Argentina',
    'Armenia',
    'Aruba',
    'Australia',
    'Austria',
    'Azerbaijan',
    'Bahamas',
    'Bahrain',
    'Bangladesh',
    'Barbados',
    'Belarus',
    'Belgium',
    'Belize',
    'Benin',
    'Bermuda',
    'Bhutan',
    'Bolivia',
    'Bonaire Sint Eustatius and Saba',
    'Bosnia and Herzegovina',
    'Botswana',
    'Brazil',
    'British Virgin Islands',
    'Brunei',
    'Bulgaria',
    'Burkina Faso',
    'Burundi',
    'Cambodia',
    'Cameroon',
    'Canada',
    'Cape Verde',
    'Cayman Islands',
    'Central African Republic',
    'Chad',
    'Chile',
    'China',
    'Colombia',
    'Comoros',
    'Congo',
    'Costa Rica',
    "Cote d'Ivoire",
    'Croatia',
    'Cuba',
    'Curacao',
    'Cyprus',
    'Czech Republic',
    'Democratic Republic of Congo',
    'Denmark',
    'Djibouti',
    'Dominica',
    'Dominican Republic',
    'Ecuador',
    'Egypt',
    'El Salvador',
    'Equatorial Guinea',
    'Eritrea',
    'Estonia',
    'Ethiopia',
    'Faeroe Islands',
    'Falkland Islands',
    'Fiji',
    'Finland',
    'France',
    'French Polynesia',
    'Gabon',
    'Gambia',
    'Georgia',
    'Germany',
    'Ghana',
    'Gibraltar',
    'Greece',
    'Greenland',
    'Grenada',
    'Guam',
    'Guatemala',
    'Guernsey',
    'Guinea',
    'Guinea-Bissau',
    'Guyana',
    'Haiti',
    'Honduras',
    'Hungary',
    'Iceland',
    'India',
    'Indonesia',
    'Iran',
    'Iraq',
    'Ireland',
    'Isle of Man',
    'Israel',
    'Italy',
    'Jamaica',
    'Japan',
    'Jersey',
    'Jordan',
    'Kazakhstan',
    'Kenya',
    'Kosovo',
    'Kuwait',
    'Kyrgyzstan',
    'Laos',
    'Latvia',
    'Lebanon',
    'Liberia',
    'Libya',
    'Liechtenstein',
    'Lithuania',
    'Luxembourg',
    'Macedonia',
    'Madagascar',
    'Malawi',
    'Malaysia',
    'Maldives',
    'Mali',
    'Malta',
    'Mauritania',
    'Mauritius',
    'Mexico',
    'Moldova',
    'Monaco',
    'Mongolia',
    'Montenegro',
    'Montserrat',
    'Morocco',
    'Mozambique',
    'Myanmar',
    'Namibia',
    'Nepal',
    'Netherlands',
    'New Caledonia',
    'New Zealand',
    'Nicaragua',
    'Niger',
    'Nigeria',
    'Northern Mariana Islands',
    'Norway',
    'Oman',
    'Pakistan',
    'Palestine',
    'Panama',
    'Papua New Guinea',
    'Paraguay',
    'Peru',
    'Philippines',
    'Poland',
    'Portugal',
    'Puerto Rico',
    'Qatar',
    'Romania',
    'Russia',
    'Rwanda',
    'Saint Kitts and Nevis',
    'Saint Lucia',
    'Saint Vincent and the Grenadines',
    'San Marino',
    'Sao Tome and Principe',
    'Saudi Arabia',
    'Senegal',
    'Serbia',
    'Seychelles',
    'Sierra Leone',
    'Singapore',
    'Sint Maarten (Dutch part)',
    'Slovakia',
    'Slovenia',
    'Somalia',
    'South Africa',
    'South Korea',
    'South Sudan',
    'Spain',
    'Sri Lanka',
    'Sudan',
    'Suriname',
    'Swaziland',
    'Sweden',
    'Switzerland',
    'Syria',
    'Taiwan',
    'Tajikistan',
    'Tanzania',
    'Thailand',
    'Timor',
    'Togo',
    'Trinidad and Tobago',
    'Tunisia',
    'Turkey',
    'Turks and Caicos Islands',
    'Uganda',
    'Ukraine',
    'United Arab Emirates',
    'United Kingdom',
    'United States',
    'United States Virgin Islands',
    'Uruguay',
    'Uzbekistan',
    'Vatican',
    'Venezuela',
    'Vietnam',
    'Western Sahara',
    'Yemen',
    'Zambia',
    'Zimbabwe']

for country in countries:
    plot_single(country.title(), "total confirmed cases")
    plot_single(country.title(), "total deaths")
    plot_single(country.title(), "new confirmed cases")
    plot_single(country.title(), "new deaths")
    plot_four(country)
    index = str(countries.index(country) + 1)
    # see progress of updating graphs
    print(country + ": " + index + "/" + str(len(countries)))

    # delete png files of graphs older than 1 day in each country folder to avoid overcrowding after updating
    dir_path = os.path.dirname(os.path.realpath(
        __file__)) + "/graphs/" + country.lower().replace(" ", "_")  # get working directory
    current_time = time.time()
    for f in os.listdir(dir_path):
        f = dir_path + "/" + f
        creation_time = os.path.getmtime(f)
        if ((current_time - creation_time) / (86400)) >= 1:
            os.remove(f)
