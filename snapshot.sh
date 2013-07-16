#!/bin/bash

SNAPSHOTS=/afs/cern.ch/user/y/yiiyama/snapshots

TARGET=$1
shift

DEST=$SNAPSHOTS/$(date +'%y%m%d')_$(basename $TARGET | sed 's/[.]/_/g')

mkdir $DEST

cp -r $TARGET $DEST/

mkdir $DEST/ATTACHMENTS

while [ $# -ne 0 ]; do
    cp -r $1 $DEST/ATTACHMENTS/
    shift
done

echo "Add a comment to the snapshot:"
read COMMENT
echo $COMMENT > $DEST/NOTE
