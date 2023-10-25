# Import necessary libraries:
# boto3 is the Amazon Web Services (AWS) SDK for Python.
# operator is a module that provides a set of convenient operators.
import boto3
from operator import itemgetter

# Create an EC2 client and resource object for the 'eu-west-2' region.
ec2_client = boto3.client('ec2', region_name="eu-west-2")
ec2_resource = boto3.resource('ec2', region_name="eu-west-2")

# Define the instance ID for which operations will be performed.
instance_id = "i-04f01be7a765exxx"  # Replace with your instance ID.

# Use the EC2 client to describe volumes attached to the specified instance ID.
volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',  # Filter volumes by the attachment instance ID.
            'Values': [instance_id]  # Look for volumes attached to the specified instance ID.
        }
    ]
)

# Get the first volume from the list of volumes returned by describe_volumes.
instance_volume = volumes['Volumes'][0]

# Use the EC2 client to describe snapshots associated with the volume ID of the retrieved volume.
snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],  # Specify the owner of the snapshots as 'self' (the current AWS account).
    Filters=[
        {
            'Name': 'volume-id',  # Filter snapshots by the volume ID.
            'Values': [instance_volume['VolumeId']]  # Look for snapshots associated with the specified volume ID.
        }
    ]
)

# Sort the list of snapshots by their start time in descending order (from newest to oldest),
# and get the first snapshot from the sorted list (the latest snapshot).
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

# Print the start time of the latest snapshot to the console.
print(latest_snapshot['StartTime'])

# Use the EC2 client to create a new volume from the latest snapshot,
# specifying the availability zone and tags for the new volume.
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],  # Specify the snapshot ID to create the volume from.
    AvailabilityZone="eu-west-2b",  # Specify the availability zone for the new volume.
    TagSpecifications=[
        {
            'ResourceType': 'volume',  # Specify the resource type as 'volume'.
            'Tags': [
                {
                    'Key': 'Name',  # Specify the tag key as 'Name'.
                    'Value': 'prod'  # Specify the tag value as 'prod'.
                }
            ]
        }
    ]
)

# Create an infinite loop to check the state of the new volume.
while True:
    # Get the state of the new volume.
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)  # Print the state of the new volume to the console.
    # Check if the state of the new volume is 'available'.
    if vol.state == 'available':
        # If the state is 'available', use the EC2 resource to attach the new volume to the specified instance,
        # specifying the device name for the new volume.
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=new_volume['VolumeId'],  # Specify the volume ID of the new volume.
            Device='/dev/xvdb'  # Specify the device name for the new volume.
        )
        break  # Exit the infinite loop once the new volume has been attached.
