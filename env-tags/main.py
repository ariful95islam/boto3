# Importing the boto3 library, which allows you to work with AWS services.
import boto3

# Defining a function called tag_instances, which will be used to tag EC2 instances.
# This function takes two arguments: the name of the region and the environment tag.
def tag_instances(region_name, environment):
    # Creating an EC2 client object for the specified region.
    ec2_client = boto3.client('ec2', region_name=region_name)
    # Creating an EC2 resource object for the specified region.
    ec2_resource = boto3.resource('ec2', region_name=region_name)

    # Creating an empty list to hold the IDs of the EC2 instances.
    instance_ids = []
    # Using the EC2 client object to describe all instances in the region.
    # Storing the information about reservations in the reservations variable.
    reservations = ec2_client.describe_instances()['Reservations']
    # Looping through each reservation in the reservations list.
    for res in reservations:
        # Extracting the list of instances from the current reservation.
        instances = res['Instances']
        # Looping through each instance in the instances list.
        for ins in instances:
            # Adding the ID of the current instance to the instance_ids list.
            instance_ids.append(ins['InstanceId'])

    # Check if the instance_ids list is empty
    if not instance_ids:
        print(f'No instances found in {region_name} for tagging.')
        return  # Exit the function early if no instances are found

    # Using the EC2 resource object to create tags for all instances in the instance_ids list.
    # The key of each tag will be 'environment', and the value will be the environment argument passed to the function.
    response = ec2_resource.create_tags(
        Resources=instance_ids,  # Specifying which resources (instances) to tag.
        Tags=[  # Specifying the tags to create.
            {
                'Key': 'environment',  # The key of the tag.
                'Value': environment   # The value of the tag.
            },
        ]
    )
    # Returning the response from the create_tags method, which can be used for error checking or logging.
    return response

# Calling the tag_instances function to tag all instances in the eu-west-2 (London) region with 'prod'.
response_london = tag_instances("eu-west-2", "prod")

# Calling the tag_instances function to tag all instances in the eu-west-1 (Ireland) region with 'dev'.
response_ireland = tag_instances("eu-west-1", "dev")
