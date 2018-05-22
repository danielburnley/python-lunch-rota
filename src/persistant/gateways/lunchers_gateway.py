import boto3
import os

class LunchersGateway:
  def __init__(self):
    self.s3 = boto3.resource('s3')
    self.lunchers = self.s3.Object(os.environ['S3_BUCKET_NAME'], 'lunchers.txt')

  def current(self):
    return self.lunchers.get()['Body'].read().decode('utf-8').strip("\n").split(",")

  def update(self, lunchers):
    lunchers = ",".join(lunchers)
    self.lunchers.put(Body=lunchers.encode('utf-8'))



