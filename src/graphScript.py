__author__ = "Jonathan Mo"
__credits__ = ["Jonathan Mo"]
__email__ = "jonathanwm8@gmail.com"

import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import math
import os

def roundup(x):
    '''
    rounds values for y axis up to nearest 100
    :param x: int y tick value
    :return: int y tick value rounded up to closest 100
    '''
    return int(math.ceil(x / 100.0)) * 100

def find_dates(graph_type):
    '''
    finds the dates in ourworldindata.org csv file
    :param graph_type: string of graph type
    :return: a list of dates
    '''
    datafile = urllib.request.urlopen('https://covid.ourworldindata.org/data/ecdc/' + graph_type)
    dates_list = []
    for line in datafile.readlines():
        line = line.decode('utf-8').strip()
        row = line.split(",")

        dates_list.append(row[0])
    datafile.close()
    return dates_list

def find_cases(column, graph_type):
    '''
    finds total cases for given population (world or country)
    :param column: the column number for csv file
    :param graph_type: string of graph type
    :return: a list of total cases for inputted location
    '''
    datafile = urllib.request.urlopen('https://covid.ourworldindata.org/data/ecdc/' + graph_type)
    num_cases = []
    for line in datafile.readlines():
        line = line.decode('utf-8').strip()
        row = line.split(",")

        num_cases.append(row[column])
    datafile.close()
    return num_cases

def find_index(country, graph_type):
    '''
    finds index of country in csv file
    :param country: string of inputted country
    :param graph_type: string of graph type
    :return: index (column) that the country is located in the csv file
    '''
    datafile = urllib.request.urlopen('https://covid.ourworldindata.org/data/ecdc/' + graph_type)
    line = datafile.readline()
    line = line.decode('utf-8').strip()
    countries_list = line.split(",")
    index = countries_list.index(country)
    return index

def plot_single(country, graph_type):
    '''
    plot total cases vs. dates starting from 2020-01-01
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

    index = find_index(country, csv)                    # find index of country in csv file
    dates_list = find_dates(csv)                        # get full list of dates in csv file
    cases_strs = find_cases(index, csv)                 # get full list of cases in csv file
    cases_strs = cases_strs[1:]                         # get rid of first column
    dates_list = dates_list[1:]                         # get rid of first row

    total_cases_ints = []
    for i in cases_strs:                                # convert elements in list to int
        if (i == ""):                                   # check for when csv file has empty string instead of 0
            i = 0
        total_cases_ints.append(int(i))
    if (total_cases_ints[-1] == 0):                           # check if today's (most recent) data was not published
        total_cases_ints[-1] = total_cases_ints[-2]

    cases_aot = total_cases_ints[-1]                          # most recent case number, aot = as of today
    date_aot = dates_list[-1]                           # most recent date, aot = as of today
    highest_cases = max(total_cases_ints)

    my_graph = plt
    my_graph.figure(figsize=(15, 7.5))                  # set figure size
    my_graph.plot(dates_list, total_cases_ints, color = 'red')               # graph the data as cases vs. dates

    my_graph.xticks(np.arange(1, len(dates_list), 7))   # show ticks on xaxis spaced out by week (7 days)
    my_graph.xticks(rotation=30)                        # angle labels to show better
    print(highest_cases)
    ystepsize = 0
    if highest_cases <= 10:
        ystepsize = 1
    elif highest_cases <= 20:
        ystepsize = 2
    elif highest_cases <= 50:
        ystepsize = 5
    elif highest_cases <= 100:
        ystepsize = 10
    elif highest_cases <= 200:
        ystepsize = 15
    elif highest_cases <= 500:
        ystepsize = 30
    elif highest_cases <= 1000:
        ystepsize = 50
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
    elif highest_cases <= 250000:
        ystepsize = 12500
    elif highest_cases <= 500000:
        ystepsize = 25000
    elif highest_cases <= 1500000:
        ystepsize = 75000
    elif highest_cases <= 2500000:
        ystepsize = 125000
    elif highest_cases <= 3000000:
        ystepsize = 150000
    elif highest_cases <= 3500000:
        ystepsize = 175000
    elif highest_cases <= 4000000:
        ystepsize = 200000
    elif highest_cases <= 4500000:
        ystepsize = 275000
    elif highest_cases <= 5000000:
        ystepsize = 250000
    elif highest_cases <= 6000000:
        ystepsize = 300000
    else:
        ystepsize = 400000

    ylabel = np.arange(0, int(highest_cases*1.1), ystepsize)
                                                                            # have yticks go 1.1 times above highest data point,
    my_graph.yticks(ylabel, ylabel, rotation=30)                            # rotate ticks to show numbers better

    my_graph.autoscale(enable=True, axis='x', tight=True)                   # tight bound it
    my_graph.grid(True)
    myStr = str(cases_aot) + " " + graph_type.title()
    my_graph.annotate((str(date_aot)+":").center(len(myStr)) + "\n" + myStr, xy=(date_aot, cases_aot), xycoords='data', xytext=(dates_list[-15],1.1*highest_cases), textcoords='data', arrowprops=dict(arrowstyle='->', color='black', lw = 2)) # label last point on graph
    my_graph.title('Covid-19 ' + graph_type.title() + ' Across ' + country.title())      #label things
    my_graph.xlabel('Date')
    my_graph.ylabel('Number of Cases')
    graph_type = graph_type.replace(" ", "_")                               # change graph name to replace spaces with underscores
    country = country.lower().replace(" ", "_")

    dir_path = os.path.dirname(os.path.realpath(__file__))                  # get working directory
    if not os.path.exists(dir_path +"/graphs/"+ country):                   # if directory for that country is not yet made, make it
        os.makedirs(dir_path + "/graphs/" + country)
    plt.savefig(dir_path + "/graphs/" + country + "/" + country + "_" + graph_type + "_" + date_aot + ".png") # save to that directory

    my_graph.show()


def plot_four(country):
    '''
    plot total cases, total deaths, new cases, new deaths starting from 2020-01-01
    :param country: string of inputted country
    :return: void
    '''
    my_graph = plt
    my_graph.figure(figsize=(15, 7.5))                                      # set figure size


    total_cases = "total_cases.csv"
    total_deaths = "total_deaths.csv"
    new_cases = "new_cases.csv"
    new_deaths = "new_deaths.csv"
    graph_type = "Total Cases, Total Deaths, New Cases, and New Deaths"

    total_cases_index = find_index(country, total_cases)                    # find index of country in total cases csv file
    total_cases_dates_list = find_dates(total_cases)                        # get full list of dates in total cases csv file
    total_cases_strs = find_cases(total_cases_index, total_cases)           # get full list of cases in total cases csv file
    total_cases_strs = total_cases_strs[1:]                                 # get rid of first column
    total_cases_dates_list = total_cases_dates_list[1:]                     # get rid of first row

    total_cases_ints = []
    for i in total_cases_strs:                                              # convert elements in list to int
        if (i == ""):                                                       # check for when csv file has empty string instead of 0
            i = 0
        total_cases_ints.append(int(i))
    if (total_cases_ints[-1] == 0):                                         # check if today's (most recent) data was not published
        total_cases_ints[-1] = total_cases_ints[-2]

    my_graph.plot(total_cases_dates_list, total_cases_ints, color = 'blue', label = "Total Cases " + "in " + country + ": " + str(total_cases_ints[-1]))  # graph the data as total cases vs. dates


    total_deaths_index = find_index(country, total_deaths)                  # find index of country in total deaths csv file
    total_deaths_dates_list = find_dates(total_deaths)                      # get full list of dates in total deaths csv file
    total_deaths_strs = find_cases(total_deaths_index, total_deaths)        # get full list of cases in total deaths csv file
    total_deaths_strs = total_deaths_strs[1:]                               # get rid of first column
    total_deaths_dates_list = total_deaths_dates_list[1:]                   # get rid of first row

    total_deaths_ints = []
    for i in total_deaths_strs:                                             # convert elements in list to int
        if (i == ""):                                                       # check for when csv file has empty string instead of 0
            i = 0
        total_deaths_ints.append(int(i))
    if (total_deaths_ints[-1] == 0):                                        # check if today's (most recent) data was not published
        total_deaths_ints[-1] = total_deaths_ints[-2]

    my_graph.plot(total_deaths_dates_list, total_deaths_ints, color='red', label = "Total Deaths " + "in " + country + ": " + str(total_deaths_ints[-1]))  # graph the data as total deaths vs. dates

    new_cases_index = find_index(country, new_cases)                        # find index of country in new cases csv file
    new_cases_dates_list = find_dates(new_cases)                            # get full list of dates in new cases csv file
    new_cases_strs = find_cases(new_cases_index, new_cases)                 # get full list of cases in new cases csv file
    new_cases_strs = new_cases_strs[1:]                                     # get rid of first column
    new_cases_dates_list = new_cases_dates_list[1:]                         # get rid of first row

    new_cases_ints = []
    for i in new_cases_strs:                                                # convert elements in list to int
        if (i == ""):                                                       # check for when csv file has empty string instead of 0
            i = 0
        new_cases_ints.append(int(i))
    if (new_cases_ints[-1] == 0):                                           # check if today's (most recent) data was not published
        new_cases_ints[-1] = new_cases_ints[-2]

    my_graph.plot(new_cases_dates_list, new_cases_ints, color='green', label = "New Cases " + "in " + country + ": " + str(new_cases_ints[-1]))  # graph the data as new cases vs. dates

    new_deaths_index = find_index(country, new_deaths)                      # find index of country in new deaths csv file
    new_deaths_dates_list = find_dates(new_deaths)                          # get full list of dates in new deaths csv file
    new_deaths_strs = find_cases(new_deaths_index, new_deaths)              # get full list of cases in new deaths csv file
    new_deaths_strs = new_deaths_strs[1:]                                   # get rid of first column
    new_deaths_dates_list = new_deaths_dates_list[1:]                       # get rid of first row

    new_deaths_ints = []
    for i in new_deaths_strs:                                               # convert elements in list to int
        if (i == ""):                                                       # check for when csv file has empty string instead of 0
            i = 0
        new_deaths_ints.append(int(i))
    if (new_deaths_ints[-1] == 0):                                          # check if today's (most recent) data was not published
        new_deaths_ints[-1] = new_deaths_ints[-2]

    my_graph.plot(new_deaths_dates_list, new_deaths_ints, color='orange', label = "New Deaths " + "in " + country + ": " + str(new_deaths_ints[-1]))  # graph the data as new deaths vs. dates

    total_cases_aot = total_cases_ints[-1]                                  # most recent case number, aot = as of today
    date_aot = total_cases_dates_list[-1]                                   # most recent date, aot = as of today
    highest_cases = max(total_cases_ints)


    my_graph.xticks(np.arange(1, len(total_cases_dates_list), 7))           # show ticks on xaxis spaced out by week (7 days)
    my_graph.xticks(rotation=30)                                            # angle labels to show better
    ystepsize = 0
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

    ylabel = (np.arange(0, int(highest_cases*1.1), ystepsize)).tolist()
    my_graph.yticks(ylabel, ylabel, rotation=30)                            # rotate ticks to show numbers better

    my_graph.autoscale(enable=True, axis='x', tight=True)                   # tight bound it
    my_graph.grid(True)


    my_graph.title('Covid-19 ' + graph_type.title() + ' Across ' + country.title() + ' as of ' + date_aot)  # label things
    my_graph.xlabel('Date')
    my_graph.ylabel('Number of Cases')
    my_graph.legend(loc="upper left")
    plt.savefig("/Users/jonathanmo/Desktop/Jomoswork/jonathanwmo.github.io/src/graphs/" + country +"/" + country.replace(" ","_").title() + "_" + "allfour_"+ date_aot + ".png")

    my_graph.show()

country = input("Input a country: ").title()
graph_type = input("Choose graph (total confirmed cases, total deaths, new confirmed cases, or new deaths): ").lower()
plot_single(country, graph_type)
# plot_four(country)