import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('images')


def save_image_metadata_to_dynamodb(metadata):
    table.put_item(Item=metadata)
    return metadata

def list_all_items():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('images')

    response = table.scan()
    items = response.get('Items', [])
    return items

def get_image_by_id(image_id: str):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('images')

    try:
        response = table.get_item(Key={'id': image_id})
        item = response.get('Item')
        if item:
            return item
        else:
            print(f"No item found with id={image_id}")
            return None
    except Exception as e:
        print(f"Error fetching item: {e}")
        return None

def delete_metadata_from_dynamodb(image_id: str):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('images')

    try:
        table.delete_item(
            Key={
                'id': image_id  # primary key
            }
        )
        print(f"Deleted metadata with id={image_id} from DynamoDB")
        return True
    except Exception as e:
        print(f"Error deleting metadata: {e}")
        return False