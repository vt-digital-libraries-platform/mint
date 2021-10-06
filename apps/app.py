import boto3
import json
import os

from noid.pynoid import mint

noid_template = os.getenv('NOID_Template')
noid_scheme = os.getenv('NOID_Scheme')
noid_naa = os.getenv('NOID_NAA')
region_name = os.getenv('Region')
table_name = os.getenv('NSTable')


ddb = boto3.resource('dynamodb', region_name=region_name).Table(table_name)


def lambda_handler(event, context, ddb):

    noid = mint(
        template=noid_template,
        n=None,
        scheme=noid_scheme,
        naa=noid_naa)
    short_id = noid.split("/")[2]
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
        "Access-Control-Allow-Origin": "*"}

    try:

        record = {}
        record["short_id"] = short_id

        ddb.put_item(Item=record)

    except BaseException:
        return {
            "statusCode": 503,
            "headers": headers,
            "body": "Noid creation is failed.",
        }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({
            "message": "New NOID: {0} is created.".format(short_id),
        }),
    }
