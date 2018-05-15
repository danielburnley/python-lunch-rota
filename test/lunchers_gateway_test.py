from src.lunch_rota import LunchersGateway

class GetNextBatchSpy:
  def __init__(self):
    self.times_called = 0
    self.requests = []
    self.response = ([], [], [])

  def execute(self, team_members, count, eligible, excluded):
    self.times_called = self.times_called + 1
    self.requests.append({
      'team_members': team_members,
      'count': count,
      'eligible': eligible,
      'excluded': excluded
    })
    self.team_members = team_members
    self.count = count
    self.eligible = eligible
    self.excluded = excluded
    return self.response

class TestLunchersGateway:
  def setup(self):
    self.get_next_batch = GetNextBatchSpy()
    self.gateway = LunchersGateway(self.get_next_batch)

  def test_given_zero_weeks_return_empty_rota(self):
    rota = self.gateway.for_weeks([1,2,3,4,5], 5, 0)
    assert rota == {}

  def test_given_zero_weeks_get_next_batch_is_not_called(self):
    self.gateway.for_weeks([1,2,3,4,5], 5, 0)
    assert self.get_next_batch.times_called == 0

  def test_given_no_team_members_return_empty_rota(self):
    rota = self.gateway.for_weeks([], 3, 52)
    assert rota == {}

  def test_given_zero_team_members_get_next_batch_is_not_called(self):
    self.gateway.for_weeks([], 3,  9)
    assert self.get_next_batch.times_called == 0

  def test_given_one_week_get_next_batch_is_called_once(self):
    self.gateway.for_weeks([1,2,3,4,5], 5, 1)
    assert self.gateway.get_next_batch.times_called == 1

  def test_given_ten_weeks_get_next_batch_is_called_ten_times(self):
    self.gateway.for_weeks([1,2,3,4,5], 5, 10)
    assert self.gateway.get_next_batch.times_called == 10

  def test_given_one_week_team_members_and_initial_params_are_passed_to_get_next_batch_1(self):
    self.gateway.for_weeks([1,2,3,4,5], 5, 1)
    assert self.get_next_batch.team_members == [1,2,3,4,5]
    assert self.get_next_batch.count == 5
    assert self.get_next_batch.eligible == [1,2,3,4,5]
    assert self.get_next_batch.excluded == []

  def test_given_one_week_team_members_and_initial_params_are_passed_to_get_next_batch_2(self):
    self.gateway.for_weeks(['cats', 'dogs', 'ducks'], 3, 1)
    request = self.get_next_batch.requests[0]
    assert request['team_members'] == ['cats', 'dogs', 'ducks']
    assert request['count'] == 3
    assert request['eligible'] == ['cats', 'dogs', 'ducks']
    assert request['excluded'] == []

  def test_given_two_weeks_response_from_get_next_batch_is_passed_into_subsequent_call(self):
    self.get_next_batch.response = ([5,4,3], [1,2], [5,4,3])
    self.gateway.for_weeks([1,2,3,4,5], 3, 2)
    request = self.get_next_batch.requests[1]
    assert request['team_members'] == [1,2,3,4,5]
    assert request['count'] == 3
    assert request['eligible'] == [1,2]
    assert request['excluded'] == [5,4,3]

  def test_given_one_week_returns_rota_with_batch_from_get_next_batch(self):
    self.get_next_batch.response = (['one', 'two', 'three'], [], [])
    rota = self.gateway.for_weeks(['one', 'two', 'three'], 3, 1)
    assert len(rota) == 1
    assert rota[0] == ['one', 'two', 'three']

  def test_given_ten_weeks_returns_rota_with_ten_items(self):
    rota = self.gateway.for_weeks([1,2,3,4], 3, 10)
    assert len(rota) == 10
