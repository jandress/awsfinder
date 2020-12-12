#search through AWS accounts for a particular host, specified by IP address or instance ID
import boto3
import configparser
import os
import argparse

#get the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-a','--address', help='internal or external ip address to search for',required=False)
parser.add_argument('-i','--instance',help='instance name to search for', required=False)
parser.add_argument('-n','--name',help='name to search for',required=False)
#parser.add_argument('-e','--ethernet',help='ethernet interface id to search for',required=False)
args = parser.parse_args()

#put a placeholder in the empty argument so we don't match an empty argument against an empty AWS field later
if (args.address is None):
        args.address = "foo"
if (args.instance is None):
        args.instance = "foo"

#set an initial region so we can connect up and enumerate things
staticregion = 'us-east-1'

#we're specifically using EC2 here, but this could be retooled for other services easily
services = ['ec2']

#this is windows specific and is where the AWS creds live -- nothing will work without this file being present
#the file should be formatted as specified here http://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html
#updating the file path *should* make everything else work for other OSs
configdir = os.path.expandvars('/home/$USER/.aws/credentials')

#read in the sections from the credentials file
config = configparser.ConfigParser()
config.read(configdir)

#loop through each section in the credentials file - this allows us to search through multiple AWS accounts
for section in config.sections():

        #setup a session for the account we read from the credentials file
        session = boto3.Session(profile_name = section)

        for service in services:

                #setup a client connection so we can ask for the regions -- we can use a static region for the connection, as we'll change it later
                client = session.client('ec2', region_name = staticregion)

                #get the list of regions relative to the service we're using
                regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

                #loop through all of the regions
                for region in regions:
                        print("Checking "+section+" "+region+" "+service)

                        #connect up to the region
                        foo = session.resource(service, region_name = region)

                        #list out the instances
                        instances = foo.instances.filter(
                                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

                        #evaluate each instance and print the match, if we find it
                        for instance in instances:

                                #iface = client.describe_network_interfaces.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running'] }])


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
