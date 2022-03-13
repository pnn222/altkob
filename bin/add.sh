#!/bin/bash

curl --header "Content-Type: application/json" --request POST --data '{"y": 1, "b": {"t": 4, "m":6, "a":4}, "z": 1}' http://localhost:8888/api/add
curl --header "Content-Type: application/json" --request POST --data '{"z": 1, "b": {"t": 4, "m":6, "a":4}, "y": 1}' http://localhost:8888/api/add
