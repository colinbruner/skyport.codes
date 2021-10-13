#!/usr/bin/env python3

# stdlib
import time
import json

# 3rd party
import boto3

# DynomoDB Table
dynamodb_table = "iata.api"
dynamodb = boto3.resource("dynamodb")


def transform_unicode(obj):
    pass


def put_data(table, data):
    # Create a DynomoDB Batch Writer
    with table.batch_writer() as batch:
        for key, obj in data.items():
            try:
                resp = batch.put_item(Item=obj)
                print(f"Successfully updated {key}.")
            except Exception as e:
                print(f"Error: {e}")
                print(f"Malformed data returned: {resp}")


def main():
    table = dynamodb.Table(dynamodb_table)

    ###
    # IATA Data
    ###
    # Read IATA JSON data from file
    with open("../iata.json", "r") as iata_file:
        iata_data = json.load(iata_file)

    start = time.time()
    put_data(table, iata_data)
    print(f"Updated {len(iata_data)} IATA Codes in {time.time() - start}s")


if __name__ == "__main__":
    main()
