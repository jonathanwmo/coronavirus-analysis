
COVID-19 Analysis Website
======================
https://jonathanwmo.github.io/coronavirus-analysis
1. [Introduction](#introduction-)
2. [Project Layout](#project-layout-)
3. [Installation](#installation-)
4. [API Syncing](#api-syncing-)
	* [Adding New APIs](#adding-new-apis-)
	* [Adding New Parsers](#adding-new-parsers-)
5. [Utilities](#utilities-)
6. [Testing](#testing-)

Introduction [^](#covid-19-analysis-website)
------------

The purpose of this wiki is to help future viewers of this repository 
understand the functions of the website and overall project. The website is
built solely on HTML, CSS, and Python. The website's purpose is to view the 
COVID-19 trends across different countries in numerical and graphical format.

Project Layout [^](#covid-19-analysis-website)
--------------

The project is laid out in a basic directory format with \src containing python, 
shell script, HTML, and CSS code as well as graph images. The \exportToHTML directory 
contains source code viewing in an HTML format.:

-   \src
    -   gitpush.sh (allows user to run both python scripts and push to repository in one shell script)
    -   \graphs (contains directories for all countries)
        -   afghanistan (contains .png images of all 5 types of graphs)
            -   afghanistan_allfour_2020-07-23.png
            -   afghanistan_new_confirmed_cases_2020-07-23.png
            -   afghanistan_new_deaths_2020-07-23.png
            -   afghanistan_total_confirmed_cases_2020-07-23.png
            -   afghanistan_total_deaths_2020-07-23.png
        -   ...
    -   graphScript.py (creates 5 new graphs in .png files for every country)
    -   \htmls (contains HTML files of all countries)
        -   afghanistan.html
        -   albania.html
        -   ...
    -   main.css (contains Cascading Sheets Styling)
    -   write_to_to_html.py (Updates the COVID-19 statistics and graph image for each countries' HTML file)
-   \exportToHTML (contains source code viewable in an HTML format)
    -   gitpush.sh.html
    -   graphScript.py.html
    -   write_to_html.py.html
-   index.html (main home page)
-   requirements.txt (contains the necessary Python packages to run)
    
    
Installation [^](#covid-19-analysis-website)
------------
To install, follow the [python.org](python.org) tutorial to install the correct version of Python.
Next make sure pip is installed on your machine, and then run `pip install -r requirements.txt` to make sure all necessary packages are installed.
Then when in the /src directory, `./gitpush.sh` will run the shell script to update the website.

Note: Users may have to run chmod +x on the python scripts to allow them to be run as executables