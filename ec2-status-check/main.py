# Import the necessary libraries:
# Boto3 is the Amazon Web Services (AWS) SDK for Python, which allows Python developers to write software that uses
# services like Amazon S3 and Amazon EC2.
# Schedule is an in-process scheduler for periodic jobs that uses the builder pattern for configuration.
import boto3
import schedule

# Create an EC2 client and resource object for the 'eu-west-2' region.
ec2_client = boto3.client('ec2', region_name='eu-west-2')
ec2_resource = boto3.resource('ec2', region_name='eu-west-2')

# Define a function to check the status of EC2 instances.
def check_ec2_status():
    # Use the EC2 client to describe instances and store the result in a variable called reservations.
    reservations = ec2_client.describe_instances()
    # Loop through each reservation in the reservations list.
    for reservation in reservations['Reservations']:
        # Extract the instances list from the current reservation.
        instances = reservation['Instances']
        # Loop through each instance in the instances list.
        for instance in instances:
            # Print the instance ID and state to the console.
            print(f"Instance {instance['InstanceId']} is {instance['State']['Name']}")

# Define another function to check the status of instances including system and instance status.
def check_instance_status():
    # Use the EC2 client to describe instance status for all instances.
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True  # Include the status of all instances, not just those currently running.
    )
    # Loop through each status in the InstanceStatuses list.
    for status in statuses['InstanceStatuses']:
        # Extract the state, instance status, and system status from the current status object.
        state = status['InstanceState']['Name']
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        # Print the instance ID, state, instance status, and system status to the console.
        print(f"Instance {status['InstanceId']} is {state} and has instance status {ins_status} and system status {sys_status}")

# Schedule the check_instance_status function to be called every 5 seconds.
schedule.every(5).seconds.do(check_instance_status)

# Create an infinite loop to keep the script running and to check for scheduled tasks.
while True:
    # If there are any scheduled tasks due, run them now.
    schedule.run_pending()
