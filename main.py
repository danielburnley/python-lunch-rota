from src.persistant import GetCurrentRota, GetNextBatch, GetNextRota, LambdaHandler
from src.persistant.gateways import ExcludedGateway, LunchersGateway, TeamMembersGateway


def lambda_handler(event, context):
  get_rota = GetCurrentRota(LunchersGateway())
  get_next_rota = GetNextRota(GetNextBatch(), TeamMembersGateway(), LunchersGateway(), ExcludedGateway())
  handler = LambdaHandler(get_rota, get_next_rota)
  return handler.execute(event, context)
