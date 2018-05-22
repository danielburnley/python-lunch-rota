import boto3
import os

class ExcludedGateway:
  def __init__(self):
    self.s3 = boto3.resource('s3')
    self.excluded = self.s3.Object(os.environ['S3_BUCKET_NAME'], 'excluded.txt')

  def current(self):
    obj = self.excluded.get()
    return obj['Body'].read().decode('utf-8').split(",")

  def update(self, excluded):
    excluded = ",".join(excluded)
    self.excluded.put(Body=excluded.encode('utf-8'))
