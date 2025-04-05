### List items dynamo

    aws dynamodb scan --table-name images --region us-east-1

### List s3 items

    aws s3 ls uploads

### To create table

    aws dynamodb create-table \

    --table-name images \

    --attribute-definitions AttributeName=id,AttributeType=S \

    --key-schema AttributeName=id,KeyType=HASH \

    --billing-mode PAY_PER_REQUEST \

    --region us-east-1


### To create bucket

    aws s3 mb s3://uploads

### To run aws cli commands as localstack

    export AWS_PROFILE=localstack

### To run app

    python3 -m uvicorn application:app --reload

### To run pytest

    python3 -m pytest

### To run localstack in docker

    docker compose up -d

### Api docs

http://localhost:8000/docs#/