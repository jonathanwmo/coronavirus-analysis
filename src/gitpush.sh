#!/bin/bash

# ./graphScript.py 
# ./write_to_html.py  

date=$(date +%F)
declare -a mycountries=['World', 'United States', 'United Kingdom', 'Italy', 'Spain', 'France', 'China']
for i in "${arr[@]}"
do 
    ./graphScript.py $i
done

git add -A

git commit -m "Updated htmls and graphs as of $date"

git push