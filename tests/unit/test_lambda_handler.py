import boto3
import json
import pytest
import os


from apps import app
from apps import update
from moto import mock_dynamodb2

test_apigateway_event = {
    "body": "long_url=YourURL&short_url=YourURL&noid=sf24bx2z&create_date=2020-03-23T17:31:35",
    "resource": "/{proxy+}",
    "path": "/path/to/resource",
    "httpMethod": "POST"}

test_apigateway_event_notexit_noid = {
    "body": "long_url=YourURL&short_url=YourURL&noid=notexitnoid&create_date=2020-03-23T17:31:35",
    "resource": "/{proxy+}",
    "path": "/path/to/resource",
    "httpMethod": "POST"}

table_name = 'minttable_test'
region_name = 'us-east-1'


def create_dyno_table(table_name, region_name):

    dynamodb = boto3.resource('dynamodb', region_name)

    # create a mock table
    table = dynamodb.create_table(TableName=table_name,
                                  KeySchema=[{'AttributeName': 'short_id',
                                              'KeyType': 'HASH'}],
                                  AttributeDefinitions=[{'AttributeName': 'short_id',
                                                         'AttributeType': 'S'},
                                                        {'AttributeName': 'long_url',
                                                         'AttributeType': 'S'}],
                                  ProvisionedThroughput={'ReadCapacityUnits': 5,
                                                         'WriteCapacityUnits': 5},
                                  GlobalSecondaryIndexes=[{"IndexName": "long_url-index",
                                                           "KeySchema": [{"AttributeName": "long_url",
                                                                          "KeyType": "HASH"}],
                                                           "Projection": {"ProjectionType": "ALL"},
                                                           "ProvisionedThroughput": {'ReadCapacityUnits': 5,
                                                                                     'WriteCapacityUnits': 5}}])


@mock_dynamodb2
def test_minting():

    create_dyno_table(table_name, region_name)
    ddb = boto3.resource('dynamodb', region_name=region_name).Table(table_name)

    # Test: request minting and get a noid
    response = app.lambda_handler(event={}, context={}, ddb=ddb)

    assert "message" in response["body"]
    assert "New NOID" in response["body"]

    # Test: request minting from a wrong table
    ddb = boto3.resource(
        'dynamodb',
        region_name=region_name).Table("wrong_table")
    response = app.lambda_handler(event={}, context={}, ddb=ddb)

    assert response["body"] == "Noid creation is failed."


@mock_dynamodb2
def test_update_record():

    create_dyno_table(table_name, region_name)

    # Test: update an existing noid record
    ddb = boto3.resource('dynamodb', region_name=region_name).Table(table_name)

    record = {}
    record["short_id"] = 'sf24bx2z'
    record["long_url"] = 'http://www.test.vt.edu'

    ddb.put_item(Item=record)

    response = update.lambda_handler(
        event=test_apigateway_event, context={}, ddb=ddb)

    assert json.loads(response["body"])[
        "message"] == "Rec {0} is updated.".format('sf24bx2z')

    # Test: update a not exist noid record
    response = update.lambda_handler(
        event=test_apigateway_event_notexit_noid, context={}, ddb=ddb)

    assert json.loads(response["body"])[
        "message"] == "Rec {0} is not exist.".format('notexitnoid')
