class GetCurrentRota:
  def __init__(self, lunchers_gateway):
    self.lunchers_gateway = lunchers_gateway

  def execute(self):
    return { 'rota' : self.lunchers_gateway.current() }

