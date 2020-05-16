#!/bin/bash

python3 /src/graphScript.py 
python3 /src/write_to_html.py  

date=$(date +%F)
cd ..
git add -A

git commit -m "Updated htmls and graphs as of $date"

git push