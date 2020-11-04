import json
import subprocess
import time

# # Retrieve a JSON of all of the volumes in your specified region and check for and saves volumes with no tags.
def proccessSnapshotsData ():
    snapshotOutput = subprocess.check_output("aws ec2 describe-snapshots --owner-ids 614844069056", shell=True)
    snapshotData = (json.loads(snapshotOutput))
    # print(snapshotData)
    untaggedSnapshotId = []
    untaggedSnapshotVolumeId = []
    for snapshots in snapshotData['Snapshots']:
        tags = snapshots.get('Tags')
        # print(tags)
        isArray = isinstance(tags, list)
        if (isArray is True):
            tagsArray = tags[0]
            isProductTagExist = str(tagsArray.get('Key')) == "product"
            if (isProductTagExist == False):
                untaggedSnapshotId.append(str(snapshots.get('SnapshotId')))
                untaggedSnapshotVolumeId.append(str(snapshots.get('VolumeId')))
        else:
            untaggedSnapshotId.append(str(snapshots.get('SnapshotId')))
            untaggedSnapshotVolumeId.append(str(snapshots.get('VolumeId')))
        
    print(untaggedSnapshotId)
    print("")
    print(untaggedSnapshotVolumeId)
    # tagSnapshots(untaggedSnapshotId, untaggedSnapshotVolumeId)

def tagSnapshots(untaggedSnapshotId, untaggedSnapshotVolumeId):
    quantity = len(untaggedSnapshotId)
    remaining = quantity

    print("*****************************************************")
    print("Total Number of untagged volumes = " + str(quantity))
    print("*****************************************************")
    time.sleep(2)




# # The main function of the script. First thing that it run.
if __name__ == '__main__':
    proccessSnapshotsData ()
