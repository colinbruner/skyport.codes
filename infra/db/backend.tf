terraform {
  backend "s3" {
    bucket = "infra.colinbruner.com"
    key    = "iata/db/"
    region = "us-east-1"
  }
}
