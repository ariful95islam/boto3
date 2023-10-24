# Import the boto3 library, which allows interaction with AWS services.
import boto3

# Create an EC2 client and resource object for the 'eu-west-2' region.
ec2_client = boto3.client('ec2', region_name='eu-west-2')
ec2_resource = boto3.resource('ec2', region_name='eu-west-2')

# Using the EC2 resource object, create a new VPC with the specified CIDR block.
new_vpc = ec2_resource.create_vpc(
    CidrBlock='10.0.0.0/16'  # CIDR block for the VPC.
)

# Using the new VPC object, create a new subnet with the specified CIDR block.
new_vpc.create_subnet(
    CidrBlock='10.0.1.0/24'  # CIDR block for the subnet.
)

# Using the new VPC object, create tags for the VPC.
new_vpc.create_tags(
    Tags=[
        {
            'Key': 'Name',  # Tag key.
            'Value': 'my-vpc'  # Tag value.
        },
    ]
)

# Using the EC2 client object, describe all VPCs.
all_vpcs = ec2_client.describe_vpcs()
vpcs = all_vpcs['Vpcs']  # Extract the list of VPCs from the response.

# Loop through each VPC in the list of VPCs.
for vpc in vpcs:
    print(vpc['VpcId'])  # Print the VPC ID to the console.
    cidr_block_assoc_set = vpc['CidrBlockAssociationSet']  # Extract the CIDR block association set from the VPC object.

    # Loop through each association set in the CIDR block association set.
    for assoc_set in cidr_block_assoc_set:
        print(assoc_set['CidrBlock'])  # Print the CIDR block to the console.

