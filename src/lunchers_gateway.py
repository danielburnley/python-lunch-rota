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
