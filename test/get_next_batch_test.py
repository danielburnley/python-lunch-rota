from src import GetNextBatch
import random

class TestGetNextBatch:
  def setup(self):
    self.team_members = []
    self.eligible = []
    self.excluded = []
    self.count = 10
    self.use_case = GetNextBatch()

  def assert_response(self, expected_selected, expected_remaining, expected_excluded):
    selected, remaining, excluded = self.use_case.execute(
      self.team_members,
      self.count,
      self.eligible,
      self.excluded
    )

    assert selected == expected_selected
    assert remaining == expected_remaining
    assert excluded == expected_excluded

  def test_given_no_team_members_return_empty_set(self):
    self.assert_response([], [], [])

  def test_given_team_members_less_than_batch_count_return_team_members(self):
    self.team_members = ['One']
    self.count = 5
    self.eligible = self.team_members
    self.assert_response(['One'], [], [])

  def test_given_team_members_equel_to_count_return_team_members(self):
    self.team_members = ['One', 'Two', 'Three']
    self.count = 3
    self.eligible = self.team_members
    self.assert_response(['One', 'Two', 'Three'], [], [])

  def test_given_team_members_more_than_count_return_randomised_team_members_and_leftovers(self):
    self.team_members = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    self.eligible = self.team_members
    self.count = 5
    self.assert_response([4, 10, 6, 1, 3], [2, 5, 8, 9, 7], [4, 10, 6, 1, 3])

  def test_given_team_members_excluded_return_randomised_team_members_not_including_excluded_and_no_remaining(self):
    self.team_members = [1, 2, 3, 4, 5, 6, 7, 8]
    self.eligible = [1, 3, 5, 7]
    self.count = 4
    self.excluded = [2, 4, 6, 8]
    self.assert_response([1, 3, 5, 7], [], [2, 4, 6, 8, 1, 3, 5, 7])

  def test_given_valid_team_members_is_less_than_count_return_randomised_team_members_including_excluded(self):
    self.team_members = [1, 2, 3, 4, 5, 6, 7, 8]
    self.eligible = [7, 8]
    self.count = 4
    self.excluded = [1, 2, 3, 4, 5, 6]
    self.assert_response([7, 8, 3, 1], [6, 2, 4, 5], [7, 8, 3, 1])

  def test_chained_batches(self):
    team_members = [1, 2, 3, 4, 5, 6, 7, 8]
    eligible = [1, 2, 3, 4, 5, 6, 7, 8]
    lunchers, remaining, excluded = self.use_case.execute(team_members, 3, eligible, [])
    assert lunchers == [3,1,6]
    assert remaining == [2,4,5,8,7]
    lunchers_two, remaining, excluded = self.use_case.execute(team_members, 3, remaining, excluded)
    assert lunchers_two == [2, 8, 4]
    assert remaining == [5, 7]
    lunchers_three, remaining, excluded = self.use_case.execute(team_members, 3, remaining, excluded)
    assert lunchers_three == [5, 7, 3]
    assert remaining == [6, 8, 1, 4, 2]
