#!/bin/bash

curl --header "Content-Type: application/json" --request POST --data '{"to_update": 1}' http://localhost:8888/api/add
curl --header "Content-Type: application/json" --request PUT --data '{"key": "IntcInRvX3VwZGF0ZVwiOiAxfSI=", "body": {"updated": 1}}' http://localhost:8888/api/update

