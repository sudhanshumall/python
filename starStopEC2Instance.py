import boto3
import sys
region = 'ap-south-1'
ec2 = boto3.client('ec2', region_name=region)

ec2Instances = []

environments  = ['dev','qa','uat']

env = ''
def main():
    global env


    if len(sys.argv) < 3:
        print("Script usage : python startstopEC2Instance.py {start|stop} {dev|qa|uat}\n")
        sys.exit(0)
    else:
        action = sys.argv[1]
        env = sys.argv[2]
                
    getEC2Instances()
    
    if action == "start":
        startInstance()
    elif action == "stop":
        stopInstance()
    else:
        print("Script usage : python startstopEC2Instance.py {start|stop} {dev|qa|uat}\n")



def getEC2Instances():
    global env

    custom_filter = [{
        'Name': 'tag:tagkey',
        'Values': [env]}]
    try:
        response = ec2.describe_tags(Filters=custom_filter)
        tags = response['Tags']
        resourceID = tags[0]['ResourceId']
    except Exception as e:
        print(e)
        
    if resourceID not in ec2Instances:
        ec2Instances.append(resourceID)
    print(ec2Instances)

def startInstance():
    try:

        print("Starting the Instance")
        ec2.start_instances(InstanceIds=ec2Instances)
    except Exception as e:
        print(e)

def stopInstance():
    try:
       
        print("Stopping the Instance")
        ec2.stop_instances(InstanceIds=ec2Instances)
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    main()