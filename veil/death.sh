#!/bin/bash

rm life
kill -9 `cat corpus`
sleep 5
rm dicongwochomut/spark.py
cp veil/template.py dicongwochomut/spark.py
./birth.sh &
