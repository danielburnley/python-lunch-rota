from datetime import date
import os
import json

class LambdaHandler:
  def __init__(self, get_rota):
    self.get_rota = get_rota

  def execute(self, event, context):
    week_number = date.today().isocalendar()[1]
    rota = self.get_rota.execute()
    lunchers = rota[week_number]
    token_string = f"token={os.environ['SLACK_TOKEN']}"

    if token_string in event['body']:
      status_code = 200
      response_body = self.format_slack_message(lunchers)
    else:
      response_body = json.dumps({})
      status_code = 401

    return {
      "statusCode": status_code,
      "body": response_body,
      "isBase64Encoded": False
    }

  def format_slack_message(self, lunchers):
    response = {}
    response['response_type'] = 'in_channel'
    response['text'] = "\n".join(lunchers)
    return json.dumps(response)
