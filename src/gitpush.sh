#!/bin/bash

START_TIME=$(date +%s)

./graphScript.py
EXIT_CODE=$?
while [ $EXIT_CODE != 0 ]
do
    ./graphScript.py
    EXIT_CODE=$?
done

./write_to_html.py
EXIT_CODE=$?
while [ $EXIT_CODE != 0 ]
do
    ./write_to_html.py
    EXIT_CODE=$?
done

date=$(date +%F)
time=$(date +"%T")

git add -A

git commit -m "Updated htmls and graphs as of $date at $time"

git push

END_TIME=$(date +%s)
RUNTIME=$((END_TIME-START_TIME))
echo "Ran graphScript.py, write_to_html.py and pushed to respository in $RUNTIME seconds."