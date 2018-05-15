#!/bin/bash

rm -rf ./src/__pycache__
zip function.zip ./src/*

aws lambda update-function-code --region eu-west-1 --function-name "lunchRota" --zip-file fileb://function.zip &&
aws lambda update-function-configuration --region eu-west-1 --function-name "lunchRota" --handler "src.lunch_rota.lambda_handler" &&
rm function.zip
