__author__ = "Jonathan Mo"
__credits__ = ["Jonathan Mo"]
__email__ = "jm9hx@virginia.edu"

import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import os
import time




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
    if (country.lower() == "china"):
        cases_strs = cases_strs[15:]
        dates_list = dates_list[15:]
    else:
        cases_strs = cases_strs[64:]                               # get rid of first column
        dates_list = dates_list[64:]

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

    ylabel = np.arange(0, int(highest_cases*1.1), ystepsize)
                                                                            # have yticks go 1.1 times above highest data point,
    my_graph.yticks(ylabel, ylabel, rotation=30)                            # rotate ticks to show numbers better

    my_graph.autoscale(enable=True, axis='x', tight=True)                   # tight bound it
    my_graph.grid(True)
    myStr = str(date_aot) + ": " + str(cases_aot)
    my_graph.annotate((myStr).center(len(myStr)) + "\n" + graph_type.title(), xy=(date_aot, cases_aot), xycoords='data', xytext=(dates_list[-2],1.1*highest_cases), textcoords='data', arrowprops=dict(arrowstyle='->', color='black', lw = 2)) # label last point on graph
    my_graph.title('Covid-19 ' + graph_type.title() + ' Across ' + country.title() + " as of " + date_aot, fontsize=14, weight='bold')      #label things
    my_graph.xlabel('Date', fontsize=12, weight='bold')
    if "death" in graph_type.lower() or "deaths" in graph_type.lower():
        my_graph.ylabel('Number of Deaths', fontsize=12, weight='bold')
    else:
        my_graph.ylabel('Number of Cases', fontsize=12, weight='bold')
    graph_type = graph_type.replace(" ", "_")                               # change graph name to replace spaces with underscores
    country = country.lower().replace(" ", "_")


    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/graphs/" + country                # get working directory
    if not os.path.exists(dir_path):                   # if directory for that country is not yet made, make it
        os.makedirs(dir_path)
    plt.savefig(dir_path + "/" + country + "_" + graph_type + "_" + date_aot + ".png", dpi=500, transparent=True) # save to that directory

    current_time = time.time()
    for f in os.listdir(dir_path):
        f = dir_path + "/" + f
        creation_time = os.path.getmtime(f)
        if ((current_time - creation_time) / (86400)) >= 1:
            os.remove(f)

    # my_graph.show()
    my_graph.clf()
    my_graph.close('all')


def plot_four(country):
    '''
    plot total cases, total deaths, new cases, new deaths starting from 2020-01-01
    :param country: string of inputted country
    :return: void
    '''
    my_graph = plt
    my_graph.figure(figsize=(14, 8))                                      # set figure size


    total_cases = "total_cases.csv"
    total_deaths = "total_deaths.csv"
    new_cases = "new_cases.csv"
    new_deaths = "new_deaths.csv"
    graph_type = "Total Cases, Total Deaths, New Cases, and New Deaths"

    total_cases_index = find_index(country, total_cases)                    # find index of country in total cases csv file
    total_cases_dates_list = find_dates(total_cases)                        # get full list of dates in total cases csv file
    total_cases_strs = find_cases(total_cases_index, total_cases)           # get full list of cases in total cases csv file
    if (country.lower() == "china"):
        total_cases_strs = total_cases_strs[15:]
        total_cases_dates_list = total_cases_dates_list[15:]
    else:
        total_cases_strs = total_cases_strs[64:]                               # get rid of first column
        total_cases_dates_list = total_cases_dates_list[64:]

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
    if (country.lower() == "china"):
        total_deaths_strs = total_deaths_strs[15:]
        total_deaths_dates_list = total_deaths_dates_list[15:]
    else:
        total_deaths_strs = total_deaths_strs[64:]                               # get rid of first column
        total_deaths_dates_list = total_deaths_dates_list[64:]                   # get rid of first row

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
    if (country.lower() == "china"):
        new_cases_strs = new_cases_strs[15:]
        new_cases_dates_list = new_cases_dates_list[15:]
    else:
        new_cases_strs = new_cases_strs[64:]                               # get rid of first column
        new_cases_dates_list = new_cases_dates_list[64:]

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
    if (country.lower() == "china"):
        new_deaths_strs = new_deaths_strs[15:]
        new_deaths_dates_list = new_deaths_dates_list[15:]
    else:
        new_deaths_strs = new_deaths_strs[64:]                               # get rid of first column
        new_deaths_dates_list = new_deaths_dates_list[64:]

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


    my_graph.title('Covid-19 ' + graph_type.title() + ' Across ' + country.title() + ' as of ' + date_aot, fontsize=14, weight='bold')  # label things
    my_graph.xlabel('Date', fontsize='12', weight='bold')
    my_graph.ylabel('Number of Cases',fontsize='12', weight='bold')
    my_graph.legend(loc="upper left")
    graph_type = graph_type.replace(" ", "_")  # change graph name to replace spaces with underscores
    country = country.lower().replace(" ", "_")

    dir_path = os.path.dirname(os.path.realpath(__file__))  # get working directory
    if not os.path.exists(dir_path + "/graphs/" + country):  # if directory for that country is not yet made, make it
        os.makedirs(dir_path + "/graphs/" + country)
    plt.savefig(dir_path + "/graphs/" + country + "/" + country + "_allfour_" + date_aot + ".png", dpi=500, transparent=True)  # save to that directory

    current_time = time.time()
    for f in os.listdir(dir_path):
        f = dir_path + "/" + f
        creation_time = os.path.getmtime(f)
        if ((current_time - creation_time) / (86400)) >= 1:
            os.remove(f)

    # my_graph.show()
    my_graph.clf()
    my_graph.close('all')

# if __name__ == "__main__":
#     country = str(sys.argv[1])
#     graph_types = ["total confirmed cases", "total deaths", "new confirmed cases", "new deaths"]
#     for graph_type in graph_types:
#         print(graph_type)
#         plot_single(country, graph_type)
#     plot_four(country)

########## update single country
country = input("Input a country: ").title()
graph_types = ["total confirmed cases", "total deaths", "new confirmed cases", "new deaths"]
for graph_type in graph_types:
    print(graph_type)
    plot_single(country, graph_type)
plot_four(country)
countries = ['World', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Antigua and Barbuda',
             'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh',
             'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia',
             'Bonaire Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands',
             'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
             'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo',
             'Costa Rica', 'Cote dIvoire', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech Republic',
             'Democratic Republic of Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt',
             'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Faeroe Islands', 'Falkland Islands',
             'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar',
             'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana',
             'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'International', 'Iran', 'Iraq', 'Ireland',
             'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo',
             'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
             'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania',
             'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique',
             'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria',
             'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea',
             'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia',
             'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'San Marino',
             'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore',
             'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'South Korea', 'South Sudan',
             'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan',
             'Tajikistan', 'Tanzania', 'Thailand', 'Timor', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
             'Turks and Caicos Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States',
             'United States Virgin Islands', 'Uruguay', 'Uzbekistan', 'Vatican', 'Venezuela', 'Vietnam', 'Western Sahara',
             'Yemen', 'Zambia', 'Zimbabwe']
# mycountries = ['World', 'United States', 'United Kingdom', 'Italy', 'Spain', 'France', 'China']
#
# for country in mycountries:
#     plot_single(country.title(), "total confirmed cases")
#     plot_single(country.title(), "total deaths")
#     plot_single(country.title(), "new confirmed cases")
#     plot_single(country.title(), "new deaths")
#     plot_four(country.title())
#     index = mycountries.index(country) + 1
#     print(country + ": " + str(index) + "/" + str(len(mycountries)))