#!/bin/bash

./graphScript.py 
./write_to_html.py  

date=$(date +%F)
time=$(date +"%T")

# declare -a mycountries=('World' 'United States' 'United Kingdom' 'Italy' 'Spain' 'France' 'China')
# for i in "${arr[@]}"
# do 
#     ./graphScript.py $i
#     ./write_to_html.py $i
# done

git add -A

git commit -m "Updated htmls and graphs as of $date at $time"

git push