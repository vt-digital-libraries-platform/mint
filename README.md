# ID Minting Service

This project contains source code and supporting files for a serverless application - VTDLP ID Minting service. This service assign a new NOID to a record and update record with new information. See [Usage](##usage) section.

The application uses several AWS resources, including Lambda functions, a DynamoDB and an API Gateway API. These resources are defined in the `template.yaml` file in this project.

## Lambda Function
* [app.py](apps/app.py): Handle NOID creation
* [update.py](apps/update.py): Update DynamoDB table record(s)

## API Gateway
* ```GET``` https://xxxx.execute-api.us-east-1.amazonaws.com/Prod/mint
	* [API key](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-setup-api-key-with-console.html#api-gateway-usage-plan-configure-apikey-on-method) is required.

* ```POST``` https://xxxx.execute-api.us-east-1.amazonaws.com/Prod/update
	* [API key](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-setup-api-key-with-console.html#api-gateway-usage-plan-configure-apikey-on-method) is required
  * Parameters are required

  | Name | Description |
  |:---  |:------------|
  | long_url | https://long_url |
  | short_url | https://short_url |
  | noid | NOID |
  | create_date | %Y-%m-%dT%H:%M:%S e.g. 2020-03-23T17:31:35  |

## DynamoDB Table
* [Table Schema](docs/table_schema.json)
* [Sample record](docs/record.json)

### Deploy VTDLP ID Minting Service application using CloudFormation stack
#### Step 1: Launch CloudFormation stack
[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?&templateURL=https://vtdlp-dev-cf.s3.amazonaws.com/95e059ceb522e30eacd80def68b64f43.template)

Click *Next* to continue

#### Step 2: Specify stack details

| Name | Description |
|:---  |:------------|
| Stack name | any valid name |
| NSTableName | a DynamoDB table name |
| NOIDNAA | a valid string. e.g. 53696 |
| NOIDScheme | ark:/ |
| NOIDTemplate | a valid string. e.g. eeddeede |
| REGION | a valid AWS region. e.g. us-east-1  |

#### Step 3: Configure stack options
Leave it as is and click **Next**

#### Step 4: Review
Make sure all checkboxes under Capabilities section are **CHECKED**

Click *Create stack*

### Deploy VTDLP ID Minting Service application using SAM CLI

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
```

Above command will build the source of the application. The SAM CLI installs dependencies defined in `requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

To package the application, run the following in your shell:
```bash
sam package --output-template-file packaged.yaml --s3-bucket BUCKETNAME
```
Above command will package the application and upload it to the S3 bucket you specified.

Run the following in your shell to deploy the application to AWS:
```bash
sam deploy --template-file packaged.yaml --stack-name STACKNAME --s3-bucket BUCKETNAME --parameter-overrides 'NSTableName=tablename Region=us-east-1 NOIDNAA=12345 NOIDScheme=ark:/ NOIDTemplate=aabbcc' --capabilities CAPABILITY_IAM --region us-east-1
```

## Usage
* Get a new NOID
```
curl -H "x-api-key:APIKEY" https://xxxx.execute-api.us-east-1.amazonaws.com/Prod/mint
```
* Output
```
{"message": "New NOID: 3c46gw18 is created."
```
* Update a record by NOID
```
curl -H "x-api-key: APIKEY" -X POST -d "long_url=YourURL&short_url=YourURL&noid=YourNOID&create_date=2020-03-23T17:31:35" https://xxxx.execute-api.us-east-1.amazonaws.com/Prod/update
```
* Output
```
{"message": "Rec 3q13c28n is updated."}
```

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests. You must have a env file: [custom_pytest.ini](custom_pytest.ini)

```bash
lambdatest$ pip install -r tests/requirements.txt --user
# unit test
lambdatest$ python -m pytest tests/unit -v -c custom_pytest.ini
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name stackname
```

