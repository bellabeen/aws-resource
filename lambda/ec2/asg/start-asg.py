import os
import boto3

# Create Schedule on Eventbridge
# For Environment variables add the following:
# NAMES - Space separated list of the Auto Scaling Groups you want to manage with this function
# MIN_SIZE - Minimum size of the Auto Scaling Group(s) when EC2 instances are started
# MAX_SIZE - Maximum size of the Auto Scaling Group(s) when EC2 instances are started
# DESIRED_CAPACITY - Desired capacity of the Auto Scaling Group(s) when EC2 instances are started

client = boto3.client('autoscaling')

def get_env_variable(var_name):
    msg = "Set the %s environment variable"
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = msg % var_name

def lambda_handler(event, context):
    auto_scaling_groups = get_env_variable('NAMES').split()

    for group in auto_scaling_groups:
        action = "Starting"
        min_size = int(get_env_variable('MIN_SIZE'))
        max_size = int(get_env_variable('MAX_SIZE'))
        desired_capacity = int(get_env_variable('DESIRED_CAPACITY'))

        print(action + " Auto Scaling Group '" + group + "'")

        response = client.update_auto_scaling_group(
            AutoScalingGroupName=group,
            MinSize=min_size,
            MaxSize=max_size,
            DesiredCapacity=desired_capacity,
        )

        print("Auto Scaling Group '" + group + "' successfully started.")
        print(response)