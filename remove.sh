#  Author -- Abhinab Padhi 
#  Date   -- 27/05/2020
#  Desc   -- Removes the Images and Snapshots taken during DR activity

#!/bin/sh
REGION="us-west-2"
AMI_FILE="./ids.txt"
SNAP_FILE="./snap.txt"
ic=0 
sc=0
OWNER_ID=self

>$SNAP_FILE
echo "Removing DR AMIs"
while IFS= read -r line
do 
   echo $line 
   ic=$((ic+1))
  aws ec2 describe-images  --owner $OWNER_ID --region $REGION --image-ids $line | grep snap | awk ' { print $2 }'| sed -e 's/"s/s/' -s -e 's/",//' >> snap.txt
   `aws ec2 deregister-image --region $REGION --image-id $line`
   echo "Removed Image $line from $REGION"
done < $AMI_FILE

if [ $ic -gt 1 ] 
then 
  echo "Removed $ic Images from $REGION"
else
  echo "Removed $ic Images from $REGION"
fi

#-------------------------------------------------------------
echo "Removing associated Snapshots"

while IFS= read -r line
do 
   sc=$((sc+1))
   aws ec2 delete-snapshot --region $REGION --snapshot-id $line
   echo "removed associated snapshot $line from $REGION"
done < $SNAP_FILE

if [ $sc -gt 1 ]
then
  echo "Removed $sc Snapshots from $REGION"
else
  echo "Removed $sc Snapshot from $REGION"
fi
