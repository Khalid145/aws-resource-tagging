## This script will take EC2 volumes with the same product tag that has been set on its attached EC2 instance. If a EC2 instance has been stopped,
## then the volume is not tagged and ignored.

## To use this script, ensure that your AWS credentials and region have been set as environmental variables.

import json
import subprocess
import time

# Retrieve a JSON of all of the volumes in your specified region and check for and saves volumes with no tags.
def proccessVolumesData ():
    volumeOutput = subprocess.check_output("aws ec2 describe-volumes", shell=True)
    volumeData = (json.loads(volumeOutput))
    # print(volumeData)
    untaggedVolumeId = []
    untaggedVolumeInstanceId = []
    ignoreVolumeId = []
    for volume in volumeData['Volumes']:
        tags = volume.get('Tags')
        print("----------")
        print(tags)
        test = ""
        if (tags is None):
            print("a")
            print(volume.get('Attachments')
            if (volume.get('Attachments') == []):
                print("No attachments")
            # for attachments in volume['Attachments']:
            #     untaggedVolumeInstanceId.append(attachments.get('InstanceId'))
            #     untaggedVolumeId.append(attachments.get('VolumeId'))
        # else:
        #     totalSize = len(tags)
        #     print(totalSize)
        #     for dict in tags:
        #         alreadyProductTagged = dict['Key'] == "product"
        #         print(alreadyProductTagged)
        #         if (alreadyProductTagged == True):
        #             print("Already Here")
        #             for attachments in volume['Attachments']:
        #                 volumeId = str(attachments.get('VolumeId'))
        #                 print(volumeId)
        #         else:
        #             print("Tag this")
        #             #     untaggedVolumeId.append(volumeId)
    print(untaggedVolumeId)





        # if (tags is not None):
        #     totalSize = len(tags)
        #     print(totalSize)
        #     for i in range(totalSize):
        #         print(str(i + 1) + "/" + str(totalSize))
        #         for dict in tags:
        #             checkBoolean = dict['Key'] == "product"
        #             for attachments in volume['Attachments']:
        #                 volumeId = str(attachments.get('VolumeId'))
        #                 if (checkBoolean == True):
        #                     print("IGNORE")
        #                     ignoreVolumeId = volumeId
        #                     break
                
                # for attachments in volume['Attachments']:
                #     volumeId = str(attachments.get('VolumeId'))
                    # if (checkBoolean == True):
                    #     # print(volumeId)
                    #     ignoreVolumeId = volumeId
                    #     print("Ignore " + ignoreVolumeId)
                    #     finalVolumeTagCheck = ignoreVolumeId == volumeId
                    #     print(finalVolumeTagCheck)
                    #     if (finalVolumeTagCheck == True):
                    #         print(attachments.get('VolumeId'))
                    #         untaggedVolumeInstanceId.append(attachments.get('InstanceId'))
                    #         untaggedVolumeId.append(attachments.get('VolumeId'))
                    # else:
                    #     print("tag now")
        # else:
        #     print('Tagging')
            # untaggedVolumeInstanceId.append(attachments.get('InstanceId'))
            # untaggedVolumeId.append(attachments.get('VolumeId'))
    # print(untaggedVolumeId)
    # tagVolumes(untaggedVolumeId, untaggedVolumeInstanceId)

# Retrieves a JSON of EC2 instances based on each volume, check if the instance is running and has a product assigned as a tag and use
# that tag to assign it to the volume.
def tagVolumes(untaggedVolumeId, untaggedVolumeInstanceId):
    quantity = len(untaggedVolumeId)
    remaining = quantity

    print("*****************************************************")
    print("Total Number of untagged volumes = " + str(quantity))
    print("*****************************************************")
    time.sleep(2)
    for i in range(quantity):
        print("Untagged Volume ID: " + str(untaggedVolumeId[i]))
        print("EC2 Instance ID: " + str(untaggedVolumeInstanceId[i]))
        e2Output = subprocess.check_output("aws ec2 describe-instances --instance-ids " + str(untaggedVolumeInstanceId[i]), shell=True)
        ec2Data = (json.loads(e2Output))
        for reservations in ec2Data['Reservations']:
            for instances in reservations['Instances']:
                instanceStateName = instances.get('State').get('Name')
                print('Instance State: ' + instanceStateName)
                for tag in instances['Tags']:
                    if str(tag.get('Key')) == "product":
                        command_string = "aws ec2 create-tags --resources %s --tags Key='%s',Value='%s'" % (untaggedVolumeId[i], str(tag.get('Key')), tag.get('Value'))
                        print("........................................")
                        print("Volume has been tagged with the Product: -> " + tag.get('Value'))
                        # print(command_string)
                        print("........................................")
                        e2Output = subprocess.check_output(command_string, shell=True)
        remaining=remaining - 1
        print("Remaining Volumes to Tag = " + str(remaining))
        print("*****************************************************")

    # The main function of the script. First thing that it run.
if __name__ == '__main__':
    proccessVolumesData()
