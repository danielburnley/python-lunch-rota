#!/bin/bash

rm -rf ./src/__pycache__
zip function.zip ./src/*

aws lambda update-function-code --function-name "lunchRota" --zip-file fileb://function.zip
aws lambda update-function-configuration --function-name "lunchRota" --handler "src.lunch_rota.lambda_handler"

rm function.zip
