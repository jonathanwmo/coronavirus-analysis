#!/bin/bash

./src/graphScript.py
./src/write_to_html.py
# python3 /src/graphScript.py
# python3 /src/write_to_html.py

git add .
echo "Enter commit message: "
read commitMessage

git commit -m "$commitMessage"

git push