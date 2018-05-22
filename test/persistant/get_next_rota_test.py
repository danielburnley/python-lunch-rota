from src.persistant import GetNextRota

class SpyGateway:
  def __init__(self):
    self.fetch_called = False
    self.current_called = False
    self.update_called = False
    self.updated_with = None
    self.returns = None

  def fetch(self):
    self.fetch_called = True
    return self.returns

  def current(self):
    self.current_called = True
    return self.returns

  def update(self, request):
    self.update_called = True
    self.updated_with = request

class SpyGetNextBatch:
  def __init__(self):
    self.called = False
    self.called_with = {}
    self.returns = None

  def execute(self, team_members, count, eligible, excluded):
    self.called_with['team_members'] = team_members
    self.called_with['eligible'] = eligible
    self.called_with['excluded'] = excluded
    return self.returns


class TestGetNextRota:
  def setup(self):
    self.team_members_gateway = SpyGateway()
    self.excluded_gateway = SpyGateway()
    self.lunchers_gateway = SpyGateway()
    self.get_next_batch = SpyGetNextBatch()
    self.use_case = GetNextRota(self.get_next_batch, self.team_members_gateway, self.lunchers_gateway, self.excluded_gateway)

  def test_given_no_excluded_members_call_next_batch_correctly(self):
    self.team_members_gateway.returns = ['One', 'Two', 'Three']
    self.excluded_gateway.returns = []
    self.get_next_batch.returns = ([], [], [])
    self.use_case.execute()
    assert self.team_members_gateway.fetch_called == True
    assert self.excluded_gateway.current_called == True
    request = self.get_next_batch.called_with
    assert request['team_members'] == ['One', 'Two', 'Three']
    assert request['eligible'] == ['One', 'Two', 'Three']
    assert request['excluded'] == []

  def test_given_excluded_members_call_next_batch_correctly(self):
    self.team_members_gateway.returns = ['One', 'Two', 'Three']
    self.excluded_gateway.returns = ['Two']
    self.get_next_batch.returns = ([], [], [])
    self.use_case.execute()
    assert self.team_members_gateway.fetch_called == True
    assert self.excluded_gateway.current_called == True
    request = self.get_next_batch.called_with
    assert request['team_members'] == ['One', 'Two', 'Three']
    assert request['eligible'] == ['One', 'Three']
    assert request['excluded'] == ['Two']

  def test_updates_lunchers_and_excluded_with_values_from_get_next_batch(self):
    self.team_members_gateway.returns = ['One', 'Two', 'Three']
    self.excluded_gateway.returns = []
    self.get_next_batch.returns = (['One', 'Two'], ['Three'], ['Meow', 'Woof'])
    self.use_case.execute()
    assert self.lunchers_gateway.update_called == True
    assert self.lunchers_gateway.updated_with == ['One', 'Two']
    assert self.excluded_gateway.update_called == True
    assert self.excluded_gateway.updated_with == ['Meow', 'Woof']

  def test_returns_rota_from_get_next_batch(self):
    self.team_members_gateway.returns = ['One', 'Two', 'Three']
    self.excluded_gateway.returns = []
    self.get_next_batch.returns = (['One', 'Two'], ['Three'], ['Meow', 'Woof'])
    response = self.use_case.execute()
    assert response['rota'] == ['One', 'Two']

