import boto3

# Replace 'your-region' with the AWS region where your RDS Aurora instance is located.
# Replace 'your-instance-identifier' with the identifier of your RDS Aurora instance.
# Replace 'db.r5.large' with the desired new instance type to which you want to upgrade.

def lambda_handler(event, context):
    # Define the region where your RDS Aurora instance is located
    # 'your-region'
    region = 'ap-southeast-1'

    # Define the name of your RDS Aurora instance
    # 'your-instance-identifier'
    instance_identifier = 'restore-tdm-tunashoki-20240318'

    # Define the new instance type to upgrade to
    # 'db.r5.large'
    new_instance_type = 'db.t3.large'  # Change this to the desired instance type

    # Initialize the RDS client
    rds_client = boto3.client('rds', region_name=region)

    try:
        # Modify the instance to upgrade the instance type
        response = rds_client.modify_db_instance(
            DBInstanceIdentifier=instance_identifier,
            ApplyImmediately=True,
            DBInstanceClass=new_instance_type
        )
        print("Successfully initiated instance type upgrade : ", response)

    except Exception as e:
        print("Error upgrading instance type: ", e)
        raise e

    return {
        'statusCode': 200,
        'body': 'Instance type upgrade initiated successfully.'
    }