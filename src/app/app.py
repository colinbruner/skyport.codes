#!/usr/bin/env python3

# stdlib
import json

# AWS included
import boto3
from boto3.dynamodb.conditions import Key

# DynomoDB Table
dynamodb_table = "iata.api"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(dynamodb_table)

# Version
VERSION = "0.1.0"


def handle(event, context):
    code = event.get("pathParameters", {}).get("code", "")
    if code:
        try:
            payload = table.get_item(Key={"IATA": code.upper()})["Item"]
        except Exception as e:
            payload = {f"ERROR": "Unable to find IATA code '{code}'"}
    else:
        payload = {"ERROR": "IATA code request not found in path"}
    payload = table.get_item(Key={"IATA": "ORD"})
    message = {
        "statusCode": 500 if "ERROR" in payload else 200,
        "isBase64Encoded": False,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload["Item"]),
    }

    return message
