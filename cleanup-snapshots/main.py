# Import the necessary libraries:
# boto3 is the Amazon Web Services (AWS) SDK for Python.
# operator is a module that provides a set of convenient operators.
import boto3
from operator import itemgetter

# Create an EC2 client object for the 'eu-west-2' region.
ec2_client = boto3.client('ec2', region_name="eu-west-2")

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
    # Use the EC2 client object to describe snapshots that belong to the current volume and are owned by 'self'.
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],  # Specify the owner of the snapshots as 'self' (the current AWS account).
        Filters=[
            {
                'Name': 'volume-id',  # Filter snapshots by the volume ID.
                'Values': [volume['VolumeId']]  # Look for snapshots associated with the current volume.
            }
        ]
    )

    # Sort the snapshots by their start time in descending order (from newest to oldest).
    sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

    # Loop through each snapshot in the sorted_by_date list, skipping the first two more recent snapshots.
    for snap in sorted_by_date[2:]:
        # Use the EC2 client object to delete the current snapshot.
        response = ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']  # Specify the ID of the snapshot to delete.
        )
        # Print the response returned by the delete_snapshot method to the console.
        # This response contains information about the request to delete the snapshot.
        print(response)
