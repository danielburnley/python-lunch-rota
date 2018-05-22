class GetPersistantRota:
  def __init__(self, get_next_batch, team_member_gateway, lunchers_gateway, excluded_members_gateway):
    self.get_next_batch = get_next_batch
    self.team_member_gateway = team_member_gateway
    self.lunchers_gateway = lunchers_gateway
    self.excluded_members_gateway = excluded_members_gateway

  def execute(self, count):
    team_members = self.team_member_gateway.fetch()
    excluded_members = self.excluded_members_gateway.fetch()
    eligible_team_members = [person for person in team if person not in excluded_members]
    next_batch, remaining, excluded = self.get_next_batch.execute()
