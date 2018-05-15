from datetime import date
from random import Random
import urllib.request
import json
import os

class GetNextBatch:
  def __init__(self):
    self.random = Random('meow')

  def execute(self, team_members, count, eligible, excluded):
    if count >= len(team_members):
      return (team_members, [], [])
    next_batch, remaining = self.draw_team_members(eligible, count)
    if len(next_batch) == count:
      return (next_batch, remaining, excluded + next_batch)
    remaining_count = count - len(next_batch)
    valid_team_members = [name for name in team_members if name not in next_batch]
    additional_batch, remaining = self.draw_team_members(valid_team_members, remaining_count)
    next_batch = next_batch + additional_batch
    return(next_batch, remaining, next_batch)

  def draw_team_members(self, eligible, count):
    eligible.sort()
    self.random.shuffle(eligible)
    return (eligible[:count], eligible[count:])


class TeamMemberGateway:
  def fetch(self):
    doc_url = f"https://docs.google.com/spreadsheets/d/{os.environ['TEAMS_DOC_ID']}/gviz/tq?tqx=out:csv"
    names = []
    with urllib.request.urlopen(doc_url) as f:
      names = f.read().decode('utf-8').split("\n")
    return [name.strip('"') for name in names]

class LunchersGateway:
  def __init__(self, get_next_batch):
    self.get_next_batch = get_next_batch

  def for_weeks(self, team_members, count, weeks):
    if len(team_members) == 0 or weeks == 0:
      return {}
    rota = {}
    remaining = team_members
    excluded = []
    for i in range(weeks):
      (next_batch, remaining, excluded) = self.get_next_batch.execute(
        team_members,
        count,
        remaining,
        excluded
      )
      rota[i] = next_batch
    return rota


class GetRota:
  def __init__(self, team_members_gateway, lunchers_gateway):
    self.team_member_gateway = team_members_gateway
    self.lunchers_gateway = lunchers_gateway

  def execute(self):
    team_members = sorted(self.team_member_gateway.fetch())
    return self.lunchers_gateway.for_weeks(team_members, 8, 52)

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

def lambda_handler(event, context):
  get_rota = GetRota(TeamMemberGateway(), LunchersGateway(GetNextBatch()))
  handler = LambdaHandler(get_rota)
  return handler.execute(event, context)
