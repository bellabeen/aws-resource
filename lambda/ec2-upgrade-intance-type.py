import boto3

# Create Schedule on Eventbridge

def lambda_handler(event, context):
    client = boto3.client('ec2')
    # Insert your Instance ID here
    my_instance = 'i-0ed7dcebbbf30517d'  # Stop the instance
    client.stop_instances(InstanceIds=[my_instance])
    waiter = client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[my_instance])  # Change the instance type
    client.modify_instance_attribute(InstanceId=my_instance,
            Attribute='instanceType', Value='r6i.2xlarge')  # Start the instance
    client.start_instances(InstanceIds=[my_instance])