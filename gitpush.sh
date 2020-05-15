#!/bin/bash

./src/graphScript.py 
./src/write_to_html.py  

date=$(date +%F)
git add .

git commit -m "Updated htmls and graphs as of $date"

git push