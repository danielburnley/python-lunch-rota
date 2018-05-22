class GetNextRota:
  def __init__(self, get_next_batch, team_members_gateway, lunchers_gateway, excluded_gateway):
    self.get_next_batch = get_next_batch
    self.team_members_gateway = team_members_gateway
    self.lunchers_gateway = lunchers_gateway
    self.excluded_gateway = excluded_gateway

  def execute(self):
    team_members = self.team_members_gateway.fetch()
    excluded_members = self.excluded_gateway.current()
    eligible_team_members = [person for person in team_members if person not in excluded_members]
    lunchers, _, excluded = self.get_next_batch.execute(team_members, 8, eligible_team_members, excluded_members)
    self.lunchers_gateway.update(lunchers)
    self.excluded_gateway.update(excluded)
    return { 'rota': lunchers }

