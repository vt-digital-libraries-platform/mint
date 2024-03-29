import boto3
import datetime
import json
import os

region_name = os.getenv('Region')
table_name = os.getenv('NSTable')

ddb = boto3.resource('dynamodb', region_name=region_name).Table(table_name)


def lambda_handler(event, context, ddb):

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
        "Access-Control-Allow-Origin": "*"}

    try:
        responseBody = event["body"]
        data = responseBody.split("&")
        long_url = data[0].split("=")[1]
        short_url = data[1].split("=")[1]
        noid = data[2].split("=")[1]
        create_date_str = data[3].split("=")[1]

        create_date = datetime.datetime.strptime(
            create_date_str, '%Y-%m-%dT%H:%M:%S')
        insert_date_str = create_date.strftime("%Y-%m-%dT%H:%M:%S")

        item = ddb.get_item(Key={'short_id': noid})

        if item.get('Item'):

            record = {}
            record["created_at"] = insert_date_str
            record["long_url"] = long_url
            record["short_id"] = noid
            record["short_url"] = short_url
            record["hits"] = 0
            record["ttl"] = 4129578000

            ddb.put_item(Item=record)

        else:
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "message": "Rec {0} is not exist.".format(noid),
                }),
            }

    except BaseException:
        return {
            "statusCode": 503,
            "headers": headers,
            "body": "Rec update is failed.",
        }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({
            "message": "Rec {0} is updated.".format(noid),
        }),
    }
