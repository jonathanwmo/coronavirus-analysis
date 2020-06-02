#!/bin/bash

# ./graphScript.py 
./write_to_html.py  

date=$(date +%F)
time=$(date +"%T")

git add -A

git commit -m "Updated htmls and graphs as of $date at $time"

git push