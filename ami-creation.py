"""
    Author -- Abhinab Padhi
    Date   -- 25/04/2020
    Desc   -- AMI creation in North.Virginia region and copying to Oregon region along with Tags for DR activity
"""

# import statements for all the necessary modules
from collections import defaultdict
import datetime
import time
import boto3
import imageid_store as i_s


#script execution start time 
s_time = int(time.time())


# EC2 connections using boto resources
ec2    = boto3.resource('ec2', region_name='us-east-1')
client = boto3.client('ec2', region_name='us-west-2')

# filtering instance based on production tag
tagged_instances = ec2.instances.filter(Filters=[{
    'Name': 'tag:env',
    'Values': ['prod']}])

ic = 0 ## image counter
cc = 0 ## copied image counter
images_to_be_deleted = []

try:
    for instance in tagged_instances.all():
        for tag in instance.tags:

           if 'Name' in tag['Key']:
               name = tag['Value']
               print("Creating Image for instance {} ".format(name))

               image = instance.create_image(
               InstanceId=instance.id,
               Name=name,
               NoReboot=True,
               )

               ic=ic+1

               image.create_tags(Resources=[image.id], Tags=[{'Key':'reference', 'Value':name},{'Key':'Name', 'Value':name}])

               while image.state == 'pending':
                 print("Image creation status is {}".format(image.state))
                 time.sleep(5)
                 image.reload()

               print("\nImage for instance {} created with imageid {}".format(name,image.id))

               if image.state == 'available':
                 copy_images = client.copy_image(Name=name, SourceImageId=image.id, SourceRegion='us-east-1')

                 cc=cc+1

                 print("\nImage {} copied to Orgeon with Image ID {}".format(image.id, [copy_images['ImageId']]))
                 client.create_tags(Resources=[copy_images['ImageId']], Tags=[{'Key':'reference', 'Value':name},{'Key':'Name', 'Value':name}])
                 images_to_be_deleted.append(copy_images['ImageId'])
                 print("Image {} tagged with tag reference: {}".format([copy_images['ImageId']], name))
                 print("\n")

    e_time     = int(time.time()) 
    end_time   = e_time - s_time
    time_taken = int(end_time/60)

    if ic > 1:
      print("{} images created for {} instances".format(ic,ic))
    else:
      print("{} image created for {} instance".format(ic,ic))
    if cc > 1:
      print("{} images copied to Oregon".format(cc))
    else:
      print("{} image copied to Oregon".format(cc))
    if time_taken > 1:
      print("AMI activity completed in {} minutes".format(time_taken))
    else:
      print("AMI activity completed in {} minute".format(time_taken))

    i_s.imageid_store("./ids.txt", images_to_be_deleted)
except:
    print("Script failed to create image")
