import urllib.request
import os

class TeamMembersGateway:
  def fetch(self):
    doc_url = f"https://docs.google.com/spreadsheets/d/{os.environ['TEAMS_DOC_ID']}/gviz/tq?tqx=out:csv"
    names = []
    with urllib.request.urlopen(doc_url) as f:
      names = f.read().decode('utf-8').split("\n")
    return [name.strip('"') for name in names]
