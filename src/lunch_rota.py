from . import *

def lambda_handler(event, context):
  get_rota = GetRota(TeamMemberGateway(), LunchersGateway(GetNextBatch()))
  handler = LambdaHandler(get_rota)
  return handler.execute(event, context)
