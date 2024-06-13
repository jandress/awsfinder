import boto3 #install with pip
import configparser
import os
import argparse

# Get the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', help='internal or external ip address to search for', required=False)
parser.add_argument('-i', '--instance', help='instance name to search for', required=False)
parser.add_argument('-n', '--name', help='name to search for', required=False)

args = parser.parse_args()

# Put a placeholder in the empty argument so we don't match an empty argument against an empty AWS field later 
if args.address is None:
    args.address = "foo"
if args.instance is None:
    args.instance = "foo"

# Set an initial region so we can connect up and enumerate things
staticregion = 'us-east-1'

# We're specifically using EC2 here, but this could be retooled for other services easily
services = ['ec2']

# Update the file path for cross-platform compatibility
if os.name == 'nt':  # For Windows
    configdir = os.path.join(os.environ['USERPROFILE'], '.aws', 'credentials')
else:  # For Linux and other OS
    configdir = os.path.join(os.environ['HOME'], '.aws', 'credentials')

# Read in the sections from the credentials file
config = configparser.ConfigParser()
config.read(configdir)

# Loop through each section in the credentials file - this allows us to search through multiple AWS accounts
for section in config.sections():
    # Setup a session for the account we read from the credentials file
    session = boto3.Session(profile_name=section)
    for service in services:
        # Setup a client connection so we can ask for the regions -- we can use a static region for the connection, as we'll change it later
        client = session.client('ec2', region_name=staticregion)
        # Get the list of regions relative to the service we're using
        regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
        # Loop through all of the regions
        for region in regions:
            print("Checking " + section + " " + region + " " + service)
            # Connect up to the region
            foo = session.resource(service, region_name=region)
            # List out the instances
            instances = foo.instances.filter(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
            # Evaluate each instance and print the match, if we find it
            for instance in instances:
                if instance.tags:
                    for tags in instance.tags:
                        if tags["Key"] == 'Name':
                            instance_name = tags["Value"]
                        else:
                            instance_name = "unknown"
                        if (args.address == instance.private_ip_address or args.address == instance.public_ip_address or args.instance == instance.id or instance_name == args.name):
                            print("Found it, stopping.")
                            print(instance.id, instance.instance_type, instance.key_name, instance.private_ip_address, instance.public_ip_address, instance.public_dns_name)
                            print(instance.tags)
                            exit()
