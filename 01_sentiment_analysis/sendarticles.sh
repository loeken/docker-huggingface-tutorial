#!/bin/bash
rm out
jq -r '.Data[] | {text: .BODY, title: .TITLE, id: .ID, ccsentiment: .SENTIMENT} | @json' articles.json | while read -r data; do
    #echo $data
    curl -X POST -H "Content-Type: application/json" -d "$data" http://localhost:8000/sentiment>>out
    echo "" >> out
done
