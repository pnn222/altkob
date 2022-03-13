#!/bin/bash

curl --header "Content-Type: application/json" --request POST --data '{"to_delete": 1}' http://localhost:8888/api/add
curl -X DELETE http://localhost:8888/api/remove?key=IntcInRvX2RlbGV0ZVwiOiAxfSI=
curl -X DELETE http://localhost:8888/api/remove?key=IntcInVwZGF0ZWRcIjogMX0i

