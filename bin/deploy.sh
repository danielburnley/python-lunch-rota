#!/bin/bash

rm -rf ./**/__pycache__
zip function.zip main.py ./src/*.py ./src/persistant/*.py ./src/persistant/gateways/*.py

aws lambda update-function-code --region eu-west-1 --function-name "lunchRota" --zip-file fileb://function.zip --query "LastModified" &&
aws lambda update-function-configuration --region eu-west-1 --function-name "lunchRota" --handler "main.lambda_handler" --query "Handler" &&
rm function.zip
