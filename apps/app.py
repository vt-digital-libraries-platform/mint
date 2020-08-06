import boto3
import json
import os

from noid.pynoid import mint

noid_template = os.getenv('NOID_Template')
noid_scheme = os.getenv('NOID_Scheme')
noid_naa = os.getenv('NOID_NAA')
region_name = os.getenv('Region')
table_name = os.getenv('NSTable')

ddb = boto3.resource('dynamodb', region_name = region_name).Table(table_name)

def lambda_handler(event, context):

    noid = mint(template=noid_template, n=None, scheme=noid_scheme, naa=noid_naa)
    short_id = noid.split("/")[2]

    try:

        record = {}
        record["short_id"] = short_id
        ddb.put_item(Item=record)

    except:
        return {
            "statusCode": 503,
            "body": "Noid creation is failed.",
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "New NOID: {0} is created.".format(short_id),
        }),
    }
