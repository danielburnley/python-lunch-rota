class GetRotaForYear:
  def __init__(self, team_members_gateway, lunchers_gateway):
    self.team_member_gateway = team_members_gateway
    self.lunchers_gateway = lunchers_gateway

  def execute(self):
    team_members = sorted(self.team_member_gateway.fetch())
    return self.lunchers_gateway.for_weeks(team_members, 8, 52)
