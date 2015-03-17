#!/bin/bash

[ ! -e $HOME/.savediff.list ] && exit 0

ROOTDIR=$(awk 'NR==1' $HOME/.savediff.list)
COPYDIR=$(awk 'NR==2' $HOME/.savediff.list)

echo $ROOTDIR $COPYDIR

awk 'NR>2' $HOME/.savediff.list | \
while read path; do
    [[ $path =~ '^[ ]*#' ]] && continue

    source=$ROOTDIR/$path
    [ ! -f $source ] && continue

    echo $source

    snapshot=$COPYDIR/$path
    if [ -e $snapshot ]; then
        patchbase=$COPYDIR/$path

        [ ! -d $(dirname $patchbase) ] && mkdir -p $(dirname $patchbase)
        diff $snapshot $source > $patchbase.$(date +%Y%m%d%H%M)
    fi

    echo $snapshot

    [ ! -d $(dirname $snapshot) ] && mkdir -p $(dirname $snapshot)

    cp $source $snapshot
done
