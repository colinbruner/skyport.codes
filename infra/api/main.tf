provider "aws" {
  region = var.aws_region
}

###
# CW
###
resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"

  retention_in_days = 7
}

###
# API_GW
###

resource "aws_apigatewayv2_api" "lambda" {
  name          = "iata_api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id = aws_apigatewayv2_api.lambda.id

  name        = "iata_api_prod"
  auto_deploy = true

  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 100
  }

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "iata" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.api.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "default" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.iata.id}"
}

# Lazy / root route. Change to static bucket target?
resource "aws_apigatewayv2_route" "iata" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "GET /{code}"
  target    = "integrations/${aws_apigatewayv2_integration.iata.id}"
}

# Add explicit /iata route (future?)
resource "aws_apigatewayv2_route" "iata_explicit" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "GET /iata/{code}"
  target    = "integrations/${aws_apigatewayv2_integration.iata.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}

