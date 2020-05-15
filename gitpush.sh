#!/bin/bash

usr/bin/python3 graphScript.py 
usr/bin/python3 write_to_html.py  

date=$(date +%F)
git add .

git commit -m "Updated htmls and graphs as of $date"

git push