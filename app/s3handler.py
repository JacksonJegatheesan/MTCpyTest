import boto3
endpoint_url = "http://localhost.localstack.cloud:4566"

def list_files(bucket_name, folder_prefix):
    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
    return [obj['Key'] for obj in response.get('Contents', [])]

def upload_image_to_s3(file_obj, bucket_name, s3_key):
    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    try:
        s3.upload_fileobj(file_obj, bucket_name, s3_key)
        print(f"Uploaded to completed")
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False


def delete_file_from_s3(bucket_name: str, s3_key: str):
    s3 = boto3.client('s3')
    try:
        s3.delete_object(Bucket=bucket_name, Key=s3_key)
        print(f"Deleted s3://{bucket_name}/{s3_key}")
        return True
    except Exception as e:
        print(f"Delete failed: {e}")
        return False