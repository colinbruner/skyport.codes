provider "aws" {
  region = var.aws_region
}

resource "aws_dynamodb_table" "iata" {
  name           = "iata.api"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "IATA"

  attribute {
    name = "IATA"
    type = "S"
  }
}

