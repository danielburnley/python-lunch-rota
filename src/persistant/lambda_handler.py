from datetime import date
from urllib.parse import parse_qs
import os
import json

class LambdaHandler:
  def __init__(self, get_rota, get_next_rota):
    self.get_rota = get_rota
    self.get_next_rota = get_next_rota

  def execute(self, event, context):
    event_body = parse_qs(event['body'])
    token_string = f"token={os.environ['SLACK_TOKEN']}"
    command = event_body['text']

    if token_string in event_body['token']:
      status_code = 200
      lunchers = []
      if 'next' in command:
        lunchers = get_next_rota.execute()['rota']
      else:
        lunchers = get_rota.execute()['rota']
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
