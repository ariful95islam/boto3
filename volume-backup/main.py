# Import the necessary libraries:
# boto3 is the Amazon Web Services (AWS) SDK for Python.
# schedule is an in-process scheduler for periodic jobs that uses the builder pattern for configuration.
import boto3
import schedule

# Create an EC2 client object for the 'eu-west-2' region.
ec2_client = boto3.client('ec2', region_name="eu-west-2")

# Define a function to create snapshots of volumes.
def create_volume_snapshots():
    # Use the EC2 client object to describe volumes that have a tag with the key 'Name' and value 'prod'.
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',  # Filter volumes by the tag key 'Name'.
                'Values': ['prod']  # Look for volumes with the tag value 'prod'.
            }
        ]
    )
    # Loop through each volume in the 'Volumes' list returned by the describe_volumes method.
    for volume in volumes['Volumes']:
        # Use the EC2 client object to create a snapshot of the current volume.
        new_snapshot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId']  # Specify the ID of the volume to snapshot.
        )
        # Print the response returned by the create_snapshot method to the console.
        # This response contains information about the new snapshot.
        print(new_snapshot)

# Use the schedule library to schedule the create_volume_snapshots function to be called once every day.
schedule.every().day.do(create_volume_snapshots)

# Create an infinite loop to keep the script running and to check for scheduled tasks.
while True:
    # If there are any scheduled tasks due, run them now.
    schedule.run_pending()
