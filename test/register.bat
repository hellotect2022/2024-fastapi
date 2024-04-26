#!/bin/bash

curl -X 'POST' -H "Content-Type: application/json" -d '{"username":"abc@gmail.com","password":"abc"}' http://localhost:8001/api/register

echo ''