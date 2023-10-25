# Import the boto3 library. This allows you to interact with AWS services.
import boto3

# Create an Amazon Elastic Kubernetes Service (EKS) client object for the 'eu-west-3' region.
client = boto3.client('eks', region_name="eu-west-2")

# Use the EKS client object to list all clusters in the 'eu-west-2' region.
# The 'list_clusters' method returns a dictionary, and we extract the list of clusters using the key 'clusters'.
clusters = client.list_clusters()['clusters']

# Loop through each cluster in the clusters list.
for cluster in clusters:
    # Use the EKS client object to describe the current cluster.
    # The 'describe_cluster' method returns detailed information about the specified cluster.
    response = client.describe_cluster(
        name=cluster  # The name of the cluster to describe.
    )
    # The 'describe_cluster' method returns a dictionary,  extract the cluster information using the key 'cluster'.
    cluster_info = response['cluster']
    # Extract the status, endpoint, and version of the current cluster from the cluster_info dictionary.
    cluster_status = cluster_info['status']
    cluster_endpoint = cluster_info['endpoint']
    cluster_version = cluster_info['version']

    # Print the status, endpoint, and version of the current cluster to the console.
    print(f"Cluster {cluster} status is {cluster_status}")
    print(f"Cluster endpoint: {cluster_endpoint}")
    print(f"Cluster version: {cluster_version}")
