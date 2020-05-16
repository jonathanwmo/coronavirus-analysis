#!/bin/bash

python3 graphScript.py 
python3 write_to_html.py  

date=$(date +%F)
# declare -a mycountries=['World', 'United States', 'United Kingdom', 'Italy', 'Spain', 'France', 'China']
# for i in "${arr[@]}"
# do 
#     ./ 
# done

git add -A

git commit -m "Updated htmls and graphs as of $date"

git push