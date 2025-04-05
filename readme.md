list items dynamo
aws dynamodb scan --table-name images --region us-east-1

list s3 items
aws s3 ls uploads

to create table
aws dynamodb create-table \
    --table-name images \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1


to create bucket
aws s3 mb s3://uploads

to run aws cli commands as localstack
export AWS_PROFILE=localstack

to run app
python3 -m uvicorn application:app --reload

to run pytest
python3 -m pytest

to run localstack in docker
docker compose up -d
