#!/bin/bash

rm -rf ./src/__pycache__
zip function.zip main.py ./src/*

aws lambda update-function-code --region eu-west-1 --function-name "lunchRota" --zip-file fileb://function.zip --query "LastModified" &&
aws lambda update-function-configuration --region eu-west-1 --function-name "lunchRota" --handler "main.lambda_handler" --query "Handler" &&
rm function.zip
