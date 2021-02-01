import boto3
import json

f = open("noinstance.txt","w")
f1 = open("instancefound.txt","w")

# Mapping client
client = boto3.client('ec2')
ec2client = boto3.resource('ec2')

# Fetch AMI Image id based on filter 
response = client.describe_images(
    Filters=[
        {
            'Name': 'name',
            'Values': [
                '*ubuntu-16.04-*-vanilla*'
            ]
        },
    ],
)
counter =0
for i in response['Images']:
    # Stores the ImageId from above response
    ImageId = response['Images'] [counter] ['ImageId']
    print("Details for Imageid  "+ ImageId)
    instance_response = client.describe_instances(
     Filters=[
         {
             'Name':'image-id',
             'Values':[ImageId]
         }
     ]
    )
    if len(instance_response['Reservations']) == 0:
        print("Instance doesn't exist \n")
        f.write("No Instance found for AMI" + ImageId + "\n")
    else:
        print(" Instance exist and details are ")
        print("InstanceID is")
        InstanceId = instance_response['Reservations'][0]['Instances'][0]['InstanceId']
        print("\t" + InstanceId)
        print("Tag values are")
        counter1 = 0
        f1.write("AMI is "+ ImageId + "\n")
        f1.write("InstanceId is " + InstanceId + "\n")
        f1.write("Tag values are \n"  )
        for tags in instance_response['Reservations'][0]['Instances'][0]['Tags']:
            print((instance_response['Reservations'][0]['Instances'][0]['Tags'][counter1]['Key'])+" is "+instance_response['Reservations'][0]['Instances'][0]['Tags'][counter1]['Value'])
            f1.write("\t"+ (instance_response['Reservations'][0]['Instances'][0]['Tags'][counter1]['Key'])+" is "+instance_response['Reservations'][0]['Instances'][0]['Tags'][counter1]['Value'] + "\n")
            counter1 = counter1+ 1
        print("State of Instance is "+ instance_response['Reservations'][0]['Instances'][0]['State']['Name']+"\n")
        f1.write("State of "+ InstanceId + " is " + instance_response['Reservations'][0]['Instances'][0]['State']['Name']+"\n\n\n")
        
        

    counter=counter+1

f.close()
f1.close()
