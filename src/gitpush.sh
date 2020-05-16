#!/bin/bash

./graphScript.py 
./write_to_html.py  

date=$(date +%F)

git add -A

git commit -m "Updated htmls and graphs as of $date"

git push