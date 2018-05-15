from random import Random

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
